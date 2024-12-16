from flask import Blueprint, render_template, abort
from ..services.balldontlie_api import BDLAPIService
from ..services.nba_api import NBAAPIService

teams_bp = Blueprint('teams', __name__)
bdl_api = BDLAPIService()
nba_api = NBAAPIService()


@teams_bp.route('/team/<int:team_id>')
def team_details(team_id):
    """
    Get team details by ID
    """
    team = bdl_api.get_team(team_id)
    if not team:
        abort(404)

    upcoming_team_games = bdl_api.get_team_games(team["id"], "upcoming")
    recent_team_games = bdl_api.get_team_games(team["id"], "completed")
    team_logo_url = nba_api.get_team_logo(team["full_name"])
    return render_template(
        'teams/details.html',
        team=team,
        upcoming_games=upcoming_team_games,
        recent_games=recent_team_games,
        team_logo_url=team_logo_url
    )