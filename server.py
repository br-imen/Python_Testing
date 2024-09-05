import json
from datetime import datetime
from flask import (Flask, render_template, request,
                   redirect, flash, url_for, session)

app = Flask(__name__)
app.secret_key = "something_special"
app.config["CLUB_FILE"] = "clubs.json"
app.config["COMPETITIONS_FILE"] = "competitions.json"


def loadClubs():
    with open(app.config["CLUB_FILE"]) as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open(app.config["COMPETITIONS_FILE"], "r") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


def get_club_from_email(email):
    try:
        club = [club for club in clubs if club["email"] == email][0]
        return club
    except IndexError:
        return None


@app.route("/showSummary", methods=["POST", "GET"])
def showSummary():
    if request.method == "POST":
        club = get_club_from_email(request.form["email"])
        if club:
            session["club_email"] = club["email"]
            return render_template(
                "welcome.html", club=club, competitions=competitions
            )
        else:
            flash("Sorry, that email wasn't found.")
            return redirect(url_for("index"))
    else:
        if session:
            club = [
                club for club in clubs if club["email"] == session["club_email"]
            ][0]
            return render_template(
                "welcome.html", club=club, competitions=competitions
            )
        else:
            flash("No session")
            return redirect(url_for("index"))


@app.route("/display-points")
def display_points():
    return render_template("display_points.html", clubs=clubs)


def validate_competition_date(competition):
    competition_date = datetime.strptime(
        competition["date"], "%Y-%m-%d %H:%M:%S"
    )
    if competition_date < datetime.now():
        return "This competition is already over. You cannot book a place."


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = get_club_from_name(club)
    foundCompetition = get_competition_from_name(competition)
    if not foundClub or not foundCompetition:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=club, competitions=competitions
        )
    error_message = validate_competition_date(foundCompetition)
    if error_message:
        flash(error_message)
        return render_template(
            "welcome.html", club=foundClub, competitions=competitions
        )
    return render_template(
        "booking.html", club=foundClub, competition=foundCompetition
    )


def get_competition_from_name(name):
    try:
        competition = [
            competition
            for competition in competitions
            if competition["name"] == name
        ][0]
        return competition
    except IndexError:
        return None


def get_club_from_name(name):
    try:
        club = [club for club in clubs if club["name"] == name][0]
        return club
    except IndexError:
        return None


def get_index_club(club):
    return clubs.index(club)


def check_places(places, club):
    if not places or int(places) < 1:
        return "Places required must be a positive integer"
    if int(places) > 12:
        return (
            "Places required must be a positive integer "
            "that does not exceed 12"
        )
    if int(places) > int(club["points"]):
        return "Places required exceed club's total points"


def take_places(places, club, competition):
    try:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - places
        )
        club["points"] = int(club["points"]) - places
        return True
    except Exception:
        return False


def update_clubs(club, index_club):
    try:
        with open(app.config["CLUB_FILE"], "w") as file_club:
            dict_clubs = {}
            clubs[index_club]["points"] = str(club["points"])
            dict_clubs["clubs"] = clubs
            json.dump(dict_clubs, file_club, indent=4)
        return True
    except FileNotFoundError:
        return False


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = get_competition_from_name(request.form["competition"])
    club = get_club_from_name(request.form["club"])
    error_message = check_places(request.form["places"], club)
    if error_message:
        flash(error_message)
        return redirect(
            url_for("book", competition=competition["name"], club=club["name"])
        )
    placesRequired = int(request.form["places"])
    if take_places(placesRequired, club, competition) and update_clubs(
        club, get_index_club(club)
    ):
        flash("Great-booking complete!")
        return render_template(
            "welcome.html", club=club, competitions=competitions
        )
    else:
        flash("Something went wrong-please try again")
        return redirect(
            url_for("book", competition=competition["name"], club=club["name"])
        )


@app.route("/logout")
def logout():
    if session:
        session.pop("club_email", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
