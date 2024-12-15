from flask import Blueprint, render_template, request, abort
from ..services.nba_api import NBAApiService

search_bp = Blueprint('search', __name__)
nba_api = NBAApiService()

@search_bp.route('/search')
def unified_search():
    """
    Unified search endpoint for both players and teams
    """
    query = request.args.get('q', '')
    if query:
        results = nba_api.unified_search(query)
        return render_template('search/results.html',
                             players=results['players'],
                             teams=results['teams'],
                             query=query)
    return render_template('search/results.html',
                         players=[],
                         teams=[],
                         query='')