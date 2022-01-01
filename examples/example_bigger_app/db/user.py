
from models.user import User


async def get_users():
    return [User(id=1, name='John Doe'), User(id=2, name='Jane Doe')]