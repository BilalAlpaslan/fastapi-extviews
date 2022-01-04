""" extviews is a fastapi library for creating RESTful APIs with a single class. """

__version__ = "0.1.0"

from .viewset import ViewSet, CrudViewSet
from .crudset import BaseCrudSet, ModelCrudSet, PymongoCrudSet, MotorCrudSet

__all__ = [
    'ViewSet',
    'CrudViewSet',
    'BaseCrudSet',
    'ModelCrudSet',
    'PymongoCrudSet',
    'MotorCrudSet', # !: not yet implemented
]


