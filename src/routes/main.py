from flask import Blueprint, render_template
from sqlalchemy.sql.expression import func
from flask_login import current_user
from ..models import NBAPlayer, NBATeam, Game, PlayerStats
from ..services.nba_api import NBAAPIService

main_bp = Blueprint('main', __name__)
nba_api = NBAAPIService()


def get_team_games(team_id, status, limit=1):
    """Helper function to get team games by status"""
    if status == "completed":
        # games that are finished
        status_filter = Game.status == "Final"
    else:  # upcoming/in progress
        status_filter = Game.status != "Final"

    query = Game.query.filter(
        (Game.home_team_id == team_id) |
        (Game.visitor_team_id == team_id),
        status_filter
    ).order_by(Game.date.desc() if status == "completed" else Game.date.asc()).limit(limit)

    return query.all()


@main_bp.route('/')
def index():
    context = {
        'is_authenticated': current_user.is_authenticated
    }

    try:
        # If user is not authenticated or has no favorites, pick random team/player
        if not current_user.is_authenticated or not current_user.favorite_team or not current_user.favorite_player:
            context['favorite_team'] = NBATeam.query.order_by(func.random()).first()
            context['favorite_player'] = NBAPlayer.query.order_by(func.random()).first()
            context['main_page_title'] = "Player and Team Spotlight"
        else:
            # Fetch user's favorite team and player
            context['favorite_team'] = NBATeam.query.get_or_404(current_user.favorite_team)
            context['favorite_player'] = NBAPlayer.query.get_or_404(current_user.favorite_player)
            context['main_page_title'] = "Your Favourites"

        # Get team games
        context['team_upcoming_games'] = get_team_games(context['favorite_team'].id, "upcoming")

        # Get player stats and picture
        context['player_stats'] = PlayerStats.query.filter_by(
            player_id=context['favorite_player'].id,
            season=2024
        ).first()

        context['player_pic_url'] = nba_api.get_player_picture_url(
            context['favorite_player'].first_name,
            context['favorite_player'].last_name
        )
        context['team_logo_url'] = nba_api.get_team_logo(context['favorite_team'].full_name)

        # Get player's team games if different from favorite team
        if context['favorite_player'].team_id != context['favorite_team'].id:
            context['player_upcoming_games'] = get_team_games(context['favorite_player'].team_id, "upcoming")
        else:
            context['player_upcoming_games'] = context['team_upcoming_games']
            context['player_recent_games'] = context['team_recent_games']

    except Exception as e:
        print(f"Error loading homepage: {str(e)}")
        context['error'] = "There was an error loading your favorites. Please try again later."

    return render_template('index.html', **context)