import Functions
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///C:\myenv\Edyoda_QuizProject\quizproj.db')
session = sessionmaker(engine)()

string = 'Quiz Project'
print(string.center(40, '-'))
username = input('Enter Username: ')
check_duplicate = session.query(models.User).filter_by(username=username).all()
if len(check_duplicate) == 0:
    admin = input('Are you an admin? (y/n): ')
    if admin.lower() == 'y':
        status = True
    else:
        status = False
    Functions.add_user(username, admin=status)
else:
    admin = input('Are you an admin? (y/n): ')
    if admin.lower() == 'y':
        print('1. Check Scores')
        print('2. Add questions')
        a = int(input('Enter Task: '))
        if a == 1:
            stud_name = input('Enter student name: ')
            Functions.checkscore(stud_name)
        else:
            Functions.add_question()
    else:
        string = 'Welcome to the quiz'
        print(string.center(40, '-'))
        print('Select your topic: ')
        topics = session.query(models.Topics.topic_name).all()
        topics_dict = {}
        for index, topic in enumerate(topics):
            print(index + 1, topic[0])
            topics_dict[index + 1] = topic[0]
        prompt = int(input('Select your topic: '))
        topic = topics_dict.get(prompt)
        Functions.displayquestion(topic, check_duplicate[0].userid)
