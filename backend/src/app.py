from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/pythonmongo'
mongo = PyMongo(app)

db = mongo.db.users

@app.route('/users', methods=['GET'])
def create_user():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'password': doc['password'],
            'email': doc['email']
        })
    return jsonify(users)

@app.route('/users', methods=['POST'])
def get_users():
    id = db.insert({
        'name': request.json['name'],
        'password': request.json['password'],
        'email': request.json['email']
    })
    return jsonify(str(ObjectId(id)))

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.find_one({'_id': ObjectId(id)})
    return jsonify({
            '_id': str(ObjectId(user['_id'])),
            'name': user['name'],
            'password': user['password'],
            'email': user['email']
        })

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'User deleted'})

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'password': request.json['password'],
        'email': request.json['email']
    }})
    return jsonify({'message': 'User updated'})

if __name__ == "__main__":
    app.run(debug=True)