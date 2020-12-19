# user -> id, name, type, password
# questions -> id, topic, difficulty, ques, sol
# options -> id, qid, options
# score -> id, qid, user_id, sol, result

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, Column, Integer, String, Unicode,
                        Boolean, Text, DateTime)

engine = create_engine('sqlite:///C:\myenv\Edyoda_QuizProject\quizproj.db',
                       echo=False)
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    userid = Column(Integer, primary_key=True)
    username = Column(String)
    usertype = Column(Boolean)
    password = Column(Unicode)


class Topics(Base):
    __tablename__ = 'topics'
    topic_id = Column(Integer, primary_key=True)
    topic_name = Column(String)
    topic_isactive = Column(Boolean)


class Difficulty(Base):
    __tablename__ = 'difficulty'
    difficulty_id = Column(Integer, primary_key=True)
    difficulty_type = Column(String)
    difficulty_isactive = Column(Boolean)


class Questions(Base):
    __tablename__ = 'questions'
    ques_id = Column(Integer, primary_key=True)
    topic_id = Column(Integer)
    difficulty_id = Column(Integer)
    question = Column(Text)
    solution_id = Column(Integer)
    question_isactive = Column(Boolean)


class Solutions(Base):
    __tablename__ = 'solutions'
    sol_id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    solution = Column(Text)
    solution_isactive = Column(Boolean)


class Score(Base):
    __tablename__ = 'score'
    score_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    score = Column(Integer)
    date = Column(DateTime)


Base.metadata.create_all(bind=engine)
