"""Database definition and setup."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Boolean


Base = declarative_base()


class List(Base):
    __tablename__ = 'list'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    # cascade='all': list deleted => tasks deleted
    tasks = relationship('Task', cascade='all')
    archived = Column(Boolean, nullable=False, default=False)

    @property
    def serialized(self):
        return {
            **self.serialized_simple,
            'tasks': [task.serialized for task in self.tasks]
        }

    @property
    def serialized_simple(self):
        return {
            'id': self.id,
            'title': self.title,
            'archived': self.archived,
        }


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    due_date = Column(TIMESTAMP(timezone=True), nullable=True)
    completed = Column(Boolean, nullable=False, default=False)
    priority = Column(Integer, nullable=False, default=0)
    list_id = Column(Integer, ForeignKey('list.id'))
    list = relationship(List)

    @property
    def serialized(self):
        return {
            'id': self.id,
            'list_id': self.list_id,
            'title': self.title,
            'due_date': self.due_date and str(self.due_date) or None,
            'completed': self.completed,
            'priority': self.priority,
        }
