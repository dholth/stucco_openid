from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from stucco_auth.tables import User, initialize as initialize_auth

Base = declarative_base()

class OpenID(Base):
    """Store the OpenIDs associated with each user. When an OpenID is
    provided, the application should log in the associated user."""
    
    __tablename__ = 'stucco_openid'
    association_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id), index=True)
    openid = Column(Unicode(256), nullable=False, index=True, unique=True)
    user = relationship(User, backref='openids')

    def __repr__(self):
        return 'openid:%r' % (self.openid,)

def initialize(session):
    Base.metadata.create_all(session.bind)

