from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger
)
from main import Base


class Payments(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    amount = Column(BigInteger, default=0)
    timestamp = Column(BigInteger, default=0)# nullable=False,) #unique=True)
    totalPayees = Column(Integer, default=0)
    tx = Column(String, default=0)



