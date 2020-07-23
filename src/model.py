import random
from uuid import uuid1
import time
import threading
uuid = lambda : str(uuid1())
getMillis = lambda : int(round(time.time() * 1000))
TIMEOUT = 5000

locationsFile = open('res/locations.txt')
locations = locationsFile.readlines()
locationsFile.close()

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

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
        self.__lastSeen = {}
        self.__roles = {}
        self.__id=id
        self.__rconpass = uuid()
        self.__hasStarted = False
        set_interval(self.timerHandler,TIMEOUT/1000)

    def isSpy(self,uId):
        return self.__roles[uId] == 1 

    def getLocation(self):
        return self.__chosenLocation


    def start(self):
        if self.__hasStarted == True:
            return
        self.__hasStarted = True
        spyIndex = random.randint(0,len(self.__members))
        self.__roles[self.__members[spyIndex].getId()] = 1
        self.__chosenLocation = locations[random.randint(0,len(locations))]
        print(self.__chosenLocation)
        

    def timerHandler(self):
        millis = getMillis()
        for uid in self.__lastSeen:
            if millis - self.__lastSeen[uid] > TIMEOUT:
                self.removeUser(uid)

    def removeUser(self,uid):
        #del self.__lastSeen[uid]
        try:
            print('removed ' + self.getUser(uid).getName())
            self.__members.remove(self.getUser(uid))
        except:
            pass


    def getUser(self,uid):
        for m in self.__members:
            if m.getId() == uid:
                return m
        return None
    
    def getStarted(self):
        return self.__hasStarted

    def getId(self):
        return self.__id

    def addMember(self,user):
        if (not self.memberExists(user.getId())):
            self.__members.append(user)
            self.__lastSeen[user.getId()] = getMillis()
            self.__roles[user.getId()] = 0
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
    
    def ping(self,uId):
        self.__lastSeen[uId] = getMillis()
        


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
    while str(id) in rooms or id < 10000:
        id = int(random.random() * 100000)
    return str(id)

def correctRconpass(roomId,Rconpass):
    room = __getRoomById(roomId)
    if room is None:
        return False
    return room.getRconpass() == Rconpass

def ping(roomId,userId):
    room = __getRoomById(roomId)
    if room is None:
        raise 'room doesnt exists'
    room.ping(userId)