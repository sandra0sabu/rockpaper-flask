from flask import Flask, render_template, request, redirect, url_for, session
import random
import os

app = Flask(__name__)
# Use an environment variable for production SECRET_KEY
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

CHOICES = ["rock", "paper", "scissors"]

def decide(player, comp):
    if player == comp:
        return "tie"
    wins = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }
    return "player" if wins[player] == comp else "computer"

@app.route("/", methods=["GET", "POST"])
def index():
    # initialize score in session if absent
    if "score" not in session:
        session["score"] = {"player": 0, "computer": 0, "ties": 0, "rounds": 0}

    result = None
    player_choice = None
    comp_choice = None

    if request.method == "POST":
        action = request.form.get("action")
        if action == "replay":
            # reset scores
            session.pop("score", None)
            return redirect(url_for("index"))

        player_choice = request.form.get("choice")
        if player_choice not in CHOICES:
            return redirect(url_for("index"))

        comp_choice = random.choice(CHOICES)
        outcome = decide(player_choice, comp_choice)

        session["score"]["rounds"] += 1
        if outcome == "player":
            session["score"]["player"] += 1
            result = f"You win! {player_choice.title()} beats {comp_choice.title()}."
        elif outcome == "computer":
            session["score"]["computer"] += 1
            result = f"You lose — {comp_choice.title()} beats {player_choice.title()}."
        else:
            session["score"]["ties"] += 1
            result = f"It's a tie — both chose {player_choice.title()}."

        # force session to save mutated dict
        session.modified = True

    return render_template("index.html",
                           result=result,
                           player_choice=player_choice,
                           comp_choice=comp_choice,
                           score=session["score"],
                           choices=CHOICES)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
