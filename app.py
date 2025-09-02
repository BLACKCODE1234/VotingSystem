from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

votes_file = "votes.json"

# Load users from JSON
def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)['credentials']

# Load votes
def load_votes():
    with open(votes_file, 'r') as file:
        data = json.load(file)
        
        
    if 'votes' not in data:
        data['votes'] = 0
    if 'AVotes' not in data:
        data['AVotes'] = 0
    if 'BVotes' not in data:
        data['BVotes'] = 0
    # ensure Candidate C count exists
    if 'CVotes' not in data:
        data['CVotes'] = 0
    if 'voters_id' not in data:
        data['voters_id'] = []

    return data

# Save vote to JSON
def save_vote(student_id, candidate):
    votes = load_votes()
    # Check if user already voted
    if str(student_id) in [str(voter_id) for voter_id in votes.get('voters_id', [])]:
        flash('You have already voted.')
        return False  # Already voted

    # Add vote
    votes['votes'] += 1

    # Tally candidate-specific vote
    if candidate == 'Candidate A':
        votes['AVotes'] += 1
    elif candidate == 'Candidate B':
        votes['BVotes'] += 1
    elif candidate == 'Candidate C':
        # ensure key exists just in case
        if 'CVotes' not in votes:
            votes['CVotes'] = 0
        votes['CVotes'] += 1

    votes['voters_id'].append(student_id)  # this is to track who voted

    with open(votes_file, 'w') as file:   # save the votes to json file
        json.dump(votes, file, indent=4)
    return True

# Login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_id = request.form['student_id']
        input_password = request.form['password']

        users = load_users()

        for user in users:
            if str(user['student_id']) == input_id and user['password'] == input_password:
                return redirect(url_for('vote', student_id=input_id))

        flash('Invalid Student ID or Password.')
        return redirect(url_for('login'))

    return render_template('login.html')

# Voting page
@app.route('/vote/<student_id>', methods=['GET', 'POST'])
def vote(student_id):
    if request.method == 'POST':
        selected_candidate = request.form.get('candidate')
        if not selected_candidate:
            flash('Please select a candidate.')
            return redirect(url_for('vote', student_id=student_id))

        success = save_vote(student_id, selected_candidate)
        if success:
            flash('Your vote has been recorded. You have been logged out.')
            return redirect(url_for('login'))
        else:
            flash('You have already voted.')
            return redirect(url_for('vote', student_id=student_id))

    return render_template('vote.html', student_id=student_id)

# Dashboard (optional)
@app.route('/dashboard/<student_id>')
def dashboard(student_id):
    return render_template('dashboard.html', student_id=student_id)



# admin page

if __name__ == '__main__':
    app.run(debug=True)
