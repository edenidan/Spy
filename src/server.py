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

    model.enterGame(roomId,username, uId)
    members = model.getMembers(roomId)
    return render_template('waitingRoom.html',isadmin=False,roomid = roomId ,username=username,members=members)


# returns create room page
@app.route('/getcreatepage',methods=['GET'])
def getCreatePage():
    return render_template('createRoom.html', uId = model.uuid())


# returns waiting room 
@app.route('/createroom',methods=['POST'])
def createRoom():
    hostName = request.form['hostName']
    uId = request.form['uId']

    roomId,rconpass = model.generateRoom(hostName, uId)
    members = model.getMembers(roomId)

    return render_template('waitingRoom.html',isadmin=True, roomid = roomId,rconpass =rconpass ,username=hostName,members=members)


@app.route('/room',methods=['POST'])
def room():
    # differenciate between admin and member
    return 'cool'
