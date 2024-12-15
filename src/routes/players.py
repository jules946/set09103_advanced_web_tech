from flask import Blueprint, render_template, request, abort
from ..services.nba_api import NBAApiService

players_bp = Blueprint('players', __name__)
nba_api = NBAApiService()


@players_bp.route('/player/<int:player_id>')
def player_details(player_id):
    """
    Get player details and stats by ID
    """
    player = nba_api.get_player(player_id)
    if not player:
        abort(404)

    stats = nba_api.get_player_stats(player_id)
    return render_template('players/details.html', player=player, stats=stats)
