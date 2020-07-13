from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:a04011972@localhost/parser_db'

db = SQLAlchemy(app)


class Team(db.Model):
    __tablename__ = 'Team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))


class League(db.Model):
    __tablename__ = 'League'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class Match(db.Model):
    __tablename__ = 'Match'
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    league_id = db.Column(db.String, db.ForeignKey('league.id'), nullable=True)
    key = db.Column(db.String(1024), nullable=True)
    value = db.Column(db.String(1024), nullable=True)

    league = db.relationship('League')
    teams = db.relationship('Team')



