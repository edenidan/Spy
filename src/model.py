import random

class User:
    def __init__(self,name):
        self.__name=name

    def getName(self):
        return self.__name

    
class Room:
    def __init__(self,id):
        self.__members=[]
        self.__id=id

    def getId(self):
        return self.__id

    def addMember(self,user):
        if (not self.memberExists(user.getName())):
            self.__members.append(user)

    def getMembers(self):
        return self.__members

    def memberExists(self,username):
        for member in self.__members:
            if member.getName() == username:
                return True
        return False


rooms = {}# id : room

rooms['1234'] = Room('1234')

def __getRoomById(roomId):
    return rooms[roomId]

def enterGame(roomId,username):
    room = __getRoomById(roomId)
    if room == None:
        raise 'room not found'
    room.addMember(User(username))

def getMembers(roomId):
    return __getRoomById(roomId).getMembers()

def generateRoom(hostName):
    id = generateID()
    rooms[id] = Room(id)
    rooms[id].addMember(User(hostName))

def generateID():
    id = random.random() * 10000
    while str(id) in rooms:
        id = random.random() * 10000
    return id