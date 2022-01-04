from typing import List

from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel

from extviews import ViewSet

app = FastAPI()


class User(BaseModel):
    id: int
    name: str

async def get_users():
    return [User(id=1, name='John Doe'), User(id=2, name='Jane Doe')]


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

@app.get('/')
async def root():
    return {'message': 'Hello World'}


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


app.include_router(UserViewSet())

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8001 ,reload=True, workers=4, )
