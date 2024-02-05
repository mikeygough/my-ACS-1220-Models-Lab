"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from books_app.models import Book, Author, Genre, User

# Import app and db from events_app package so that we can run app
from books_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route("/")
def homepage():
    users = User.query.all()
    return render_template("home.html", users=users)


@main.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username).one()
    favorite_books = user.favorite_books
    return render_template("profile.html", user=user, favorite_books=favorite_books)
