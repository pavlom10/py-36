import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DSN = 'postgresql://:@localhost:5432/vk_tinder'

engine = sq.create_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Search(Base):
    __tablename__ = 'search'

    id = sq.Column(sq.Integer, primary_key=True)
    owner_id = sq.Column(sq.Integer)
    user_id = sq.Column(sq.Integer)
    photos = sq.Column(sq.Text)
    date = sq.Column(sq.DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return f'<Search: ({self.id}): {self.owner_id} {self.user_id} {self.photos}>'

    def __repr__(self):
        return str(self)


def create_schema():
    Base.metadata.create_all(bind=engine)


# create_schema()
# session = Session()
