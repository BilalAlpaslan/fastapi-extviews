
from pydantic import BaseModel


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


class GenericCrudSet(BaseCrudSet):
    """
    Generic CRUD set.

    base_path: str = None
    """
    model : BaseModel = None
    
    def __init__(self):
        assert self.model is not None, "model is not defined"
        super().__init__()
    
    def list(self):
        return {'message': 'Hello World generic crud list'}

    def retrieve(self, id : int):
        return {'message': f'Hello World {id}'}

    def create(self, data : dict):
        return {'message': f'Hello World create {data}'}

    def update(self, id : int, data : dict):
        return {'message': f'Hello World update {id}'}

    def partial_update(self, id : int, data : dict):
        return {'message': f'Hello World partial_update {id}'}

    def destroy(self, id : int):
        return  {'message': f'Hello World destroy {id}'}