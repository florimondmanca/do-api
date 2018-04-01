"""Database definition and setup."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Boolean


Base = declarative_base()
DB_NAME = 'sqlite:///do.db'


class List(Base):
    __tablename__ = 'list'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    tasks = relationship('Task')

    @property
    def serialized(self):
        return {
            'id': self.id,
            'title': self.title,
            'tasks': [task.serialized for task in self.tasks]
        }


class Task(Base):
    """
    {
        'id': 0,
        'list_id': 1,
        'title': 'Buy grosseries',
        'due_date': falcon.dt_to_http(
            datetime.now() + timedelta(days=1)),
        'completed': False,
        'priority': 2,
    },
    """
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    due_date = Column(TIMESTAMP(timezone=True), nullable=True)
    completed = Column(Boolean)
    priority = Column(Integer)
    list_id = Column(Integer, ForeignKey('list.id'))
    list = relationship(List)

    @property
    def serialized(self):
        return {
            'id': self.id,
            'list_id': self.list_id,
            'title': self.title,
            'due_date': str(self.due_date),
            'completed': self.completed,
            'priority': self.priority,
        }
