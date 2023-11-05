from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import asc

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return"Index for Message Application"

@app.route('/messages', methods=['GET', 'POST'])
def messages():

    if request.method == 'GET':
        all_messages = []
        messages = Message.query.order_by(asc(Message.created_at)).all()
        for messege in messages:
            message_dict = messege.to_dict()
            all_messages.append(message_dict)

        response = make_response(
            all_messages,
            200
        )
        return response
    
    elif request.method == 'POST':
        new_message = Message(
            body=request.get_json()['body'],
            username=request.get_json()['username'],
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = make_response(
            jsonify(message_dict),
            201
        )

        return response 



@app.route('/messages/<int:id>', methods=['GET', 'PATCH'])
def messages_by_id(id):
    
    if request.method == 'GET':
        message = Message.query.filter(Message.id == id).first()
        message_dict = messages.to_dict()

        response = make_response(
            message_dict,
            200
        )
        return response
    elif request.method == 'PATCH':
        message = Message.query.filter(Message.id == id).first()
        for attr in request.get_json():
            setattr(message, attr, request.get_json(message))

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
            message_dict,
            200
        )

        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
