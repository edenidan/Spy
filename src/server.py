import model
from flask import Flask,render_template,request


app = Flask(__name__)

@app.route('/',methods=['GET'])
def homePage():
    return render_template('home.html')

# returns name choose page
@app.route('/getjoinpage',methods=['POST'])
def join():
    roomId = request.form['roomId']
    # generating unique user Id (uuid)
    # this Id will be used to avoid member duplications 
    # on page refresh
    return render_template('joinRoom.html',roomid=roomId, uId= model.uuid())

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
    


@app.route('/room',methods=['POST'])
def room():
    # differenciate between admin and member
    return 'cool'

@app.route('/ping',methods=['POST'])
def ping():
    # differenciate between admin and member
    json = request.get_json()
    roomId = json['roomid']
    uId = json['userid']

    model.ping(roomId,uId)
    members = model.getMembers(roomId)
    return ','.join([m.getName() for m in members])