import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

DATABASE_URL="postgresql://postgres:Aathini@localhost/fastapi"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


data = sqlalchemy.Table(
    "cars",
    metadata,
    sqlalchemy.Column("registration_no", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("car_name", sqlalchemy.String),
    sqlalchemy.Column("model", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Integer),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)

class Data(BaseModel):
    registration_no:str
    car_name:str
    model:str
    price:int

app = FastAPI(title="REST API using FastAPI PostgreSQL")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/api/cars/")
async def create_data(car: Data):
    data1 = data.insert().values(
            registration_no=car.registration_no,
            car_name=car.car_name,
            model=car.model,
            price=car.price
        )
    await database.execute(data1)
    return "Data Inserted"

@app.get("/api/cars/")
async def read_notes():
    data1 = data.select()
    return await database.fetch_all(data1)

@app.put("/api/cars/{registration_no}/", response_model=Data)
async def update_note(registration_no: str, updation: Data):
   data1 = data.update().where(data.c.registration_no == registration_no ).values(registration_no=updation.registration_no, car_name=updation.car_name,model=updation.model,price=updation.price)
   await database.execute(data1)
   return {**updation.dict(), "registration_no": registration_no}

@app.delete("/api/cars/{registration_no}/")
async def delete_note(registration_no: str):
    data1 = data.delete().where(data.c.registration_no ==registration_no)
    await database.execute(data1)
    return {"message": "car detail with registration_no: {} deleted successfully!".format(registration_no)}