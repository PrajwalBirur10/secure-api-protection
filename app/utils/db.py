from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime

class ScanLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    time: str = Field(default_factory=lambda: str(datetime.now()))
    input: str
    result: str
    score: int

engine = create_engine("sqlite:///logs.db")
SQLModel.metadata.create_all(engine)

def save_log(input_text: str, result: str, score: int):
    with Session(engine) as session:
        log = ScanLog(input=input_text, result=result, score=score)
        session.add(log)
        session.commit()

def get_logs():
    with Session(engine) as session:
        return session.exec(select(ScanLog)).all()
