from fastapi import FastAPI

from api.user import UserViewSet

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


app.include_router(UserViewSet())

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8001 ,reload=True, workers=4, )
