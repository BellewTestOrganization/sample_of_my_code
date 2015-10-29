import xmltodict

from sport_parser.models import Sport
from sport_parser.libs.saver.saver import Saver
from sport_parser.libs.xml.abstract_parser import AbstractParser


class BaseParser(AbstractParser):
    company_name=''

    def __init__(self):
        self.saver = Saver(self.company_name)

    def parse(self, xml):
        obj = xmltodict.parse(xml, process_namespaces=True)
        try:
            self.sport = Sport.objects.get(name=self.find_sport_name(obj))
        except:
            raise Exception('This sport type is not supported')
        categories = self.find_categories(obj)
        for category in categories:
            if not isinstance(category, dict):
                # TODO log this
                continue
            try:
                saved_category = self.saver.save_category(self.sport,
                                                          category['Name'])
            except KeyError:
                # TODO log this
                continue
            tournaments_data = self.find_tournaments_data(category)
            for tournament_data in tournaments_data:

                saved_tournament = \
                    self.saver.save_tournament(
                        saved_category,
                        self.find_tournament_name(tournament_data))
                matches_data = self.find_matches_data(tournament_data)
                for match_data in matches_data:
                    self.save_match(match_data, saved_tournament)

    def save_match(self, matches_data, tournament):
        team1_name = self.find_matches_team(matches_data, 1)
        team2_name = self.find_matches_team(matches_data, 2)
        team1 = self.saver.save_team(team1_name)
        team2 = self.saver.save_team(team2_name)
        try:
            country_name = self.find_matches_country(matches_data)
            sity_name = self.find_matches_city(matches_data)
            stadium_name = self.find_matches_stadium(matches_data)
            country = self.saver.save_country(country_name)
            sity = self.saver.save_city(sity_name, country)
            stadium = self.saver.save_stadium(stadium_name, sity)
        except:
            stadium = None
        status_name = self.find_match_status(matches_data)
        status = self.saver.save_match_status(status_name)
        date = self.find_match_date(matches_data)

        winner = self.find_match_winner(matches_data)

        match = self.saver.save_match(
            tournament=tournament,
            status=status,
            team1=team1,
            team2=team2,
            stadium=stadium,
            date=date,
            winner=winner
        )
        statistics = self.find_format_statistic(matches_data, team1, team2)
        for statistic in statistics:
            self.saver.save_statistic(statistic, match)
        referee, country_name = self.find_match_referee(matches_data)
        if referee:
            self.saver.save_referee(referee, country_name, match)
        structure = self.find_match_structure(matches_data)
        if len(structure):
            for player in structure:
                player_name, shirt_number, team, substructure = \
                    self.find_player_data(player, team1, team2)
                self.saver.save_player(
                    player_name, shirt_number, team, substructure, match
                )
        goals = self.find_match_goals(matches_data)
        if len(goals):
            for goal in goals:
                team, player, time = self.find_goal(goal, team1, team2)
                self.saver.save_goal(team, player, time, match)
        cards = self.find_match_cards(matches_data)
        if len(cards):
            for card in cards:
                team, player, time, type = self.find_card(card, team1, team2)
                self.saver.save_card(team, player, time, type, match)

        substitutions = self.find_match_substitutions(matches_data)
        if len(substitutions):
            for substitution in substitutions:
                team, player_in, player_out, time = \
                    self.find_substitutions(substitution, team1, team2)
                self.saver.save_substitutions(team, player_in, player_out, time, match)
