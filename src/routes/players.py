from flask import Blueprint, render_template, abort
from ..services.nba_api import NBAAPIService
from ..models import NBAPlayer, PlayerStats
from src.routes.main import get_team_games

players_bp = Blueprint('players', __name__)
nba_api = NBAAPIService()

@players_bp.route('/player/<int:player_id>')
def player_details(player_id):
    """
    Get player details and stats by ID
    """
    # TODO: Create 404 page
    # get player by ID from database
    player = NBAPlayer.query.get_or_404(player_id)
    if not player:
        abort(404)

    # get player stats from database
    stats = PlayerStats.query.filter_by(player_id=player_id, season=2024).first()
    if not stats:
        print(f"No stats found for player: {player_id}")
        abort(404)

    # get player pic url using NBA api
    player_pic_url = nba_api.get_player_picture_url(player.first_name, player.last_name)

    # get upcoming and recent team games
    upcoming_team_games = get_team_games(player.team_id, status="upcoming", limit=3)
    recent_team_games = get_team_games(player.team_id, status="completed", limit=3)

    return render_template(
        'players/details.html',
        player=player,
        stats=stats,
        player_pic_url=player_pic_url,
        upcoming_games=upcoming_team_games,
        recent_games=recent_team_games
    )
