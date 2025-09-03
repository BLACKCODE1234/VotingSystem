import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash

from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with your secret key

# File paths for JSON data files
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CANDIDATE_FILE = os.path.join(BASE_DIR, 'candidate.json')
VOTES_FILE = os.path.join(BASE_DIR, 'votes.json')
STUDENTS_FILE = os.path.join(BASE_DIR, 'students.json')


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


class VoteForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    candidate = RadioField('Candidates', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit Vote')


@app.route('/')
def home():
    candidates = load_json(CANDIDATE_FILE)
    return render_template('home.html', candidates=candidates)


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    candidates = load_json(CANDIDATE_FILE)
    form = VoteForm()
    # Populate the radio field choices
    form.candidate.choices = [(c['id'], c['name']) for c in candidates]

    if form.validate_on_submit():
        student_id = form.student_id.data.strip()
        candidate_id = form.candidate.data

        # Validate student exists
        students = load_json(STUDENTS_FILE)
        if not any(s['id'] == student_id for s in students):
            flash("Invalid Student ID. Please enter a valid Student ID.", "danger")
            return redirect(url_for('vote'))

        # Check if student already voted
        votes = load_json(VOTES_FILE)
        if any(v['student_id'] == student_id for v in votes):
            flash("You have already voted. Multiple voting is not allowed.", "warning")
            return redirect(url_for('vote'))

        # Record the vote
        votes.append({"student_id": student_id, "candidate_id": candidate_id})
        save_json(VOTES_FILE, votes)

        flash("Thank you for voting!", "success")
        return redirect(url_for('results'))

    return render_template('page2.html', form=form)


@app.route('/results')
def results():
    candidates = load_json(CANDIDATE_FILE)
    votes = load_json(VOTES_FILE)

    # Count votes
    counts = {c['id']: 0 for c in candidates}
    for v in votes:
        print(counts)
        print(v['candidate_id'])
        if v['candidate_id'] in counts:
            counts[v['candidate_id']] += 1

    results = []
    for c in candidates:
        results.append({'name': c['name'], 'votes': counts[c['id']]})

    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
