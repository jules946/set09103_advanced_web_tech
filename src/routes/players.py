from flask import Blueprint, render_template, abort
from ..services.balldontlie_api import BDLAPIService
from ..services.nba_api import NBAAPIService

players_bp = Blueprint('players', __name__)
bdl_api = BDLAPIService()
nba_api = NBAAPIService()

@players_bp.route('/player/<int:player_id>')
def player_details(player_id):
    """
    Get player details and stats by ID
    """
    player = bdl_api.get_player(player_id)
    if not player:
        abort(404)

    stats = bdl_api.get_player_stats(player_id)
    # TODO: Create 404 page
    if not stats:
        print(f"No stats found for player: {player_id}")
        abort(404)
    player_pic_url = nba_api.get_player_picture_url(player["first_name"], player["last_name"])
    upcoming_team_games = bdl_api.get_team_games(player["team"]["id"], "upcoming")
    recent_team_games = bdl_api.get_team_games(player["team"]["id"], "completed")
    return render_template(
        'players/details.html',
        player=player,
        stats=stats,
        player_pic_url=player_pic_url,
        upcoming_games=upcoming_team_games,
        recent_games=recent_team_games
    )
