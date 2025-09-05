from flask import Flask,render_template,request,redirect,url_for,flash,session
import os 
import dotenv
from pymongo import MongoClient


app = Flask(__name__)

app.secret_key = 'your_secret_key'  


dotenv.load_dotenv()

mongodb_username = os.getenv("MONGODB_USERNAME", "default_username")
mongodb_password = os.getenv("MONGODB_PASSWORD", "default_password")
mongodb_url = os.getenv("MONGODB_url", "default_url")


try:
    client = MongoClient(mongodb_url)
    db = client[os.getenv("MONGODB_DATABASE", "default_db")]
    print("working")
except ValueError as e:
    print("not working")

users_col = db["users"]
students_col = db["students"]
candidates_col = db["candidates"]
votes_col = db["votes"]


def validate_login(student_id, password):
    user_doc = users_col.find_one()
    if not user_doc:
        return False
    for user in user_doc.get("userdetails", []):
        if user["student_id"] == student_id and user["password"] == password:
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
    flash("You have successfully voted👌.")
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
    
    data = get_vote_data()
    votes = data.get('votes',{})
    total_votes = data.get('total_votes',0)
    return render_template('adminview.html', votes=votes, total_votes=total_votes)





def get_vote_data():
    vote_doc = votes_col.find_one()
    if not vote_doc:
        vote_doc = {
            "votes": {"Alice": 0, "Bob": 0},
            "voted_users": [],
            "total_votes": 0
        }
        votes_col.insert_one(vote_doc)
    return vote_doc


def save_vote_data(data):
    votes_col.update_one({}, {"$set": {
    "votes": data["votes"],
    "voted_users": data["voted_users"],
    "total_votes": data["total_votes"]
}}, upsert=True)



def has_voted(student_id):
    data = get_vote_data()
    return student_id in data.get("voted_users", [])


def add_vote(student_id, candidate):
    data = get_vote_data()

    if has_voted(student_id):
        return False

    candidate = candidate.strip()
    if candidate not in data["votes"]:
        return False

    data["votes"][candidate] += 1
    data["total_votes"] += 1
    data["voted_users"].append(student_id)

    save_vote_data(data)
    return True





        
    
@app.route('/vote', methods=['POST'])
def vote():
    student_id = session.get('student_id')
    candidate = request.form.get('candidate')
    
    if not student_id:
        flash("You must log in first.")
        return redirect(url_for('home'))
    
    if has_voted(student_id):
        flash("Thank You👍")
        return redirect(url_for('logout'))

    elif add_vote(student_id, candidate):
        flash("Vote recorded successfully!")
        # return redirect(url_for('home'))
    else:
        flash("Error recording vote.")
        
    
    
    return redirect(url_for('logout'))
    

# if __name__ == '__main__':
#     app.run(host='0.0.0.0',debug=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)