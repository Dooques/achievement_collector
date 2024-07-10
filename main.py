from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQL_ALCHEMY_DATABASE_URI'] = os.environ.get('SQL_ALCHEMY_DATABASE_URI')
Bootstrap5(app)


@app.route('/')
def index():
    pass


if __name__ == '__main__':
    app.run(debug=True)
