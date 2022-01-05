from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from extviews import PymongoConnection, MotorConnection, CrudViewSet, BaseCrudSet

app = FastAPI()

conn = PymongoConnection()
conn2 = MotorConnection()

#------------------------------------------------------------------------------ MODEL
class User(BaseModel):
    id: int
    name: str
    age: int

#------------------------------------------------------------------------------ CRUD SET
class UserCrudSet(BaseCrudSet):
    # db = conn.get_db()
    db = conn2.get_db()
    
    async def list(self):
        users = []
        async for u in  self.db.users.find():
            users.append(User(**u))
        print(users)
        return users
    
    async def create(self, data: User):
        await self.db.users.insert_one(data.dict())
        return data

#------------------------------------------------------------------------------ VIEW SET
class UserCrudViewSet(CrudViewSet):
    base_path = '/users'
    class_tag = 'user'
    crud = UserCrudSet
    model = User
    
    async_db = True
    
    @classmethod
    def get_response_model(cls, action: str) -> BaseModel :
        if action == 'list':
            return List[User]
        return User


app.include_router(UserCrudViewSet())


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8001 ,reload=True, workers=4, )

