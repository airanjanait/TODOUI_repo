from sqlalchemy import create_engine
from sqlalchemy.sql.sqltypes import Integer,VARCHAR
from sqlalchemy import Column
from sqlalchemy.orm import sessionmaker,declarative_base
import pymysql
from sqlalchemy import Integer,VARCHAR,ForeignKey


SQLALCHEMY_DATABASE_URL="mysql+pymysql://root@localhost/todoapi"
engine=create_engine(   
    SQLALCHEMY_DATABASE_URL,connect_args={}
)

Session=sessionmaker(bind=engine,autocommit=False, autoflush=False,)
session=Session()

Base=declarative_base()

#____________logininfo table_______________

class DBUser(Base):
    __tablename__='logininfo'
    id=Column(Integer,primary_key=True,index=True)
    Name=Column(VARCHAR(23))
    Email=Column(VARCHAR(23))
    Password=Column(VARCHAR(23))
    
#____________todo table_________________
    
class DBTask(Base):
    __tablename__='todo'
    ID=Column(Integer,primary_key=True,index=True)
    TaskName=Column(VARCHAR(23))
    StartDate=Column(VARCHAR(23))
    StartTime=Column(VARCHAR(23))
    DueDate=Column(VARCHAR(23))
    
#________________taskhistory table___________
    
class DBTaskHistory(Base):
    __tablename__='taskhistory'
    history_id=Column(Integer,primary_key=True,index=True)
    task_id = Column(Integer, ForeignKey('todo.ID'))
    taskname=Column(VARCHAR(23))
    startdate=Column(VARCHAR(23))
    duedate=Column(VARCHAR(23))
    
Base.metadata.create_all(engine)

    

def get_db():
    db=Session()
    try:
        yield db
    finally:
        print("done")


