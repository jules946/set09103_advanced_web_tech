from flask import Blueprint, render_template, request, abort
from ..services.nba_api import NBAApiService

search_bp = Blueprint('search', __name__)
nba_api = NBAApiService()

@search_bp.route('/search')
def unified_search():
    """
    Unified search endpoint that returns combined and sorted player/team results
    """
    query = request.args.get('q', '')
    if query:
        results = nba_api.unified_search(query)
        return render_template('search/results.html',
                             results=results['results'],
                             total_results=results['total_results'],
                             query=query)
    return render_template('search/results.html',
                         results=[],
                         total_results=0,
                         query='')