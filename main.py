from fastapi import FastAPI

from database import Base, engine
from routers import users_router, vehicles_router

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(users_router, prefix="/api")
app.include_router(vehicles_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "woi"}
