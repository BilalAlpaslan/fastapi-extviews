from typing import Callable, List, Sequence, Union
from fastapi import APIRouter, Header
from fastapi.params import Depends
from pydantic import BaseModel

from .crudset import BaseCrudSet

__all__ = ['ViewSet', 'CrudViewSet']

supported_methods_names: List[str] = [
    'list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']


class ViewSet:
    """ router: APIRouter = None
    base_path: str = None
    class_tag: str = None
    path_key: str = "id"
    response_model: BaseModel = None
    dependencies: Sequence[Depends] = None
    """
    router: APIRouter = None
    base_path: str = None
    class_tag: str = None
    path_key: str = "id"
    response_model: BaseModel = None
    dependencies: Sequence[Depends] = None

    def __init__(self) -> APIRouter:
        self.functions: List[Callable] = []
        self.extra_functions: List[List] = []

        self.execute()

    def get_response_model(self, action: str) -> Union[BaseModel, None]:
        """ if override this method, you can return different response model for different action """
        if self.response_model is not None:
            return self.response_model
        return None

    def get_dependencies(self, action: str) -> Sequence[Depends]:
        """ if override this method, you can return different dependencies for different action """
        if self.dependencies is not None:
            return self.dependencies
        return None

    def execute(self) -> APIRouter:

        if self.router is None:
            self.router = APIRouter()

        if self.base_path is None:
            self.base_path = '/' + self.__class__.__name__.lower()

        if self.class_tag is None:
            self.class_tag = self.__class__.__name__

        for func in supported_methods_names:
            if hasattr(self, func):
                self.functions.append(getattr(self, func))

        self.extra()

        for func in self.functions:
            self._register_route(func)

        for func, methods, path in self.extra_functions:
            self._register_extra_route(func, methods=methods, path=path)

    def _register_route(self, func: Callable, hidden_params: List[str] = ["self"]):

        # hidden_params TODO: add support for hidden params

        extras = {}
        extras['response_model'] = self.get_response_model(func.__name__)
        extras['dependencies'] = self.get_dependencies(func.__name__)

        if func.__name__ == 'list':
            self.router.add_api_route(self.base_path, func, tags=[
                                      self.class_tag], methods=['GET'], **extras)
        elif func.__name__ == 'retrieve':
            self.router.add_api_route(f"{self.base_path}/\u007b{self.path_key}\u007d", func, tags=[
                                      self.class_tag], methods=['GET'], **extras)
        elif func.__name__ == 'create':
            self.router.add_api_route(self.base_path, func, tags=[
                                      self.class_tag], methods=['POST'], **extras)
        elif func.__name__ == 'update':
            self.router.add_api_route(f"{self.base_path}/\u007b{self.path_key}\u007d", func, tags=[
                                      self.class_tag], methods=['PUT'], **extras)
        elif func.__name__ == 'partial_update':
            self.router.add_api_route(f"{self.base_path}/\u007b{self.path_key}\u007d", func, tags=[
                                      self.class_tag], methods=['PATCH'], **extras)
        elif func.__name__ == 'destroy':
            self.router.add_api_route(f"{self.base_path}/\u007b{self.path_key}\u007d", func, tags=[
                                      self.class_tag], methods=['DELETE'], **extras)
        else:
            print(f"Method {func.__name__} is not supported")

    def _register_extra_route(self, func: Callable, methods: List[str] = ["GET"], path: str = None):
        extras = {}
        extras['response_model'] = self.get_response_model(func.__name__)
        extras['dependencies'] = self.get_dependencies(func.__name__)
        if path is None:
            path = func.__name__
        self.router.add_api_route(f"{self.base_path}{path}", func, tags=[
                                  self.class_tag], methods=methods, **extras)

    def extra_method(self, methods: List[str] = ["GET"], path_key: str = None):
        """ if you want to add extra method to the viewset, you can use this decorator """
        def decorator(func):
            self.extra_functions.append([func, methods, path_key])
            return func
        return decorator

    def extra(self):
        """ if you want to add extra method to the viewset, you can override this method and use extra_method decorator """
        # TODO: maybe this is not the best way to do this but it works for now


class CrudViewSet(ViewSet):
    """
    This is the base viewset for CRUD operations.
    """
    crud: BaseCrudSet = None
    model: BaseModel = None
    async_db = False

    def __init__(self):
        assert self.crud is not None, "You must define crud model"
        assert self.model is not None, "You must define model"

        self._crud = self.crud()
        super().__init__()

    async def list(self) -> List[model]:
        if self.async_db:
            return await self._crud.list()
        return self._crud.list()

    async def retrieve(self, id: int) -> model:
        if self.async_db:
            return await self._crud.retrieve(id)
        return self._crud.retrieve(id)

    async def create(self, data: model) -> model:
        if self.async_db:
            return await self._crud.create(data)
        return self._crud.create(data)

    async def update(self, id: int, data: model) -> model:
        if self.async_db:
            return await self._crud.update(id, data)
        return self._crud.update(id, data)

    async def partial_update(self, id: int, data: model) -> model:
        if self.async_db:
            return await self._crud.partial_update(id, data)
        return self._crud.partial_update(id, data)

    async def destroy(self, id: int) -> model:
        if self.async_db:
            return await self._crud.destroy(id)
        return self._crud.destroy(id)
