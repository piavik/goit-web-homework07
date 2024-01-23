
from sqlalchemy import select, func, desc
import connect_postgres
from models import Group, Student, Lector, Subject, Score
from random import choice

def select_1(number, *args):
    ''' Знайти 5 студентів із найбільшим середнім балом з усіх предметів.'''
    result = (
        session.query(
            Student.name.label("Student"), 
            func.round(func.avg(Score.score), 2).label("Average Score")
        )
        .select_from(Student)
        .join(Score) #, Student.id == Score.student_id)
        .group_by(Student.id)
        .order_by(func.avg(Score.score).desc())
        .limit(number)
        .all()
    )
    return result

def select_2(subject_id, *args):
    '''Знайти студента із найвищим середнім балом з певного предмета.'''
    result = (
        session.query(
            Subject.name.label("Subject"), 
            Student.name.label("Student"),
            func.round(func.avg(Score.score), 2).label("Average Score")
        )
        .select_from(Score)
        .join(Student) #, Score.student_id == Student.id) # not needed as relatoins are described in the model ?
        .join(Subject) #, Score.subject_id == Subject.id)
        .filter(Subject.id == subject_id)
        .group_by(Subject.id, Student.id)
        .first()
    )
    return result

def select_3(subject_id, *args):
    '''Знайти середній бал у групах з певного предмета.'''
    result = (
        session.query(
            Subject.name.label("Subject"), 
            func.round(func.avg(Score.score), 2).label("Average Score")
        )
        .select_from(Score)
        .join(Student) 
        .join(Subject)
        .filter(Subject.id == subject_id)
        .group_by(Subject.id)
        .first()
    )
    return result

def select_4(*args):
    '''Знайти середній бал на потоці (по всій таблиці оцінок).'''
    result = (
        session.query(
            func.round(func.avg(Score.score), 2).label("Average Total")
        )
        .select_from(Score)
        .first()
    )
    return result

def select_5(lector_id, *args):
    '''Знайти які курси читає певний викладач.'''
    result = (
        session.query(
            Lector.name.label("Lector"), 
            Subject.name.label("Subject"), 
        )
        .select_from(Lector)
        .join(Subject)
        .filter(Lector.id == lector_id)
        .group_by(Lector.id, Subject.id)
        .all()
    )
    return result

def select_6(group_id, *args):
    '''Знайти список студентів у певній групі.'''
    result = (
        session.query(
            Group.name.label("Group"),
            Student.name.label("Student")
        )
        .select_from(Student)
        .join(Group)
        .filter(Group.id == group_id)
        .group_by(Group.id, Student.id)
        .all()
    )
    return result

def select_7(group_id, subject_id, *args):
    '''Знайти оцінки студентів у окремій групі з певного предмета.'''
    result = (
        session.query(
            Group.name.label("Group"),
            Subject.name.label("Subject"),
            Score.score.label("Score")
        )
        .select_from(Student)
        .join(Score)
        .join(Subject)
        .join(Group)
        .filter(Group.id == group_id, Subject.id == subject_id)
        .group_by(Group.id, Subject.id)
        .all() 
    )
    return result


def main():
    for i in range(7, 8):
        # calling functions in a loop
        function_name = globals()['select_' + str(i)]
        result = function_name(*params[i])
        print('-'*20)
        print(f'{i}. {function_name.__doc__}')
        if result is None:
            print("Nothing found")
        else:
            for row in result:
                print(row)

    

if __name__ == "__main__":
    session = connect_postgres.DBSession()
    random_group = choice(session.query(Group.id).all())[0]
    random_student = choice(session.query(Student.id).all())[0]
    random_lector = choice(session.query(Lector.id).all())[0]
    random_subject = choice(session.query(Subject.id).all())[0]
    params = { 
        1: [5],                 # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
        2: [random_subject],    # Знайти студента із найвищим середнім балом з "певного" предмета.
        3: [random_subject],    # Знайти середній бал у групах з "певного" предмета.
        4: [],                  # Знайти середній бал на потоці (по всій таблиці оцінок).
        5: [random_lector],     # Знайти які курси читає "певний" викладач.
        6: [random_group],      # Знайти список студентів у "певній" групі.
        7: [random_group, random_subject],      # Знайти оцінки студентів у "окремій" групі з "певного" предмета.
        8: [random_lector],     # Знайти середній бал, який ставить "певний" викладач зі своїх предметів.
        9: [random_student],    # Знайти список курсів, які відвідує : студент.
        10: [random_student, random_lector]     # Список курсів, які "певному" студенту читає "певний" викладач.
    }
    main()
    session.close()
