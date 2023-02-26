from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from validation import Validation
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/b4rok/Documents/Playground/crud-flask-rest-api/data.db' #Change This to your directory in local
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))

    def json(self):
        return{'id': self.id,'username': self.username, 'email': self.email}

#Test Route
@app.route('/', methods=['GET'])
def index():
    return make_response(jsonify({'message': 'index routing'}), 200)

#Create User endpoint
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        register_validation = Validation.register_validation(data['username'], data['email'])
        if register_validation:
            new_user = User(username=data['username'], email=data['email'])
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({'message': 'user created'}), 200)
        else:
            return make_response(jsonify({'message': 'can not create user because invalid input'}), 422)
    except:
        return make_response(jsonify({'message':'error creating user'}), 500)

#Get all user endpoint
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify({'users': [user.json() for user in users]}), 200)
    except:
        return make_response(jsonify({'message': 'error getting user'}), 500)

#Get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'users': user.json()}), 200)
        return make_response(jsonify({'message': f'user with id {id} not found'}), 400)
    except:
        return make_response(jsonify({'message': 'error getting user'}), 500)

#Update User
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': f'user with id {id} updated'}), 200)
        return make_response(jsonify({'message': f'user with id {id} not found'}), 400)
    except:
        return make_response(jsonify({'message': 'error updating user'}), 500)

#Delete User by id
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': f'user with id {id} deleted'}), 200)
        return make_response(jsonify({'message': f'user with id {id} not found'}), 400)
    except:
        return make_response(jsonify({'message': 'error deleting user'}), 500)

if __name__ == "__main__":
    app.run(debug=True)
