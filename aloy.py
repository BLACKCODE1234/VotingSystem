from flask import Flask,render_template,request,redirect,url_for,flash,session
import json


app = Flask(__name__)

app.secret_key = 'your_secret_key'  

users = 'users.json'
VOTES_FILE = 'votes.json'

with open(users,'r') as f:
    users_data = json.load(f)
def validate_login(student_id,password):
    for user in users_data['userdetails']:
        if user['student_id'] == student_id and user['password'] == password:
            return user
    return False




@app.route('/',methods=['GET','POST'])
def home():
    # return render_template('home.html')
    if request.method == 'POST':
        student_id_raw = request.form.get('student_id') or session.get('student_id')
        # student_id_raw = request.form.get('student_id')

        password = request.form.get('password')
        print(student_id_raw)
        try:
            student_id = int(student_id_raw)
            
        except ValueError:
            flash("Student ID must be a number.")
            return redirect(url_for('home'))

        user = validate_login(student_id,password)
        if user:
            session['student_id'] = user['student_id']
            if user['student_id'] == 201 and user['password'] == "admin123":
                return redirect(url_for('admin_view'))
            return redirect(url_for('userview'))
        return render_template('home.html',error = "Invalid User id or Password")
    if request.method == 'GET':
        if 'student_id' in session:
            if session['student_id'] == 201:
                return redirect(url_for('admin_view'))
            return redirect(url_for('userview'))
    
        return render_template('home.html')



@app.route('/logout')
def logout():
    session.pop('student_id', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))



@app.route('/userview',)
def userview():
    return render_template('userview.html')


@app.route('/admin_view',)
def admin_view():
    # return render_template('adminview.html')
    student_id = session.get('student_id')
    if not student_id or student_id != 201:
        flash("Access denied. Admins only.")
        return redirect(url_for('home'))
    
    data = load_votes()
    votes = data['votes']
    total_votes = data['total_votes']
    return render_template('adminview.html', votes=votes, total_votes=total_votes)





def load_votes():
    with open(VOTES_FILE, 'r') as f:
        return json.load(f)
    

def has_votes(student_id):
    data = load_votes()
    return student_id in data.get('voted_users',[]) 


def save_votes(data):
    with open(VOTES_FILE,'w') as f:
        json.dump(data,f,indent=4)
        
      

def add_votes(student_id,candidate):
    data = load_votes()
    
    

        
    if student_id in data['voted_users']:
        return False
    
    candidate = candidate.strip()
    
    if candidate == 'Alice':
        data['votes']['Alice'] += 1
    if candidate == 'Bob':
        data['votes']['Bob'] += 1
        
    data['total_votes'] += 1
    data['voted_users'].append(student_id)
        
    save_votes(data)
    return True
        
        
    
@app.route('/vote', methods=['POST'])
def vote():
    student_id = session.get('student_id')
    candidate = request.form.get('candidate')
    
    if not student_id:
        flash("You must log in first.")
        return redirect(url_for('home'))
    
    if has_votes(student_id):
        flash("You have already voted.")
        return redirect(url_for('logout'))

    elif add_votes(student_id, candidate):
        flash("Vote recorded successfully!")
        # return redirect(url_for('home'))
    else:
        flash("Error recording vote.")
        
    
    
    return redirect(url_for('logout'))
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)