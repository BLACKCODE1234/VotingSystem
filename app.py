from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from JSON
def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)['credentials']

# Load votes
def load_votes():
    if not os.path.exists('votes.json'):
        with open('votes.json', 'w') as f:
            json.dump({"votes": []}, f)
    with open('votes.json', 'r') as file:
        return json.load(file)['votes']

# Save vote to JSON
def save_vote(student_id, candidate):
    votes = load_votes()
    # Check if user already voted
    for vote in votes:
        if vote['student_id'] == student_id:
            return False  # Already voted

    # Add vote
    votes.append({
        "student_id": student_id,
        "candidate": candidate
    })
    with open('votes.json', 'w') as file:
        json.dump({"votes": votes}, file, indent=4)
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
            return render_template('vote_confirmation.html', student_id=student_id, candidate=selected_candidate)
        else:
            flash('You have already voted.')
            return redirect(url_for('vote', student_id=student_id))

    return render_template('vote.html', student_id=student_id)

# Dashboard (optional)
@app.route('/dashboard/<student_id>')
def dashboard(student_id):
    return render_template('dashboard.html', student_id=student_id)

if __name__ == '__main__':
    app.run(debug=True)
