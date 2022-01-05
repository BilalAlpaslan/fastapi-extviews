
from pydantic import BaseModel

from .connections import MotorConnection, PymongoConnection

__all__ = ['BaseCrudSet', 'ModelCrudSet', 'PymongoCrudSet', 'MotorCrudSet'] 

class BaseCrudSet(object):
    """ 
    Base class for CRUD operations.
    """
    def __init__(self) -> None:
        super().__init__()

    def list(self):
        assert False, "You must implement list method"

    def retrieve(self, id : int):
        assert False, "You must implement retrieve method"

    def create(self, data : dict):
        assert False, "You must implement create method"

    def update(self, id : int, data : dict):
        assert False, "You must implement update method"

    def partial_update(self, id : int, data : dict):
        assert False, "You must implement partial_update method"

    def destroy(self, id : int):
        assert False, "You must implement destroy method"


class ModelCrudSet(BaseCrudSet):
    """
    Generic CRUD set.

    model : BaseModel = None
    """
    model : BaseModel = None
    
    def __init__(self):
        assert self.model is not None, "model is not defined"
        super().__init__()


class PymongoCrudSet(ModelCrudSet):
    """MongoDB CRUD set.

    model : BaseModel = None
    connection : PymongoConnection = None
    collecttion: str = None
    """
    connection : PymongoConnection = None
    collecttion: str = None
    
    def __init__(self):
        assert self.connection is not None, "connenciton is not defined"
        if self.collecttion is None:
            self.collecttion = self.model.__name__.lower()
            
        self.db =  self.connection.get_db()
        self._collection = self.db[self.collecttion]
        super().__init__()

    def list(self):
        models=[]
        for _model in self._collection.find():
            models.append(self.model(**_model))
        return models

    def retrieve(self, id : int):
        _model = self._collection.find_one({'id': id})
        return self.model(**_model)

    def create(self, model : BaseModel):
        self._collection.insert_one(model.dict())
        return model

    def update(self, id : int, model : BaseModel):
        self._collection.update_one({'id': id}, {'$set': model.dict()})
        return model

    def partial_update(self, id : int, model : BaseModel):
        self._collection.update_one({'id': id}, {'$set': model.dict()})
        return model

    def destroy(self, id : int):
        self._collection.delete_one({'id': id})
        return {'message': f'destroy {id}'}


class MotorCrudSet(ModelCrudSet):
    
    
    # !: not implemented yet
    
    """MongoDB CRUD set.

    model : BaseModel = None
    collecttion: str = None
    """
    conn : MotorConnection = None
    collecttion: str = None
    
    async def __new__(cls):
        instance = super().__new__(cls)
        await instance.__init__()
        return instance
    
    async def __init__(self):
        assert self.conn is not None, "conn is not defined"
        if self.collecttion is None:
            self.collecttion = self.model.__name__.lower()
            
        self._conn = await self.conn.get_db_client()
        self._collection = self._conn["default"][self.collecttion]
        super().__init__()

    async def list(self):
        data = await self._collection.find_one()
        print(data)
        return self.model(**data)

    async def retrieve(self, id : int):
        return {'message': f'Hello World mongo {id}'}

    async def create(self, data : dict):
        return {'message': f'Hello World mongo create {data}'}

    async def update(self, id : int, data : dict):
        return {'message': f'Hello World mongo update {id}'}

    async def partial_update(self, id : int, data : dict):
        return {'message': f'Hello World mongo partial_update {id}'}

    async def destroy(self, id : int):
        return  {'message': f'Hello World mongo destroy {id}'}