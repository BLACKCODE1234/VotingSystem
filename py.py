users = 'users.json'
import json



with open(users,'r') as f:
    users_data = json.load(f)
    
    
def validate_login(student_id,password):
    for user in users_data['userdetails']:
        if user['student_id'] == student_id and user['password'] == password:
            return True
        
    return False




student_id =int(input('student_id: '))
password = input('password: ').strip()

if validate_login(student_id,password):
    print("Login Successful")
    if student_id == 123 and password == "admin123":
        print("This is the admin page")
else:
    print("Invalid User id or Password ")
