from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from extviews import ViewSet


class UserViewSet(ViewSet):
    def list():
        return [{'message': 'Hello World'}]

    def retrieve(id):
        return {'message': f'Hello World {id}'}

class Product(BaseModel):
    id: int
    name: str
    
class ProductViewSet(ViewSet):
    base_path = '/products'
    class_tag = 'product'
    response_model = Product
    
    def list():
        return Product(id=1, name='John Doe')

    def retrieve(id):
        return Product(id=id, name='John Doe')

app = FastAPI()
app.include_router(UserViewSet())
app.include_router(ProductViewSet())

client = TestClient(app)



def test_base_viewset():
    assert UserViewSet.base_path == '/userviewset'
    assert UserViewSet.class_tag == 'UserViewSet'
    assert UserViewSet.response_model == None
    
def test_base_viewset_2():
    assert ProductViewSet.base_path == '/products'
    assert ProductViewSet.class_tag == 'product'
    assert ProductViewSet.response_model == Product

def test_base_viewset_list():
    response = client.get('/userviewset')
    assert response.status_code == 200
    assert response.json() == [{'message': 'Hello World'}]

def test_base_viewset_get():
    id = 1
    response = client.get(f'/userviewset/{id}')
    assert response.status_code == 200
    assert response.json() == {'message': f'Hello World {id}'}
    
def test_base_viewset_list_2():
    response = client.get('/products')
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'John Doe'}

def test_base_viewset_get_2():
    id = 1
    response = client.get(f'/products/{id}')
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'John Doe'}