import random
from uuid import uuid1 as uuid

class User:
    def __init__(self,name):
        self.__name=name

    def getName(self):
        return self.__name

    
class Room:
    def __init__(self,id):
        self.__members=[]
        self.__id=id
        self.__rconpass = uuid()

    def getId(self):
        return self.__id

    def addMember(self,user):
        if (not self.memberExists(user.getName())):
            self.__members.append(user)
        else:
            raise 'Member already exists.'

    def getMembers(self):
        return self.__members

    def memberExists(self,username):
        for member in self.__members:
            if member.getName() == username:
                return True
        return False

    def getRconpass(self):
        return self.__rconpass


rooms = {}# id : room

rooms['1234'] = Room('1234')

def __getRoomById(roomId):
    return rooms[roomId]

def enterGame(roomId,username):
    room = __getRoomById(roomId)
    if room == None:
        raise 'Room not found.'
    room.addMember(User(username))

def getMembers(roomId):
    return __getRoomById(roomId).getMembers()

def generateRoom(hostName):
    id = generateID()
    rooms[id] = Room(id)
    rooms[id].addMember(User(hostName))
    return rooms[id].getId(),rooms[id].getRconpass()

def generateID():
    id = int(random.random() * 100000)
    while str(id) in rooms:
        id = int(random.random() * 100000)
    return str(id)