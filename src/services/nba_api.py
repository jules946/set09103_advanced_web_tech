import os
import requests


class NBAApiService:
    """
    Service class to interact with the balldontlie NBA API
    """
    def __init__(self):
        self.base_url = "https://api.balldontlie.io/v1"
        self.headers = {"Authorization": os.environ.get('NBA_API_KEY')}

    def get_player(self, player_id):
        """Get player details by ID"""
        response = requests.get(f"{self.base_url}/players/{player_id}", headers=self.headers)
        if response.status_code == 200:
            try:
                return response.json().get('data', [])
            except ValueError as e:
                print("JSONDecodeError:", e)
        else:
            print(f"Error: Received status code {response.status_code}")
        return None

    def search_players(self, name):
        """Search players by name"""
        params = {"search": name}
        response = requests.get(f"{self.base_url}/players", headers=self.headers, params=params)

        # Log the response for debugging
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        if response.status_code == 200:
            try:
                return response.json().get('data', [])
            except KeyError as e:
                print("KeyError:", e)
            except ValueError as e:
                print("JSONDecodeError:", e)
        else:
            print(f"Error: Received status code {response.status_code}")
        return []

    def get_player_stats(self, player_id, season=2023):
        """Get player stats for a specific season"""
        params = {
            "player_id": player_id,
            "season": season
        }
        response = requests.get(f"{self.base_url}/season_averages", headers=self.headers, params=params)
        if response.status_code == 200:
            try:
                return response.json().get('data', [])
            except ValueError as e:
                print("JSONDecodeError:", e)
        else:
            print(f"Error: Received status code {response.status_code}")
        return []
