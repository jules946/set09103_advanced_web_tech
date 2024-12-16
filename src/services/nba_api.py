from nba_api.stats.static import players


class NBAAPIService:
    """
    Utility class for retrieving NBA player information and assets from nba_api library.
    """
    def __init__(self):
        # luckily nba has done this for me :)
        self.placeholder_pic_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/placeholder.png"

    @staticmethod
    def _get_player_id(first_name, second_name):
        """
        Gets NBA player ID by first and last name.
        """
        player = players.find_players_by_full_name(f"{first_name} {second_name}")
        if player:
            return player[0]['id']
        return None

    def get_player_picture_url(self, first_name, second_name):
        """
        Get player picture URL by player ID.
        """
        # This isn't great but... it works, until nba will change url structure
        player_id = self._get_player_id(first_name, second_name)
        if player_id:
            return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
        return self.placeholder_pic_url
