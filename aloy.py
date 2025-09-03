from flask import Flask,render_template,request,redirect,url_for,flash
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
        student_id = int(request.form.get('student_id'))
        password = request.form.get('password')

        user = validate_login(student_id,password)
        if user:
            if user['student_id'] == 201 and user['password'] == "admin123":
                return render_template('adminview.html')
            else:
                return render_template('userview.html')
        else:
            return render_template('home.html',error = "Invalid User id or Password")
    return render_template('home.html')




@app.route('/userview',)
def userview():
    return render_template('userview.html')


@app.route('/admin_view',)
def admin_view():
    return render_template('adminview.html')




def load_votes():
    with open(VOTES_FILE, 'r') as f:
        return json.load(f)
    
def save_votes(data):
    with open(VOTES_FILE,'w') as f:
        json.dump(data,f,indent=4)
        
    
def has_votes(student_id):
    data = load_votes()
    return student_id in data.get('voted_users',[])   

def add_votes(student_id):
    data = load_votes()
    
    
        
    if student_id in data['voted_users']:
        return False
    
    
    else:
        data['votes']['Alice '] += 1
        data['votes']['Bob '] += 1
        data['voted_users'].append(student_id)
        save_votes(data)
        return True
        
        
    
@app.route('/vote', methods=['POST'])
def vote():
    student_id = int(request.form.get('student_id'))
    candidate = request.form.get('candidate')
    
    if has_votes(student_id):
        flash("You have already voted.")
        return redirect(url_for('home'))

    if add_votes(student_id, candidate):
        flash("Vote recorded successfully!")
        return redirect(url_for('home'))
    else:
        return "Error recording vote."

if __name__ == '__main__':
    app.run(debug=True)