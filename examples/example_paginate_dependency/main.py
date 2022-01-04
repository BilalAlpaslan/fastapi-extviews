from typing import Sequence
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from extviews.connections import PymongoConnection
from extviews.crudset import PymongoCrudSet
from extviews.depends import pagination_depends
from extviews import CrudViewSet

app = FastAPI()

#------------------------------------------------------------------------------
# Models
class User(BaseModel):
    id: int
    name: str
    age: int

#------------------------------------------------------------------------------
# CRUD SET

class UserCrudSet(PymongoCrudSet):
    connection = PymongoConnection
    collection = "users"
    model = User
    
    def list(self, skip: int = 0, limit: int = 10) -> Sequence[User]:
        models = []
        for _model in self._collection.find().skip(skip).limit(limit):
            models.append(self.model(**_model))
        return models
            
#------------------------------------------------------------------------------
# VIEW SET

class UserCrudViewSet(CrudViewSet):
    base_path = '/users'
    class_tag = 'user'
    crud = UserCrudSet
    model = User
    
    @classmethod
    def get_dependencies(cls, action: str) -> Sequence[Depends]:
        if action in ['list']:
            return [pagination_depends(max_limit=10)]
        return None
    
    @classmethod
    def list(cls, skip: int = 0, limit: int = 10) -> Sequence[User]:
        return cls._crud.list(skip=skip, limit=limit)

app.include_router(UserCrudViewSet())


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8001 ,reload=True, workers=4, )

