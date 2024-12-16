import os
import requests
from typing import Dict, List
from rapidfuzz import process, fuzz

class NBAApiService:
    """
    Service class to interact with the balldontlie NBA API
    """
    def __init__(self):
        self.base_url = "https://api.balldontlie.io/v1"
        self.headers = {"Authorization": os.environ.get('NBA_API_KEY')}

    @staticmethod
    def process_response(response):
        """Process the response from the API"""
        if response.status_code == 200:
            try:
                return response.json().get('data', [])
            except ValueError as e:
                print("JSONDecodeError:", e)
        else:
            print(f"Error: Received status code {response.status_code}")
            print("Response Text:", response.text)
        return []

    def get_player(self, player_id):
        """Get player details by ID"""
        response = requests.get(f"{self.base_url}/players/{player_id}", headers=self.headers)
        return self.process_response(response)

    def search_players(self, name):
        """Search players by name"""
        params = {"search": name}
        response = requests.get(f"{self.base_url}/players", headers=self.headers, params=params)
        return self.process_response(response)

    def search_teams(self, search_query):
        """
        Search teams by name using fuzzy matching, returns teams sorted by match quality.
        """
        # fetch all teams from the API
        response = requests.get(f"{self.base_url}/teams", headers=self.headers)
        all_teams = self.process_response(response)

        # NBA data api doesn't have search functionality, unlike the players
        scored_matches = []
        
        for team in all_teams:
            # calculate match scores for both full_name and name
            full_name_score = fuzz.partial_ratio(search_query.lower(), team["full_name"].lower())
            name_score = fuzz.partial_ratio(search_query.lower(), team["name"].lower())

            # check for exact substring matches
            query_lower = search_query.lower()
            full_name_contains = query_lower in team["full_name"].lower()
            name_contains = query_lower in team["name"].lower()

            # only consider the higher of the two scores
            final_score = max(full_name_score, name_score)

            # add bonus points for exact substring matches
            if full_name_contains or name_contains:
                final_score += 20

            # filter down to high quality matches
            if final_score >= 80:
                scored_matches.append({
                    "team": team,
                    "score": final_score
                })

        # sort score in descending order
        scored_matches.sort(key=lambda x: x["score"], reverse=True)

        # return team details from the initial API response
        return [match["team"] for match in scored_matches]

    def get_team(self, team_id):
        """Get team details by ID"""
        response = requests.get(f"{self.base_url}/teams/{team_id}", headers=self.headers)
        return self.process_response(response)

    def unified_search(self, query: str) -> Dict[str, List]:
        """
        Perform a unified search for both players and teams
        Returns a dictionary with both player and team results
        """
        players = self.search_players(query)
        teams = self.search_teams(query)

        return {
            "players": players,
            "teams": teams,
            "total_results": len(players) + len(teams)
        }

    def get_player_stats(self, player_id, season=2024):
        """Get player stats for a specific season"""
        params = {
            "player_id": player_id,
            "season": season
        }
        response = requests.get(f"{self.base_url}/season_averages", headers=self.headers, params=params)
        return self.process_response(response)