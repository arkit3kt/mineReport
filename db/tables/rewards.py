from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    BigInteger,
    Boolean
)
from main import Base

class Rewards(Base):
    __tablename__ = 'rewards'
    id = Column(Integer, primary_key=True)
    blockheight = Column(Integer, default=0)
    timestamp = Column(BigInteger, default=0)  # nullable=False,) #unique=True)
    reward = Column(BigInteger, default=0)
    percent = Column(Float, default=0)
    immature = Column(Boolean, default=0)
    currentLuck = Column(Float, default=0)
    orphan = Column(Boolean, default=0)
    uncle = Column(Boolean, default=0)

    def __repr__(self):
        return f"<rewards(id={self.id}, blockheight={self.blockheight}, reward={self.reward})>"

class RewardSums(Base):
    __tablename__ = 'reward_sums'
    id = Column(Integer, primary_key=True)
    interval = Column(BigInteger, default=0)
    reward = Column(BigInteger, default=0)
    numreward = Column(BigInteger, default=0)
    name = Column(String, default="")
    offset = Column(BigInteger, default=0)
    def __repr__(self):
        return f"<reward_sums(id={self.id}, interval={self.interval} reward={self.reward}, numreward={self.numreward})>"