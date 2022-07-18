import os
from turtle import update
from flask import Flask, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from flask_migrate import Migrate
from marshmallow import Schema
from datetime import datetime

app = Flask(__name__)

USERNAME = os.getenv('POSTGRES_USERNAME')
PASSWORD = os.getenv('POSTGRES_PASS')
DB = 'Flask_Application'

URI = f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/{DB}"

app.config['SQLALCHEMY_DATABASE_URI'] = URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    published = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, title, content, created_date=None):
        self.title = title

        self.content = content
        if created_date is None:
            created_date = datetime.utcnow()
            updated_date = datetime.utcnow()
        self.created_date = created_date
        self.updated_date = updated_date

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
            'published': self.published
        }


class PostSchema(Schema):
    """
    Post serializer
    """
    class Meta:
        fields = ('id', 'title', 'content', 'created_date',
                  'updated_date', 'published')


posts_schema = PostSchema(many=True)
post_schema = PostSchema()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/posts", methods=['GET', 'POST'])
def single_post():
    if request.method == 'POST':
        if not create_post(request.form['title'], request.form['content']):
            abort(400)

    posts = get_posts()
    return jsonify({'posts': posts_schema.dump(posts)})


@app.route("/posts/<int:post_id>", methods=['GET', 'DELETE', 'PUT'])
def show_post(post_id):
    if request.method == 'DELETE':
        if delete_post(post_id):
            posts = get_posts()
            return jsonify({'posts': posts_schema.dump(posts)})
        else:
            abort(400)
    elif request.method == 'PUT':
        update_post(post_id, request.form['title'], request.form['content'])
        posts = get_posts(post_id)
        return jsonify({'posts': post_schema.dump(posts)})

    else:
        post = get_posts(post_id)
        return jsonify(post_schema.dump(post).data)


def update_post(post_id, title, content):
    try:
        post = get_posts(post_id)
        post.title = title
        post.content = content
        post.updated_date = datetime.utcnow()
        db.session.commit()
    except:
        abort(404)
        pass


def delete_post(post_id):
    try:
        Post.query.filter(Post.id == post_id).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def get_posts(post_id=None):
    if post_id:
        try:
            post = Post.query.filter(Post.id == post_id).one()
            return post
        except NoResultFound:
            abort(404)
    else:
        posts = Post.query.order_by(desc(Post.created_date))
        return posts


def create_post(title, content):
    try:
        post = Post(title, content)
        db.session.add(post)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404


if __name__ == "__main__":
    app.run(debug=True)
