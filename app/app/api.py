# app/api.py
from app import app
from app.models import User, Bmi, Kommentar
from flask import jsonify


@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(User.to_collection())
# @app.route('/api/users/<int:id>/followers', methods=['GET'])
# def get_followers(id):
#     user = User.query.get_or_404(id)
#     data = user.followers_to_collection()
#     return jsonify(data)

# @app.route('/api/users/<int:id>/followed', methods=['GET'])
# def get_followed(id):
#     user = User.query.get_or_404(id)
#     data = user.followed_to_collection()
#     return jsonify(data)

@app.route('/api/users/<int:id>/posts', methods=['GET'])
def get_posts(id):
    user = User.query.get_or_404(id)
    data = user.posts_to_collection()
    return jsonify(data)