import model
import click
from flask import Flask,render_template,request

app = Flask(__name__)
hacker_msg = 'YOU NO HACK!'

@app.route('/',methods=['GET'])
def homePage():
    return render_template('home.html')

# returns name choose page
@app.route('/getjoinpage',methods=['POST'])
def join():
    roomId = request.form['roomId']
    if model.roomExists(roomId):
        return render_template('joinRoom.html',roomid=roomId, uId= model.uuid())
    
    if roomId == '':
        return render_template('home.html')

    return render_template('home.html',error=True,errormessage='Room does not exist.')


# returns waiting room page
@app.route('/enterwaitingroom',methods=['POST'])
def enterRoom():
    username = request.form['username']
    roomId = request.form['roomId']
    uId = request.form['uId']
    Rconpass = request.form['rconpass']

    #if the client has the correct password he will have the start button on the waiting room
    admin = False
    if model.correctRconpass(roomId,Rconpass):
        admin=True

    model.enterGame(roomId,username, uId)
    members = model.getMembers(roomId)
    if(members is None):
        return hacker_msg
    return render_template('waitingRoom.html',isadmin=admin,rconpass = Rconpass,roomid = roomId ,username=username,userid=uId,members=members)


# returns create room page
@app.route('/getcreatepage',methods=['GET'])
def getCreatePage():
    return render_template('createRoom.html', uId = model.uuid())


# returns waiting room 
@app.route('/createroom',methods=['GET'])
def createRoom():
    roomId,rconpass = model.generateRoom()
    return roomId+','+ rconpass
    


@app.route('/startroom',methods=['POST'])
def startroom():
    roomId = request.form['roomid']
    userId = request.form['userid']
    username = request.form['username']
    rconpass = request.form['rconpass']

    room = model.__getRoomById(roomId)
    if room.getRconpass() != rconpass:
        return hacker_msg

    members = model.getMembers(roomId)
    if(members is None):
        return 
    room.start()

    IsSpy = room.isSpy(userId)
    if(IsSpy is None):
        return hacker_msg
    location = room.getLocation()
    return render_template('room.html',session = room.getSession(),isadmin=True,isspy=IsSpy,rconpass=rconpass, location = location,username=username, userid = userId, roomid=roomId, members=members)

@app.route('/getroom',methods=['POST'])
def getroom():
    roomId = request.form['roomid']
    userId = request.form['userid']
    username = request.form['username']
    Rconpass = request.form['rconpass']


    members = model.getMembers(roomId)
    if(members is None):
        return hacker_msg
    room = model.__getRoomById(roomId)
    if(room is None):
        return hacker_msg
    
    IsSpy = room.isSpy(userId)
    if(IsSpy is None):
        return hacker_msg 
    location = room.getLocation()

    return render_template('room.html',session = room.getSession(),isadmin=room.getRconpass()==Rconpass,rconpass=Rconpass , isspy=IsSpy, location = location,username=username, userid = userId, roomid=roomId, members=members)

@app.route('/ping',methods=['POST'])
def ping():
    # differenciate between admin and member
    json = request.get_json()
    roomId = json['roomid']
    uId = json['userid']
    generalInfo = json['general']

    room = model.__getRoomById(roomId)
    if(room is None):
        return hacker_msg
    hasStarted = room.getStarted()

    if(generalInfo == 'pass'):
        pass

    if(generalInfo == 'member&start'):
        model.ping(roomId,uId)
        members = model.getMembers(roomId)
        return ','.join([m.getName() for m in members]) + '&' + str(hasStarted)

    if(generalInfo == 'member&session'):
        model.ping(roomId,uId)
        members = model.getMembers(roomId)
        s = str(room.getSession())
        return ','.join([m.getName() for m in members]) + '&' + s
    
    
    return 'invalid request'


@app.route('/reroll',methods=['POST'])
def reroll():
    roomId = request.form['roomid']
    userId = request.form['userid']
    username = request.form['username']
    rconpass = request.form['rconpass']
    
    room = model.__getRoomById(roomId)
    if(room is None):
        return hacker_msg
    if room.getRconpass() != rconpass:
        return hacker_msg
    room.reroll()
    return 'Success'
