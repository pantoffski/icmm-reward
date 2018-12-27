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
        c.execute("""CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teamName TEXT NOT NULL UNIQUE,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")
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
    def insertTeam(cls, teamName):
        team = [teamName]
        c = cls.DB_CONN.cursor()
        c.execute("INSERT INTO teams (teamName) VALUES (?)", team)
        rows = c.fetchall()
        return rows

    @classmethod
    def getTeamById(cls, teamId):
        values = [teamId]
        c = cls.DB_CONN.cursor()
        c.execute("""SELECT id, teamName, timestamp
            FROM teams
            WHERE id = ?""", values)
        row = c.fetchone()
        return row

    @classmethod
    def getTeamByTeamName(cls, teamName):
        values = [teamName]
        c = cls.DB_CONN.cursor()
        c.execute("""SELECT id, teamName, timestamp
            FROM teams
            WHERE teamName = ?""", values)
        rows = c.fetchone()
        return rows

    @classmethod
    def getUsersWithTeam(cls):
        # returned format : [firstname, lastname, teamId, first10k, teamName, timestamp]
        c = cls.DB_CONN.cursor()
        c.execute("""SELECT users.firstname, users.lastname, users.teamId, users.first10k,
            teams.teamName, teams.timestamp
            FROM users JOIN teams on users.teamId = teams.id
            ORDER BY teams.timestamp""")
        rows = c.fetchall()
        return rows

    @classmethod
    def getUserByName(cls, firstname, lastname):
        c = cls.DB_CONN.cursor()
        values = (firstname, lastname)
        c.execute("SELECT firstname, lastname, teamId, first10k FROM users WHERE (firstname = ? AND lastname = ?)", values)
        rows = c.fetchall()
        return rows

    @classmethod
    def insertUser(cls, firstname, lastname, teamId, first10k):
        user = [firstname, lastname, teamId, first10k]
        c = cls.DB_CONN.cursor()
        c.execute("INSERT INTO users VALUES (?,?,?,?)", user)
        cls.DB_CONN.commit()

    @classmethod
    def insertUsers(cls, users):
        c = cls.DB_CONN.cursor()
        for user in users:
            # user is [firstname, lastname, teamId, first10k]
            c.execute("INSERT INTO users VALUES (?,?,?,?)", user)
        cls.DB_CONN.commit()

    @classmethod
    def updateTeamByUser(cls, teamId, firstname, lastname):
        values = [teamId, firstname, lastname]
        c = cls.DB_CONN.cursor()
        c.execute("""UPDATE users SET teamId=? WHERE firstname=? AND lastname=?""", values)
        cls.DB_CONN.commit()

    @classmethod
    def checkTeam(cls, teamName, user1, user2, user3, user4):
        userList = [(user1["firstname"],user1["lastname"]) , (user2["firstname"],user2["lastname"]) ,
                    (user3["firstname"],user3["lastname"]) , (user4["firstname"],user4["lastname"])]

        data = {"member1": "notInit", "member2": "notInit", "member3": "notInit", "member4": "notInit"}

        c = cls.DB_CONN.cursor()

        # Check if teamName exists.
        team = UserDB.getTeamByTeamName(teamName)
        if team is not None:
            data["teamName"] = ResMessage.DUP_TEAM_NAME
        else:
            data["teamName"] = ResMessage.OK

        userSet = set()
        userNotFirst10k = []

        for index in range(0,4):
            if userList[index][0] == "" or userList[index][1] == "":
                setMsgData(data, index, ResMessage.EMPTY_FIELD)
                continue
            if userList[index] in userSet:
                setMsgData(data, index, ResMessage.DUP_USER)
                continue
            userSet.add(userList[index])

            all_data = UserDB.getUserByName(userList[index][0], userList[index][1])

            if len(all_data) == 0:
                setMsgData(data, index, ResMessage.USER_NOT_FOUND)
                continue

            if len(all_data) > 1:
                print("Error: found duplicate data in database %s %s" % (userList[index][0], userList[index][1]))
                assert(0)

            firstname = all_data[0][0]
            lastname = all_data[0][1]
            team = all_data[0][2]
            isFirst10k = all_data[0][3]

            if not(team == "" or team == None):
                setMsgData(data, index, ResMessage.USER_REGISTERED)
                continue

            if isFirst10k == 0:
                userNotFirst10k.append(index)

            setMsgData(data, index, ResMessage.OK)

        # Not enough first10k
        if len(userNotFirst10k) > 3:
            for index in userNotFirst10k:
                setMsgData(data, index, ResMessage.NOT_FIRST_10K)

        if all([data["teamName"] == ResMessage.OK,
        data["member1"] == ResMessage.OK,
        data["member2"] == ResMessage.OK,
        data["member3"] == ResMessage.OK,
        data["member4"] == ResMessage.OK]):
            data["success"] = True
        else:
            data["success"] = False

        return data
