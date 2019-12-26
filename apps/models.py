from datetime import datetime
from exts import db

__author__ = 'litl'


class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship('BoardModel', backref='posts')
    author_id = db.Column(db.String(50), db.ForeignKey('front_user.id'), nullable=False)
    author = db.relationship('FrontUser', backref='posts')
    comment_num = db.Column(db.Integer, nullable=False, default=0)


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.String(50), db.ForeignKey('front_user.id'), nullable=False)
    post = db.relationship('PostModel', backref='comments')
    author = db.relationship('FrontUser', backref='comments')


class HighLight(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    post = db.relationship('PostModel', backref='highlight')


class ApiTestCase(db.Model):
    __tablename__ = 'api_test_case'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_name = db.Column(db.String(50), nullable=False)
    request_url = db.Column(db.String(200), nullable=False)
    request_data = db.Column(db.String(200), nullable=False)
    request_method = db.Column(db.String(10), nullable=False)
    request_expected_result = db.Column(db.String(200), nullable=False)
    request_result = db.Column(db.String(200), nullable=True, default='')
    operator = db.Column(db.String(200), nullable=False)
    request_return_result = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)



class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    api = db.relationship('Api', backref='project')


class Api(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False, unique=True)
    body = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))