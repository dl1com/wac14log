
import re
from datetime import date
from dbhandler import DBHandler
import jsonhandler

class ContestLib:
    def __init__(self, filename):
        self.ci = jsonhandler.read_contest_info(filename)
        self.dbh = DBHandler("data/contest.sqlite")

    def get_contestname(self) -> str:
        return self.ci["contestname"]

    def get_description(self) -> str:
        return self.ci["description"]

    def get_bands(self):
        band_list = []
        for band in self.ci["bands"]:
            band_list.append(band["name"])
        return band_list

    def get_callsigns(self):
        call_list = []
        for call in self.ci["callsigns"]:
            call_list.append(call["name"])
        return call_list

    def is_callsign(self, call) -> bool:
        res = re.search("[a-zA-Z0-9]{1,3}[0-9][a-zA-Z0-9]{0,3}[a-zA-Z]", call)
        if res is None:
            print(call + " is no callsign")
            return False
        print(call + " is a callsign")
        return True

    def submit_entry(self,
                     qso_date: date,
                     participant: str,
                     callsign: str,
                     bands: list[str]):

        if self.is_callsign(participant) is False:
            return "Bitte Rufzeichen überprüfen"
        if bands == []:
            return "Bitte mindestens ein Band/Special auswählen"
        
        # Make Call all caps
        participant = participant.upper()
        callsign = callsign.upper()

        for band in bands:
            self.dbh.store_entry(qso_date, participant, callsign, band)

    def get_score_table_all(self):
        participants = (self.dbh.get_participants())
        scores = []

        for p in participants:
            scores.append(self.get_score(p))

        return {'Call': participants, 'Punkte': scores}

    def get_score_table(self, p: str):
        entries = (self.dbh.get_entries_of_participant(p))
        dates = []
        calls = []
        bands = []
        points = []
        for e in entries:
            call = e[2]
            band = e[3]

            band_points = self.get_points_for_band(band)
            call_points = self.get_points_for_call(call)
            qso_points = max(band_points, call_points)

            # Find occurences of this call in table so far
            call_indices = []
            for i in range(len(calls)):
                if calls[i] == call:
                    call_indices.append(i)
            # Find duplicates of band for this call
            for i in call_indices:
                if bands[i] == band:
                    # Band already counted, no additional points
                    qso_points = 0

            dates.append(e[0].date())
            calls.append(call)
            bands.append(band)
            points.append(qso_points)
        return {'Datum': dates, 'Call': calls,
                'Band/Special': bands, 'Punkte': points}

    def get_score(self, p: str) -> int:
        table = self.get_score_table(p)
        score = 0
        for p in table["Punkte"]:
            score += p
        return score

    def get_participants(self) -> list[str]:
        participants = (self.dbh.get_participants())
        return participants

    def get_points_for_band(self, b: str) -> int:
        # TODO Optimize (use dict for band-> point relation)
        for band in self.ci["bands"]:
            if b == band["name"]:
                return int(band["points"])
        return 0

    def get_points_for_call(self, c: str) -> int:
        # TODO Optimize (use dict for call-> point relation)
        for call in self.ci["callsigns"]:
            if c == call["name"]:
                return int(call["points"])
        return 0       
