from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "Tyler"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)



responses = []


@app.route('/')
def survey_start():
    """Root and start of survey"""
    return render_template("survey_start.html", survey=survey)

app.route('/start', methods=["POST"])
def start_quest():
    
    return redirect("/questions/0")

@app.route('/answer', methods=["POST"])
def show_answers():

    choice = request.form["answer"]
    responses.append(choice)

@app.route('/questions/<int:idx>')
def show_question(idx):
    "Show questions"
    question = survey.questions[idx]
    return render_template('questions.html', idx = idx, question = question)




