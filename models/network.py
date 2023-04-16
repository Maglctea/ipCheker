from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()
engine = create_engine('sqlite:///../ipChecker.sqlite', echo=False)
session = sessionmaker(bind=engine)
s: Session = session()

class Network(Base):
    __tablename__ = 'network'

    # id_network = Column(Integer, primary_key=True)
    name_network = Column(String(25))
    address_network = Column(String(25), primary_key=True)
    description_network = Column(Text, nullable=True)

    def __str__(self):
        return self.address_network

    @staticmethod
    def add(name_network, address_network, description_network):
        network = Network(name_network=name_network, address_network=address_network, description_network=description_network)
        s.add(network)
        s.commit()
        return network

    @staticmethod
    def get(address_network, many=False):
        if address_network == '*':
            return s.query(Network).all()
        if many:
            return s.query(Network).filter_by(address_network=address_network).all()
        else:
            return s.query(Network).filter_by(address_network=address_network).first()

Base.metadata.create_all(engine)
# Network.add('name', '127.0.0.2', 'description') # Добавит ip в бд

# print(Network.get('127.0.0.1')) # Получение сети из бд по ip
# print(Network.get('*', True)) # Получение всех сетей из бд
