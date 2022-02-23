from fastapi import FastAPI
from pydantic import BaseModel

from extviews.connections import PymongoConnection
from extviews.crudset import PymongoCrudSet
from extviews import CrudViewSet

app = FastAPI()

conn = PymongoConnection()

#------------------------------------------------------------------------------
# Models
class User(BaseModel):
    id: int
    name: str
    age: int

#------------------------------------------------------------------------------
# CRUD SET

class UserCrudSet(PymongoCrudSet):
    connection = conn
    collection = "users"
    model = User

#------------------------------------------------------------------------------
# VIEW SET

class UserCrudViewSet(CrudViewSet):
    base_path = '/users'
    class_tag = 'user'
    crud = UserCrudSet
    model = User


app.include_router(UserCrudViewSet().router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8001 ,reload=True, workers=4, )

