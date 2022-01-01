from typing import Callable, List, Sequence, Union
from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel

__all__ = ['ViewSet', 'register']

supported_methods_names: List[str] = [
    'list', 'retrieve', 'create', 'update', 'partial_update', 'delete']


class ViewSet:
    """ router: APIRouter = None
    base_path: str = None
    class_tag: str = None
    path_key: str = "id"
    response_model: BaseModel = None
    """
    router: APIRouter = None
    base_path: str = None
    class_tag: str = None
    path_key: str = "id"
    response_model: BaseModel = None
    dependencies: Sequence[Depends] = None
    
    functions: List[Callable] = []
    extra_functions: List[List] = []
    
    @classmethod
    def get_response_model(cls, action: str) -> Union[BaseModel, None]:
        """ if override this method, you can return different response model for different action """
        if cls.response_model is not None:
            return cls.response_model
        return None
    
    @classmethod
    def get_dependenciesl(cls, action: str) -> Sequence[Depends]:
        """ if override this method, you can return different dependencies for different action """
        if cls.dependencies is not None:
            return cls.dependencies
        return None


    @classmethod
    def execute(cls) -> APIRouter:

        if cls.router is None:
            cls.router = APIRouter()
        
        if cls.base_path is None:
            cls.base_path = '/' + cls.__name__.lower()
        
        if cls.class_tag is None:
            cls.class_tag = cls.__name__

        for func in cls.__dict__.keys():
            if func in supported_methods_names:
                cls.functions.append(cls.__dict__[func])

        for func in cls.functions:
            cls._register_route(func)
        
        for func,methods,path in cls.extra_functions:
            cls._register_extra_route(func, methods=methods, path=path)

        return cls.router

    @classmethod
    def _register_route(cls, func: Callable):
        # remove self from the arguments
        assert not ("self"  in func.__code__.co_varnames), "self is not allowed in the arguments"
        
        extras = {}  # TODO: not going well this way
        
        if func.__name__ == 'list':
            extras['response_model'] = cls.get_response_model(func.__name__)
            extras['dependencies'] = cls.get_dependenciesl(func.__name__)
            cls.router.add_api_route(cls.base_path, func, tags=[cls.class_tag], methods=['GET'],**extras)
        elif func.__name__ == 'retrieve':
            extras['response_model'] = cls.get_response_model(func.__name__)
            extras['dependencies'] = cls.get_dependenciesl(func.__name__)
            cls.router.add_api_route(f"{cls.base_path}/\u007b{cls.path_key}\u007d", func, tags=[cls.class_tag], methods=['GET'],**extras)
        elif func.__name__ == 'create':
            extras['response_model'] = cls.get_response_model(func.__name__)
            extras['dependencies'] = cls.get_dependenciesl(func.__name__)
            cls.router.add_api_route(cls.base_path, func, tags=[cls.class_tag], methods=['POST'],**extras)
        elif func.__name__ == 'update':
            extras['response_model'] = cls.get_response_model(func.__name__)
            extras['dependencies'] = cls.get_dependenciesl(func.__name__)
            cls.router.add_api_route(f"{cls.base_path}/\u007b{cls.path_key}\u007d", func, tags=[cls.class_tag], methods=['PUT'],**extras)
        elif func.__name__ == 'partial_update':
            extras['response_model'] = cls.get_response_model(func.__name__)
            extras['dependencies'] = cls.get_dependenciesl(func.__name__)
            cls.router.add_api_route(f"{cls.base_path}/\u007b{cls.path_key}\u007d", func, tags=[cls.class_tag], methods=['PATCH'],**extras)
        elif func.__name__ == 'delete':
            extras['response_model'] = cls.get_response_model(func.__name__)
            extras['dependencies'] = cls.get_dependenciesl(func.__name__)
            cls.router.add_api_route(f"{cls.base_path}/\u007b{cls.path_key}\u007d", func, tags=[cls.class_tag], methods=['DELETE'],**extras)
        else:
            print(f"Method {func.__name__} is not supported")

    @classmethod
    def _register_extra_route(cls, func: Callable, methods: List[str] = ["GET"], path: str = None):
        extras = {}
        extras['response_model'] = cls.get_response_model(func.__name__)
        extras['dependencies'] = cls.get_dependenciesl(func.__name__)
        if path is None:
            path = func.__name__
        cls.router.add_api_route(f"{cls.base_path}{path}", func, tags=[cls.class_tag], methods=methods,**extras)

    @classmethod
    def extra_method(cls, methods: List[str] = ["GET"], path_key: str = None):
        """ if you want to add extra method to the viewset, you can use this decorator """
        def decorator(func):
            cls.extra_functions.append([func, methods, path_key])
            return func
        return decorator

def register(cls: ViewSet) -> APIRouter:
    """ for registering ViewSet """
    router = cls.execute()
    return router
