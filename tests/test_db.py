import os
import sys
import inspect
CURRENT_DIR = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
# Include paths for module search
sys.path.insert(0, PARENT_DIR)

from constant import ResMessage
from db import UserDB

def testFail_DupUser(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["1"], users["3"], users["3"])
    print(data)
    assert(data["success"] == False)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.DUP_USER)
    assert(data["member3"] == ResMessage.OK)
    assert(data["member4"] == ResMessage.DUP_USER)

def testFail_DupUserAllFirst10k(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["2"], users["5"], users["5"])
    print(data)
    assert(data["success"] == False)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.OK)
    assert(data["member3"] == ResMessage.OK)
    assert(data["member4"] == ResMessage.DUP_USER)

def testFail_UserNotExist(users):
    notExistUser = {"firstname": "Z", "lastname": "Z"}
    data = UserDB.checkTeam("HelloWorld", users["1"], users["2"], notExistUser, users["4"])
    assert(data["success"] == False)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.OK)
    assert(data["member3"] == ResMessage.USER_NOT_FOUND)
    assert(data["member4"] == ResMessage.OK)

def testFail_AlreadyRegistered(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["2"], users["3"], users["7"])
    assert(data["success"] == False)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.OK)
    assert(data["member3"] == ResMessage.OK)
    assert(data["member4"] == ResMessage.USER_REGISTERED)

def testFail_AlreadyRegisteredAndThree10k(users):
    data = UserDB.checkTeam("HelloWorld", users["3"], users["4"], users["6"], users["7"])
    assert(data["success"] == False)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.OK)
    assert(data["member3"] == ResMessage.OK)
    assert(data["member4"] == ResMessage.USER_REGISTERED)

def testSuccess_TwoFirst10k(users):
    data = UserDB.checkTeam("MyNewTeam", users["1"], users["2"], users["3"], users["4"])
    assert(data["success"] == True)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.OK)
    assert(data["member3"] == ResMessage.OK)
    assert(data["member4"] == ResMessage.OK)

def testSuccess_SwapPosition(users):
    data = UserDB.checkTeam("HelloWorld", users["4"], users["3"], users["2"], users["1"])
    assert(data["success"] == True)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.OK)
    assert(data["member3"] == ResMessage.OK)
    assert(data["member4"] == ResMessage.OK)

def testSuccess_SwapPosition_2(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["3"], users["4"], users["2"])
    assert(data["success"] == True)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.OK)
    assert(data["member3"] == ResMessage.OK)
    assert(data["member4"] == ResMessage.OK)

def testSuccess_ThreeFirst10k(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["2"], users["3"], users["5"])
    assert(data["success"] == True)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.OK)
    assert(data["member3"] == ResMessage.OK)
    assert(data["member4"] == ResMessage.OK)

def testSuccess_OneFirst10k(users):
    data = UserDB.checkTeam("HelloWorld", users["3"], users["1"], users["4"], users["6"])
    assert(data["success"] == True)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.OK)
    assert(data["member3"] == ResMessage.OK)
    assert(data["member4"] == ResMessage.OK)

def testSuccess_AllFirst10k(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["2"], users["5"], users["8"])
    assert(data["success"] == True)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.OK)
    assert(data["member3"] == ResMessage.OK)
    assert(data["member4"] == ResMessage.OK)

def testFail_AllNotFirst10k(users):
    data = UserDB.checkTeam("HelloWorld", users["3"], users["4"], users["6"], users["9"])
    assert(data["success"] == False)
    assert(data["teamName"] == ResMessage.OK)
    assert(data["member1"] == ResMessage.NOT_FIRST_10K)
    assert(data["member2"] == ResMessage.NOT_FIRST_10K)
    assert(data["member3"] == ResMessage.NOT_FIRST_10K)
    assert(data["member4"] == ResMessage.NOT_FIRST_10K)

def testFail_DupTeam(users):
    data = UserDB.checkTeam("MyTeam", users["1"], users["2"], users["3"], users["4"])
    assert(data["success"] == False)
    assert(data["teamName"] == ResMessage.DUP_TEAM_NAME)
    assert(data["member1"] == ResMessage.OK)
    assert(data["member2"] == ResMessage.OK)
    assert(data["member3"] == ResMessage.OK)
    assert(data["member4"] == ResMessage.OK)
