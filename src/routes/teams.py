from flask import Blueprint, render_template, abort
from ..services.nba_api import NBAApiService

teams_bp = Blueprint('teams', __name__)
nba_api = NBAApiService()


@teams_bp.route('/team/<int:team_id>')
def team_details(team_id):
    """
    Get team details by ID
    """
    team = nba_api.get_team(team_id)
    if not team:
        abort(404)

    return render_template('teams/details.html', team=team)