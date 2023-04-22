from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "Tyler"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



RESPONSES_KEY = "responses"


@app.route('/')
def survey_start():
    """Root and start of survey"""
    return render_template("survey_start.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_quest():
    
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route('/answer', methods=["POST"])
def show_answers():
    """display answer choices and handle response on submit"""
    choice = request.form["answer"]

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:idx>')
def show_question(idx):
    """Show questions"""

    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != idx):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {idx}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[idx]
    return render_template('questions.html', idx = idx, question = question)

@app.route('/complete')
def complete_page():
    """Survey is complete page"""

    return render_template("complete.html")




