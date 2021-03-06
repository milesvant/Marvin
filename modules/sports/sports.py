from math import isnan
from datetime import datetime, timedelta
from pybaseball import schedule_and_record
from .sports_helper import SportsHelper


class Sports:
    """Class which allows Marvin to retrieve sports scores.

        Attributes:
            helper: A SportsHelper object which assists with the
                interpretation of user commands.
    """

    def __init__(self):
        self.helper = SportsHelper()

    def route_command(self, command, say, listen):
        """Executes and generates  a string response for a given sports
            command.

            Args:
                command: a string command which requests some action or
                    information related to sports.
                say: A function which will say (either through text to speech
                    or printing) a string in the main speaker loop
                listen: A function which will listen and record user input
                    through either speech to text or through the CLI
            Returns:
                True if a command was executed (or failed while executed) and
                    false if the command was invalid.
        """
        label, args = self.helper.parse_command(command)
        # if the game was today
        if label == "result today":
            today = datetime.utcnow().date()
            current_year = today.year
            dataframe = schedule_and_record(
                current_year, self.helper.baseball_teams_to_abbrev[args])
            index = self.helper.dataframe_first_instance_of(
                dataframe, self.helper.date_to_dataframe_index(today))
            if index == -1:
                say("Could not find information about that game at this\
time")
                return True
            opp = self.helper.abbrev_to_baseball_teams[dataframe['Opp'][index]]
            runs = dataframe['R'][index]
            if not isnan(runs) or isnan(index):
                runs = int(dataframe['R'][index])
                runs_against = int(dataframe['RA'][index])
                if runs > runs_against:
                    response = "The {} beat the {} today, {} to {}".format(
                        args, opp, runs, runs_against)
                else:
                    response = "The {} lost to the {} today, {} to {}".format(
                        args, opp, runs, runs_against)
            else:
                response = "Could not find information about that game at this\
time"
            say(response)
        # if the game was yesterday
        elif label == "result yesterday":
            yesterday = datetime.utcnow().date() - timedelta(1)
            current_year = yesterday.year
            dataframe = schedule_and_record(
                current_year, self.helper.baseball_teams_to_abbrev[args])
            index = self.helper.dataframe_first_instance_of(
                dataframe, self.helper.date_to_dataframe_index(yesterday))
            if index == -1 or isnan(index):
                say("Could not find information about that game at this\
time")
                return True
            opp = self.helper.abbrev_to_baseball_teams[dataframe['Opp'][index]]
            runs = dataframe['R'][index]
            if not isnan(runs):
                runs = int(dataframe['R'][index])
                runs_against = int(dataframe['RA'][index])
                if runs > runs_against:
                    response = "The {} beat the {} yesterday, {} to {}".format(
                        args, opp, runs, runs_against)
                else:
                    response = "The {} lost to the {} yesterday, {} to {}".format(
                        args, opp, runs, runs_against)
            else:
                response = "Could not find information about that game at this\
time"
            say(response)
        # if the game was on a day of the week which was specified
        elif label == "result specific":
            day = self.helper.day_of_week_to_date(args['day'], datetime.utcnow().date())
            current_year = day.year
            dataframe = schedule_and_record(
                current_year, self.helper.baseball_teams_to_abbrev[args['team']])
            index = self.helper.dataframe_first_instance_of(
                dataframe, self.helper.date_to_dataframe_index(day))
            if index == -1 or isnan(index):
                say("Could not find information about that game at this\
time")
                return True
            opp = self.helper.abbrev_to_baseball_teams[dataframe['Opp'][index]]
            runs = dataframe['R'][index]
            if not isnan(runs):
                runs = int(runs)
                runs_against = int(dataframe['RA'][index])
                if runs > runs_against:
                    response = "The {} beat the {} on {}, {} to {}".format(
                        args['team'], opp, args['day'], runs, runs_against)
                else:
                    response = "The {} lost to the {} on {}, {} to {}".format(
                        args['team'], opp, args['day'], runs, runs_against)
            else:
                response = "Could not find information about that game at this\
time"
            say(response)
        elif label == "record":
            current_year = datetime.utcnow().date().year
            dataframe = schedule_and_record(
                current_year, self.helper.baseball_teams_to_abbrev[args])
            record = self.helper.dataframe_last_non_nan(dataframe)
            if record == "":
                say("Could not find information about that season at this\
time")
            else:
                wins, losses = record.split("-")
                response = "The {}\'s record this season is {} wins and {} \
losses".format(
                    args, wins, losses
                )
                say(response)
        else:
            return False
        return True
