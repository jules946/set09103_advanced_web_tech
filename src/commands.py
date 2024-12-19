import time
from datetime import datetime, timezone, timedelta
import click
from flask.cli import with_appcontext
from .models import db, NBAPlayer, NBATeam, PlayerStats, Game
from .services.balldontlie_api import BDLAPIService


@click.command('sync-nba')
@with_appcontext
def sync_nba_command():
    """Sync NBA data from API to database"""
    sync_all_data()
    click.echo('NBA data synced successfully')


def register_commands(app):
    app.cli.add_command(sync_nba_command)


def sync_all_data():
    """Main sync function to update all NBA data with rate limiting"""
    api_service = BDLAPIService()

    print("Starting team sync...")
    # teams sync
    teams = api_service.get_all_teams()
    for team_data in teams:
        # check if 'conference' exists and is not empty
        # if we don't do this the API will return teams that no longer exist
        if team_data.get('conference'):
            team = NBATeam.query.get(team_data['id'])
            if not team:
                team = NBATeam(id=team_data['id'])

            team.name = team_data['name']
            team.full_name = team_data['full_name']
            team.abbreviation = team_data['abbreviation']
            team.city = team_data['city']
            team.conference = team_data['conference']
            team.division = team_data['division']
            team.last_updated = datetime.now(timezone.utc)

            db.session.add(team)
    db.session.commit()
    print("Team sync complete!")

    # players sync with rate limiting
    print("Starting player sync...")
    players = api_service.get_all_players()
    total_players = len(players)

    for index, player_data in enumerate(players, 1):
        print(f"Processing player {index}/{total_players}: {player_data['first_name']} {player_data['last_name']}")

        player = NBAPlayer.query.get(player_data['id'])
        if not player:
            player = NBAPlayer(id=player_data['id'])

        player.first_name = player_data['first_name']
        player.last_name = player_data['last_name']
        player.position = player_data['position']
        player.height = player_data['height']
        player.weight = player_data['weight']
        player.team_id = player_data['team']['id']
        player.last_updated = datetime.now(timezone.utc)

        db.session.add(player)

        # commit every 50 players
        if index % 50 == 0:
            db.session.commit()
            print(f"Committed batch of 50 players ({index}/{total_players})")

        # only update stats if they're older than 24 hours
        existing_stats = PlayerStats.query.filter_by(
            player_id=player.id,
            season=2024
        ).first()

        now = datetime.now(timezone.utc)

        # check if we should update player stats (have they been updated within 24 hrs)
        should_update = not existing_stats or \
                        (existing_stats.last_updated.replace(tzinfo=timezone.utc) < now - timedelta(hours=24))

        if should_update:
            time.sleep(0.6)  # Wait 600ms between stats requests
            stats = api_service.get_player_stats(player.id)
            if stats:
                stat = existing_stats or PlayerStats(player_id=player.id, season=2024)
                stat.games_played = stats[0].get('games_played', 0)
                stat.pts = stats[0].get('pts', 0)
                stat.reb = stats[0].get('reb', 0)
                stat.ast = stats[0].get('ast', 0)
                stat.last_updated = now  # Use the same now value we created above
                db.session.add(stat)

    db.session.commit()
    print("Player and stats sync complete!")

    # Games sync with rate limiting
    print("Starting games sync...")
    now = datetime.now(timezone.utc)
    two_weeks_ago = now - timedelta(weeks=2)
    two_weeks_future = now + timedelta(weeks=2)

    for index, team in enumerate(NBATeam.query.all(), 1):
        print(f"Processing game data for team {index}/{len(teams)}: {team.full_name}")

        time.sleep(0.6)
        upcoming = api_service.get_team_games(team.id, "upcoming")
        time.sleep(0.6)
        completed = api_service.get_team_games(team.id, "completed")

        for game_data in upcoming + completed:
            game_date = datetime.strptime(game_data['date'], '%Y-%m-%d').replace(tzinfo=timezone.utc)

            if two_weeks_ago <= game_date <= two_weeks_future:
                game = Game.query.get(game_data['id'])
                if not game:
                    game = Game(id=game_data['id'])

                game.date = game_date  # Store the timezone-aware date
                game.home_team_id = game_data['home_team']['id']
                game.visitor_team_id = game_data['visitor_team']['id']
                game.home_team_score = game_data.get('home_team_score')
                game.visitor_team_score = game_data.get('visitor_team_score')
                game.status = game_data['status']
                game.season = 2024
                game.last_updated = now

                db.session.add(game)

        # commit after each team's games
        db.session.commit()
        print(f"Committed games for {team.full_name}")

    print("Games sync complete!")
    print("Full sync completed successfully!")