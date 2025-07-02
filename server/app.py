#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Chatterbox API</h1>'

# GET all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    message_dicts = [m.to_dict() for m in messages]
    return make_response(jsonify(message_dicts), 200)

# POST a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    new_message = Message(
        body=data['body'],
        username=data['username']
    )

    db.session.add(new_message)
    db.session.commit()

    return make_response(jsonify(new_message.to_dict()), 201)

# PATCH or DELETE a message by id
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def update_or_delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return make_response({'error': 'Message not found'}, 404)

    if request.method == 'PATCH':
        data = request.get_json()
        if 'body' in data:
            message.body = data['body']
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response(jsonify({"message": "Deleted"}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)