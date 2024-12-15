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


@players_bp.route('/players/search')
def search_players():
    """
    Search for players by name
    """
    # get the query parameter from the URL
    query = request.args.get('q', '')
    if query:
        # search for players using the NBA API
        players = nba_api.search_players(query)
        # render the search results template with results from the API
        return render_template('players/search.html', players=players, query=query)
    return render_template('players/search.html', players=[], query='')