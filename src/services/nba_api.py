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
        Get lis of all teams.
        """
        # fetch all teams from the API
        response = requests.get(f"{self.base_url}/teams", headers=self.headers)
        return self.process_response(response)

    def get_team(self, team_id):
        """Get team details by ID"""
        response = requests.get(f"{self.base_url}/teams/{team_id}", headers=self.headers)
        return self.process_response(response)

    def unified_search(self, query: str) -> Dict[str, List]:
        """
        Perform a unified search for both players and teams,
        returning results sorted by match relevance
        """
        # get API results
        players = self.search_players(query)
        teams = self.search_teams(query)

        # create unified results list with match scores
        unified_results = []

        # process players
        for player in players:
            name = f"{player['first_name']} {player['last_name']}"
            score = fuzz.partial_ratio(query.lower(), name.lower())
            # bonus for exact substring matches
            if query.lower() in name.lower():
                score += 20

            if score > 80:
                unified_results.append({
                    "type": "player",
                    "data": player,
                    "score": score
                })

        # process teams
        for team in teams:
            score = fuzz.partial_ratio(query.lower(), team['full_name'].lower())
            # bonus for exact substring matches
            if query.lower() in team['full_name'].lower():
                score += 20

            if score > 80:
                unified_results.append({
                    "type": "team",
                    "data": team,
                    "score": score
                })

        # sort all results by score, descending
        unified_results.sort(key=lambda x: x['score'], reverse=True)

        return {
            "results": unified_results,
            "total_results": len(unified_results)
        }

    def get_player_stats(self, player_id, season=2024):
        """Get player stats for a specific season"""
        params = {
            "player_id": player_id,
            "season": season
        }
        response = requests.get(f"{self.base_url}/season_averages", headers=self.headers, params=params)
        return self.process_response(response)