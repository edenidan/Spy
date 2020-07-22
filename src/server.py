import model
from flask import Flask,render_template,request


app = Flask(__name__)

@app.route('/',methods=['GET'])
def homePage():
    return render_template('home.html')

@app.route('/join',methods=['POST'])
def join():
    roomId = request.form['roomId']
    return render_template('joinRoom.html',roomid=roomId)

@app.route('/enterroom',methods=['POST'])
def enterRoom():
    username = request.form['username']
    roomId = request.form['roomId']
    model.enterGame(roomId,username)
    members = model.getMembers(roomId)
    return render_template('room.html',username=username,members=members)
    
@app.route('/createroom',methods=['GET'])
def createRoom():
    return render_template('createRoom.html')
