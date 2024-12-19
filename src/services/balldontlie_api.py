import os
import requests
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

    def get_all_players(self, cursor=None, per_page=100):
        """Get list of all active players with pagination"""
        all_players = []
        while True:
            params = {"per_page": per_page}
            if cursor:
                params["cursor"] = cursor
            response = requests.get(f"{self.base_url}/players/active", headers=self.headers, params=params)
            data = self.process_response(response)
            all_players.extend(data)
            meta = response.json().get("meta", {})
            cursor = meta.get("next_cursor")
            if not cursor:
                break
        return all_players

    def get_player(self, player_id):
        """Get player details by ID"""
        response = requests.get(f"{self.base_url}/players/{player_id}", headers=self.headers)
        return self.process_response(response)

    def search_players(self, name):
        """Search players by name"""
        params = {"search": name}
        response = requests.get(f"{self.base_url}/players/active", headers=self.headers, params=params)
        return self.process_response(response)

    def get_all_teams(self):
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