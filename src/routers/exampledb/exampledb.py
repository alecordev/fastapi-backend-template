from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship
from typing import List, Optional

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


app = FastAPI()

SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/profiles/", response_model=List[Profile])
def read_profiles(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    profiles = session.exec(select(Profile).offset(skip).limit(limit)).all()
    return profiles


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
