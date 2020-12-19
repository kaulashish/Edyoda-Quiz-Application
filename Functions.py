#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 11:42:47 2020

@author: ashish
"""
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
import models
from datetime import datetime

engine = create_engine('sqlite:///C:\myenv\Edyoda_QuizProject\quizproj.db')
session = sessionmaker(engine)()


def get_max_id(table_name, column_name):
    max_id = session.query(table_name).order_by(column_name.desc()).first()
    return max_id


def add_user(user_name, admin=False):
    #Getting max id in the table
    id_max = get_max_id(models.User, models.User.userid)
    if id_max == None:
        id_max = 1
    else:
        id_max = id_max.userid + 1

    if admin == True:
        admin = 1
        password = input("Enter password for your account: ")
        #Preparing object to be added to the database
        user_obj = models.User(userid=id_max,
                               username=user_name,
                               usertype=admin,
                               password=password)

    else:
        admin = 0
        #Preparing object to be added to the database
        user_obj = models.User(userid=id_max,
                               username=user_name,
                               usertype=admin)

    session.add(user_obj)
    session.commit()
    print("User {} added successfully.".format(user_name))


def add_topics(topic_name):
    id_max = get_max_id(models.Topics, models.Topics.topic_id)
    if id_max == None:
        id_max = 1
    else:
        id_max = id_max.topic_id + 1

    topic_obj = models.Topics(topic_id=id_max,
                              topic_name=topic_name,
                              topic_isactive=1)
    session.add(topic_obj)
    session.commit()
    print("Topic {} added successfully".format(topic_name))


def add_difficulty(difficulty_name):
    id_max = get_max_id(models.Difficulty, models.Difficulty.difficulty_id)
    if id_max == None:
        id_max = 1
    else:
        id_max = id_max.difficulty_id + 1

    difficulty_obj = models.Difficulty(difficulty_id=id_max,
                                       difficulty_type=difficulty_name,
                                       difficulty_isactive=1)
    session.add(difficulty_obj)
    session.commit()
    print("Difficulty {} added successfully".format(difficulty_obj))


def add_question():
    question_topic = input("Enter question topic: ")
    q_dif = input("Enter question difficulty: ")
    question = input("Enter question: ")
    option = input("Enter options seperated by commas: ").strip().split(",")
    count = 1
    for op in option:
        print(count, ". ", op)
        count += 1

    sol = int(input("Enter solution for the question. Select number: "))

    # =============================================================================
    #     If topic does not exist, ask user if want to add to DB
    # =============================================================================
    topic_check = session.query(
        models.Topics).filter_by(topic_name=question_topic).all()
    if len(topic_check) == 0:
        conf = input(
            "Entered topic not found. Do you want to add it to the database (y/n)"
        )
        if conf.lower() == 'y':
            add_topics(question_topic)
        else:
            return "quit"

    difficulty_check = session.query(
        models.Difficulty).filter_by(difficulty_type=q_dif).all()
    if len(difficulty_check) == 0:
        conf = input(
            "Entered difficulty not found. Do you want to add it to the database (y/n)"
        )
        if conf.lower() == 'y':
            add_difficulty(q_dif)
        else:
            return "quit"

    #Now we need ID for topic, difficulty and options
    topic_id = session.query(
        models.Topics).filter_by(topic_name=question_topic).all()
    topic_id = topic_id[0].topic_id

    difficulty_id = session.query(
        models.Difficulty).filter_by(difficulty_type=q_dif).all()
    difficulty_id = difficulty_id[0].difficulty_id

    max_question_id = get_max_id(models.Questions, models.Questions.ques_id)
    if max_question_id == None:
        max_question_id = 1
    else:
        max_question_id = max_question_id.ques_id + 1

    # First we will load the options, then we will load the question since we need the id for correct option
    solution_dict = {}
    for index, op in enumerate(option):
        max_id = get_max_id(models.Solutions, models.Solutions.sol_id)
        if max_id == None:
            max_id = 1
        else:
            max_id = max_id.sol_id + 1

        solution_dict[index + 1] = max_id
        option_obj = models.Solutions(sol_id=max_id,
                                      question_id=max_question_id,
                                      solution=op,
                                      solution_isactive=1)
        session.add(option_obj)
        print("Loading option ", index + 1)
    session.commit()

    solution_id = solution_dict[sol]

    question_obj = models.Questions(ques_id=max_question_id,
                                    topic_id=topic_id,
                                    difficulty_id=difficulty_id,
                                    question=question,
                                    solution_id=solution_id,
                                    question_isactive=1)
    session.add(question_obj)
    session.commit()
    print("Question loaded successfully")


def displayquestion(topic, user_id):
    marks = 0
    topicid = session.query(models.Topics).filter_by(topic_name=topic).all()
    topicid = topicid[0].topic_id
    #filters out questions from Questions table
    questions = session.query(
        models.Questions).filter_by(topic_id=topicid).all()

    for ques in questions:
        print(ques.question)
        ques_id = ques.ques_id

        #filter out options for the question and print them.
        options = session.query(
            models.Solutions).filter_by(question_id=ques_id).all()
        if len(options) == 0:
            continue

        #create a option dict containing index of solution as key
        #and option as value
        option_dict = {}
        temp_dict = {}
        for index, option in enumerate(options):
            option_dict[index + 1] = option.solution
            temp_dict[option.solution] = option.sol_id
            print(index + 1, option.solution)
        user_sol = int(input('Enter your answer: '))
        if ques.solution_id == temp_dict[option_dict[user_sol]]:
            marks += 1
    addscore(user_id, marks)

    print('Your total score is: ', marks)


def addscore(user_id, score):
    id_max = get_max_id(models.Score, models.Score.score_id)
    if id_max == None:
        id_max = 1
    else:
        id_max = id_max.score_id + 1
    scoreobj = models.Score(score_id=id_max,
                            date=datetime.now(),
                            user_id=user_id,
                            score=score)
    session.add(scoreobj)
    session.commit()


def checkscore(username):
    user_id = session.query(models.User).filter_by(username=username).first()
    user_id = user_id.userid
    score_records = session.query(
        models.Score).filter_by(user_id=user_id).all()
    for row in score_records:
        print(f'{username} scored {row.score} on {row.date}')


session.close()
