import os
import requests
from typing import Dict, List
from rapidfuzz import fuzz
from datetime import datetime, timedelta

class BDLAPIService:
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
        response = requests.get(f"{self.base_url}/players/active", headers=self.headers, params=params)
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

    def unified_search(self, search_query: str) -> Dict[str, List]:
        """
        Perform a unified search for both players and teams,
        returning results sorted by match relevance.
        """
        # get API results
        players = self.search_players(search_query)
        teams = self.search_teams(search_query)

        # create unified results list with match scores
        unified_results = []

        # helper function to calculate normalized scores
        def calculate_score(query: str, target: str) -> float:
            # primary score using WRatio
            calculated_score = fuzz.WRatio(query.lower(), target.lower())

            # adjust score if search query is a substring of target
            # e.g. "LeBron" should match "LeBron James"
            if query.lower() in target.lower():
                calculated_score += int((len(query) / len(target)) * 20)

            return min(calculated_score, 100)

        # process players
        for player in players:
            name = f"{player['first_name']} {player['last_name']}"
            score = calculate_score(search_query, name)

            if score > 80:
                unified_results.append({
                    "type": "player",
                    "data": player,
                    "score": score
                })

        # process teams
        for team in teams:
            # calculate match scores for both full_name and name
            full_name_score = calculate_score(search_query, team["full_name"])
            name_score = calculate_score(search_query, team["name"])

            # only consider the higher of the two scores
            score = max(full_name_score, name_score)

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

    def get_team_games(self, team_id, status):
        """
        Get the last 3 and next 3 games for a team based on the current date.
        """
        # TODO: this will be bad during off season
        # calculate the date range: two weeks before and after current date

        today = datetime.now()
        start_date = (today - timedelta(weeks=2)).strftime("%Y-%m-%d")
        end_date = (today + timedelta(weeks=2)).strftime("%Y-%m-%d")

        # Set params based on status
        params = {
            "team_ids[]": team_id,
            "start_date": start_date,
            "end_date": end_date
        }

        # make request
        response = requests.get(f"{self.base_url}/games", headers=self.headers, params=params)
        games = self.process_response(response)

        # filter games by status and return the appropriate 3 games
        if status == "completed":
            completed_games = [game for game in games if game["status"] == "Final"]
            return completed_games[-3:]
        elif status == "upcoming":
            upcoming_games = [game for game in games if game["status"] not in ["Final", ""]]
            return upcoming_games[:3]
        else:
            raise ValueError("Invalid status. Must be 'upcoming' or 'completed'.")