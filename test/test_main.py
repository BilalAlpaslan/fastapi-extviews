from fastapi import FastAPI

from extviews import ViewSet, register


app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}


class UserViewSet(ViewSet):

    def retrieve(self, pk):
        print("retrieve")
    
    def extra_like(self, pk):
        print("extra_like")
        
register(UserViewSet)