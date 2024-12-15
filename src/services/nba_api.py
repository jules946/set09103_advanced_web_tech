import os
import requests
from typing import Dict, List

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

    def search_teams(self, name):
        """Search teams by name"""
        params = {"search": name}
        response = requests.get(f"{self.base_url}/teams", headers=self.headers, params=params)
        return self.process_response(response)

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