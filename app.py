#https://www.youtube.com/watch?v=hbDRTZarMUw&ab_channel=Codemy.com

from cv2 import AsyncArray
from flask import Flask, render_template, Response, request, redirect
from camera import Video
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
equation=''

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///equations.db'
db = SQLAlchemy(app)

#db model
class EquationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String(2), nullable=False)

    #function to return string when we add
    def __repr__(self):
        return '<Name %r>' % self.id

@app.route('/',methods = ["GET","POST"])
def index():

    return render_template('index.html', eqn=equation)

def gen(camera):
    while True:
        frame,gesture=camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + 
        b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/enter', methods=["POST"])
def enter():

    if request.method == "POST":

        frame,gesture=Video().get_frame()
        new_gesture = EquationData(character = gesture)


        #push to db
        try:
            db.session.add(new_gesture)
            db.session.commit()
            return redirect('/')
        except:
            return "error"
            
    else:
        characters = EquationData.query.order_by(EquationData.id)
        return render_template('index.html', characters = characters)

@app.route('/clear', methods=["POST"])
def clear():
    equation=''
    return render_template('index.html', eqn=equation)

if __name__ == "__main__":
    app.run(debug=True)