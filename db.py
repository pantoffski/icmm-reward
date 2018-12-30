import sqlite3
from constant import ResMessage

def setMsgData(data, index, msg):
    if index == 0:
        key = "member1"
    elif index == 1:
        key = "member2"
    elif index == 2:
        key = "member3"
    elif index == 3:
        key = "member4"
    else:
        assert(0)
    data[key] = msg
    return data

class UserDB:
    """Singleton style database class"""
    DB_CONN = None

    @classmethod
    def connect(cls, db_path):
        if cls.DB_CONN is None:
            print("Connecting database: %s" % (db_path))
            cls.DB_CONN = sqlite3.connect(db_path)

    @classmethod
    def close(cls):
        if cls.DB_CONN:
            cls.DB_CONN.close()
            cls.DB_CONN = None

    @classmethod
    def initSchema(cls):
        print("Initialize database schema")
        c = cls.DB_CONN.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
                firstname TEXT,
                lastname TEXT,
                teamId INTEGER DEFAULT NULL,
                first10k INTEGER,
                PRIMARY KEY ('firstname', 'lastname'),
                FOREIGN KEY(teamId) REFERENCES teams(id)
            )""")
        cls.DB_CONN.commit()

    @classmethod
    def insertUser(cls, teamName):
        # To be implemented
        user = [firstname, lastname, teamId, first10k]
        c = cls.DB_CONN.cursor()
        c.execute("INSERT INTO users VALUES (?,?,?,?)", user)
        cls.DB_CONN.commit()

    @classmethod
    def getUser(cls, bibNumber):
        # To be implemented
        c = cls.DB_CONN.cursor()
        values = (bibNumber,)
        c.execute("SELECT firstName, lastName, challenge, raceCategory, telNumber, bibNumber, eRewardUrl FROM users WHERE (bibNumber = ?)", values)
        row = c.fetchone()
        if row == None:
            return None
        data = {"firstName": row[0],
                "lastName": row[1],
                "challenge": row[2],
                "raceCategory": row[3],
                "telNumber": row[4],
                "bibNumber": row[5],
                "eRewardUrl": row[6]}
        return data

    @classmethod
    def setERewardUrl(cls, bibNumber, eRewardUrl):
        try:
            c = cls.DB_CONN.cursor()
            values = (bibNumber, eRewardUrl)
            c.execute("UPDATE users WHERE bibNumber=? VALUES eRewardUrl=?", values)
            cls.DB_CONN.commit()
            return True
        except:
            return False
