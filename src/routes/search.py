from flask import Blueprint, render_template, request
from src.models import NBATeam, NBAPlayer
from typing import Dict, List
from rapidfuzz import fuzz

search_bp = Blueprint('search', __name__)



def unified_search(search_query: str, all_players, all_teams) -> Dict[str, List]:
    """
    Perform a unified search for both players and teams,
    returning results sorted by match relevance.
    """

    # create unified results list with match scores
    unified_results = []

    # helper function to calculate normalized scores
    def calculate_score(query: str, target: str) -> float:
        # primary score using WRatio
        calculated_score = fuzz.WRatio(query.lower(), target.lower())

        # adjust score if search query is a substring of target
        # e.g. "LeBron" should match "LeBron James"
        if query.lower() in target.lower():
            calculated_score += int((len(query) / len(target)) * 20)

        return calculated_score

    # process players
    for player in all_players:
        name = f"{player.first_name} {player.last_name}"
        score = calculate_score(search_query, name)

        if score > 80:
            unified_results.append({
                "type": "player",
                "data": player,
                "score": score
            })

    # process teams
    for team in all_teams:
        # calculate match scores for both full_name and name
        full_name_score = calculate_score(search_query, team.full_name)
        name_score = calculate_score(search_query, team.name)

        # only consider the higher of the two scores
        score = max(full_name_score, name_score)

        if score > 80:
            unified_results.append({
                "type": "team",
                "data": team,
                "score": score
            })

    # sort all results by score, descending
    unified_results.sort(key=lambda x: x['score'], reverse=True)

    return {
        "results": unified_results,
        "total_results": len(unified_results)
    }

@search_bp.route('/search')
def search_page():
    """
    Unified search endpoint that returns combined and sorted player/team results
    """

    # get query from request i.e. search term
    query = request.args.get('q', '')
    if query:

        # get all players from db
        all_players = NBAPlayer.query.all()
        # get all teams from db
        all_teams = NBATeam.query.all()

        results = unified_search(search_query=query, all_players=all_players, all_teams=all_teams)

        return render_template('search/results.html',
                             results=results['results'],
                             total_results=results['total_results'],
                             query=query)
    return render_template('search/results.html',
                         results=[],
                         total_results=0,
                         query='')