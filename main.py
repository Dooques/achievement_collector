import json

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from steam_api import SteamAPI
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


# db = SQLAlchemy(model_class=Base)
# db.init_app(app)

# steam_api = SteamAPI()
# user_game_data = steam_api.get_achievements()
# print(user_game_data)


@app.route('/')
def index():
    with open('game_data.json', 'r') as json_file:
        game_data = json.load(json_file)
        game_list = [game for game in game_data.values()]
        new_game_list = []
        achievement_dict = {}
        for game in game_list:
            new_game_list.append(game)
            if game['achievements'] is None:
                pass
            else:
                achievements = [achievement for achievement in game['achievements'].values()]
                achievement_dict[game['gameName']] = achievements[:3]
    return render_template('index.html', game_data=game_list, achievements=achievement_dict)


if __name__ == '__main__':
    app.run(debug=True)
