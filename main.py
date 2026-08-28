from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from routers.__init__ import users_router, vehicles_router

Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

app = FastAPI()

app.include_router(users_router, prefix="/api")
app.include_router(vehicles_router, prefix="/api")


@app.get("/")
def run():
    return {"message": "woi"}
