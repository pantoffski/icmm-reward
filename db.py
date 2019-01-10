import sqlite3

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
                firstName TEXT,
                lastName TEXT,
                bibName TEXT,
                challenge TEXT,
                raceCategory TEXT,
                telNumber TEXT,
                bibNumber TEXT,
                PRIMARY KEY (bibNumber)
            )""")
        cls.DB_CONN.commit()

    @classmethod
    def insertUser(cls, firstName, lastName, bibName, challenge, raceCategory, telNumber, bibNumber):
        # To be implemented
        user = [firstName, lastName, bibName, challenge, raceCategory, telNumber, bibNumber]
        c = cls.DB_CONN.cursor()
        c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?)", user)
        cls.DB_CONN.commit()

    @classmethod
    def getUser(cls, bibNumber):
        # To be implemented
        c = cls.DB_CONN.cursor()
        values = (bibNumber,)
        c.execute("SELECT firstName, lastName, challenge, raceCategory, telNumber, bibNumber FROM users WHERE (bibNumber = ?)", values)
        row = c.fetchone()
        if row == None:
            return None
        data = {"firstName": row[0],
                "lastName": row[1],
                "challenge": row[2],
                "raceCategory": row[3],
                "telNumber": row[4],
                "bibNumber": row[5]}
        return data
