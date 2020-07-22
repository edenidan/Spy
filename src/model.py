import random
from uuid import uuid1
uuid = lambda : str(uuid1())

class User:
    def __init__(self,name,uId):
        self.__name=name
        self.__id = uId

    def getName(self):
        return self.__name

    def getId(self):
        return self.__id

    
class Room:
    def __init__(self,id):
        self.__members=[]
        self.__id=id
        self.__rconpass = uuid()

    def getId(self):
        return self.__id

    def addMember(self,user):
        if (not self.memberExists(user.getId())):
            self.__members.append(user)
        else:
            raise 'Member already exists.'

    def getMembers(self):
        return self.__members

    def memberExists(self,uId):
        for member in self.__members:
            if member.getId() == uId:
                return True
        return False

    

    def getRconpass(self):
        return self.__rconpass


rooms = {}# id : room

rooms['1234'] = Room('1234')

# get room by Id
def __getRoomById(roomId):
    return rooms[roomId]

# enter a waiting room 
def enterGame(roomId,username, uId):
    room = __getRoomById(roomId)
    if room is None:
        raise 'Room not found.'
    if not room.memberExists(uId):
        room.addMember(User(username, uId))

# list of members from room by Id
def getMembers(roomId):
    return __getRoomById(roomId).getMembers()

# creates a room with a unique Id
def generateRoom():
    id = generateID()
    rooms[id] = Room(id)
    return id,rooms[id].getRconpass()

# creates a unique 5 digit Id
def generateID():
    id = int(random.random() * 100000)
    while str(id) in rooms:
        id = int(random.random() * 100000)
    return str(id)

def correctRconpass(roomId,Rconpass):
    room = __getRoomById(roomId)
    if room is None:
        return False
    return room.getRconpass() == Rconpass