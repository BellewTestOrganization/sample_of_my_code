from .base_parser import BaseParser
from pprint import pprint
import datetime


class SportRadarParser(BaseParser):
    def __init__(self):
        self.company_name = 'Sportradar'
        super().__init__()

    def find_sport_name(self, obj):
        return obj['BetradarLivescoreData']['Sport']['Name']

    def find_categories(self, obj):
        return obj['BetradarLivescoreData']['Sport']['Category']

    def find_tournaments_data(self, category):
        tournaments_data = category['Tournament']
        if not isinstance(tournaments_data, list):
            tournaments_data = [tournaments_data]
        return tournaments_data

    def find_matches_data(self, tournament):
        matches_data = tournament['Match']
        if not isinstance(matches_data, list):
            matches_data = [matches_data]
        return matches_data

    def find_tournament_name(self, tournament):
        return self.__find_text(tournament['Name'])

    def __find_text(self, parsed_list):
        parsed_name = ''
        for parsed in parsed_list:
            if isinstance(parsed, str):
                parsed_name = parsed
                continue
        return parsed_name

    def find_matches_team(self, obj, number):
        return obj['Team{}'.format(number)]['Name']['#text']

    def find_matches_country(self, obj):
        return obj['Venue']['Country']['@name']

    def find_matches_city(self, obj):
        return obj['Venue']['City']['@name']

    def find_matches_stadium(self, obj):
        return obj['Venue']['Stadium']['@name']

    def find_match_winner(self, obj):
        winner = None
        if obj.get('Winner'):
            winner = int(obj['Winner'])
        return winner

    def find_match_date(self, obj):
        date = obj['MatchDate']
        return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S CEST")

    def find_match_status(self, obj):
        return obj['Status']['Name']['#text']

    def find_match_structure(self, obj):
        structure = []
        if obj.get('Lineups') and obj['Lineups'].get('TeamPlayer'):
            structure = obj['Lineups']['TeamPlayer']
        return structure

    def find_player_data(self, player_data, team1, team2):
        player_name = player_data['Player']['#text']
        shirt_number = int(player_data['ShirtNumber'])
        substructure = True if player_data['Substitute'] == '1' else False
        team = team1 if player_data['PlayerTeam'] == '1' else team2
        return player_name, shirt_number, team, substructure

    def find_match_goals(self, matches_data):
        result = []
        if matches_data.get('Goals'):
            result = matches_data['Goals']['Goal']
        if not isinstance(result, list):
            result = [result]
        return result

    def find_goal(self, goal_data, team1, team2):
        team = team1 if goal_data.get('Team1') else team2
        player = goal_data['Player']['#text']
        time = goal_data['Time']
        return team, player, time

    def find_match_cards(self, matches_data):
        result = []
        if matches_data.get('Cards'):
            result = matches_data['Cards']['Card']
        if not isinstance(result, list):
            result = [result]
        return result

    def find_card(self, goal_data, team1, team2):
        type = goal_data['@type']
        team = team1 if goal_data.get('PlayerTeam') == '1' else team2
        player = goal_data['Player']['#text']
        time = goal_data['Time']
        return team, player, time, type

    def find_match_referee(self, matches_data):
        referee = None
        country = None
        if matches_data.get('Referee'):
            referee = matches_data['Referee']['@name']
        return referee, country

    def find_match_substitutions(self, matches_data):
        result = []
        if matches_data.get('Substitutions'):
            result = matches_data['Substitutions']['Substitution']
        if not isinstance(result, list):
            result = [result]
        return result

    def find_substitutions(self, substitutions_data, team1, team2):
        player_in = substitutions_data['PlayerIn']['#text']
        player_out = substitutions_data['PlayerOut']['#text']
        team = team1 if substitutions_data.get('PlayerTeam') == '1' else team2
        time = substitutions_data['Time']
        return team, player_in, player_out, time

    def find_format_statistic(self, matches_data, team1, team2):
        result = []
        stat_data = matches_data.get('Statistics')
        if stat_data:
            for name, data in stat_data.items():
                result.append({
                    'name': name,
                    'team': team1,
                    'value': data['Team1']
                })
                result.append({
                    'name': name,
                    'team': team2,
                    'value': data['Team2']
                })
        return result
