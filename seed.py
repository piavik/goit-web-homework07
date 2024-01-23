from datetime import datetime
from faker import Faker
from random import randint, sample, choice
from sqlalchemy.sql import text

import connect_postgres
from models import Group, Student, Lector, Subject, Score

NUMBER_OF_STUDENTS = 50
NUMBER_OF_GROUPS = 3
NUMBER_OF_SUBJECTS = 8
NUMBER_OF_LECTORS = 5
NUMBER_OF_SCORES = 20

faker = Faker()

def clear_table(table):
    session.execute(text(f'TRUNCATE TABLE {table} CASCADE'))
    session.commit()

def seed_groups(session, number):
    clear_table(Group.__tablename__)
    for _ in range(number):
        group = Group(
            name=faker.unique.word()
        )
        session.add(group)
    session.commit()

def seed_lectors(session, number):
    clear_table(Lector.__tablename__)
    for _ in range(number):
        lector = Lector(
            name=faker.unique.name()
        )
        session.add(lector)
    session.commit()

def seed_students(session, number):
    clear_table(Student.__tablename__)
    group_ids = session.query(Group.id).all()
    for _ in range(number):
        student = Student(
            name=faker.unique.name(),
            group_id=choice(group_ids)[0]
        )
        session.add(student)
    session.commit()

def seed_subjects(session, number):
    clear_table(Subject.__tablename__)
    with open('./subjects_list.txt', 'r') as fh:
        subjects_list = fh.read().split('\n')
    fake_subjects = sample(subjects_list, number)
    lector_ids = session.query(Lector.id).all()
    for subject_name in fake_subjects:
        subject = Subject(
            name=subject_name,
            lector_id=choice(lector_ids)[0]
        )
        session.add(subject)
    session.commit()

def seed_scores(session, number):
    clear_table(Score.__tablename__)
    student_ids = session.query(Student.id).all()
    subject_ids = session.query(Subject.id).all()

    study_end = datetime.now().date()
    offset = 0 if study_end.month <9 else 1
    study_start = datetime(datetime.now().year-offset, 9, 1).date()

    for _ in range(number):
        score = Score(
            score=randint(1, 12),
            score_date=faker.date_between(study_start, study_end),
            student_id=choice(student_ids)[0],
            subject_id=choice(subject_ids)[0]
        )
        session.add(score)
    session.commit()


def seed(session):
    seed_groups(session, NUMBER_OF_GROUPS)
    seed_lectors(session, NUMBER_OF_LECTORS)
    seed_students(session, NUMBER_OF_STUDENTS)
    seed_subjects(session, NUMBER_OF_SUBJECTS)
    seed_scores(session, NUMBER_OF_SCORES)


if __name__ == "__main__":
    session = connect_postgres.DBSession()
    seed(session)
    session.close()