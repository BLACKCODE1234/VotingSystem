import json

class VotingCli:
    def __init__(self):
        print("Voting CLI initialized")
        
    def login(self):
        with open('students.json','r') as f:
            data = json.load(f)
        try:
            input_id = int(input("Enter student ID: ") )   
       
            found = False
            for student in data['students']:
                if input_id == student['student_id']:
                    print("Student Details")
                    print("---------------")
                    for idx,value in student.items():
                        print(f"  {idx}: {value}")
                        found = True    
                        
            if not found:
                print("Login failed. Student not found.")
                
            print()
        except ValueError:
            print("Invalid input. Please enter a numeric student ID.")
            return None
            
            
    def vote(self):
        if self.login():
            print("Voting process started...")
            aspirants  = []            
            
    def menu(self):
        # self.login()
        self.vote()

if __name__ == '__main__':
    voting = VotingCli()
    voting.menu()