from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import datetime, timedelta

DB_NAME = "todo.db"
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='empty')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return "<Task(id='%s', task='%s', deadline='%s')>" % (
            self.id, self.task, self.deadline)


class SqlSession:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{DB_NAME}?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def add_task(self, task, deadline):
        new_row = Table(task=task, deadline=deadline)
        self.session.add(new_row)
        self.session.commit()

    def get_tasks(self):
        return self.session.query(Table).order_by(Table.deadline).all()

    def get_todays_tasks(self):
        return self.session.query(Table).filter(Table.deadline == datetime.today().date()).all()

    def get_weeks_tasks(self):
        today = datetime.today().date()
        return self.session.query(Table).filter(Table.deadline.between(today, today + timedelta(days=7))). \
            order_by(Table.deadline).all()

    def get_all_tasks(self):
        return self.session.query(Table).order_by(Table.deadline).all()

    def get_missed_tasks(self):
        return self.session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()

    def delete_task(self, id_):
        self.session.query(Table).filter(Table.id == id_).delete()
        self.session.commit()
