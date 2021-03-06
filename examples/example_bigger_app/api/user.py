from typing import List
from fastapi import Depends

from extviews import ViewSet

from db.user import get_users
from depends.depends import verify_token
from models.user import User

class UserViewSet(ViewSet):
    base_path = '/users'
    # class_tag = 'user'
    # response_model = User
    # dependencies = [Depends(verify_token)]
    
    def get_response_model(action: str):
        if action == 'list':
            return List[User] # TODO: generic function for all actions
        
    def get_dependencies(action: str):
        if action in ["create", "update", "delete"]:
            return [Depends(verify_token)]
        return None
        
    def list(self): # TODO: if we use "self" can we remove this ? viewset ViewSet._register_route function
        return get_users()

    def retrieve(self, id: int):
        return {'message': f'Hello World {id}'}
    
    def create(self, user: User):
        return {'message': f'Hello World create {user.id}'}
    
    def update(self, id: int):
        return {'message': f'Hello World update {id}'}
    
    def delete(self, id: int):
        return {'message': f'Hello World delete {id}'}
