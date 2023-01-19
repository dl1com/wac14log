import sqlite3
from datetime import date, datetime

class DBHandler:
    def __init__(self,filename):
        self.db = filename
        self.con = sqlite3.connect(self.db,
                                   detect_types=sqlite3.PARSE_DECLTYPES |
                                                sqlite3.PARSE_COLNAMES)
        self.cur = self.con.cursor()

        print("Connected to sqlite: " + filename)

        res = self.cur.execute("SELECT name FROM sqlite_master")
        if res.fetchone() is None:
            print("Created table")
            self.create_db()

    def __del__(self):
        self.con.close()

    def create_db(self):        
        self.cur.execute("""CREATE TABLE contest_entry(
                            date TIMESTAMP,
                            participant TEXT NOT NULL,
                            callsign TEXT NOT NULL,
                            band TEXT NOT NULL)
                            """)

    def store_entry(self, qso_date : date, participant : str, callsign : str, band : str):
        dt = datetime.combine(qso_date, datetime.min.time())
        data = [(dt, participant, callsign, band)]
        self.cur.executemany("INSERT INTO contest_entry VALUES (?,?,?,?)", data)
        self.con.commit()

    def get_participants(self) -> list[str]:
        res = self.cur.execute("SELECT DISTINCT participant FROM contest_entry")
        participants = []
        for p in res.fetchall():
            participants.append(p[0])
        return participants

    def get_entries_of_participant(self, participant):
        query = """SELECT * FROM contest_entry
                   WHERE participant == '{}'
                   """.format(participant)
        res = self.cur.execute(query)
        return res.fetchall()