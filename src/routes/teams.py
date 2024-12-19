from flask import Blueprint, render_template, abort
from ..services.nba_api import NBAAPIService
from ..models import NBAPlayer, NBATeam, Game, PlayerStats
from src.routes.main import get_team_games
teams_bp = Blueprint('teams', __name__)
nba_api = NBAAPIService()


@teams_bp.route('/team/<int:team_id>')
def team_details(team_id):
    """
    Get team details by ID
    """
    # get team info from db
    team = NBATeam.query.get_or_404(team_id)
    if not team:
        abort(404)

    # get team players
    team_players = team.players

    # get 3 upcoming and recent team games from db
    upcoming_team_games = get_team_games(team_id, status="upcoming", limit=3)
    recent_team_games = get_team_games(team_id, status="completed", limit=3)

    # get team logo url with NBA API
    team_logo_url = nba_api.get_team_logo(team.full_name)

    return render_template(
        'teams/details.html',
        team=team,
        team_players=team_players,
        upcoming_games=upcoming_team_games,
        recent_games=recent_team_games,
        team_logo_url=team_logo_url
    )