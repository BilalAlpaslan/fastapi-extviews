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
        
    def list(): # TODO: if we use "self" can we remove this ? viewset ViewSet._register_route function
        return get_users()

    def retrieve(id: int):
        return {'message': f'Hello World {id}'}
    
    def create(user: User):
        return {'message': f'Hello World create {user.id}'}
    
    def update(id: int):
        return {'message': f'Hello World update {id}'}
    
    def delete(id: int):
        return {'message': f'Hello World delete {id}'}

    @ViewSet.extra_method(methods=["POST"], path_key="/{id}/like")
    def like(id: int):
        return {'message': 'Hello World extra_method'}