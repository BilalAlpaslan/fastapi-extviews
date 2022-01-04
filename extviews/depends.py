
from typing import Any, Optional

from fastapi import Depends


PAGINATION = dict(skip=int, limit=int)

def create_query_validation_exception(field: str, msg: str) -> Exception:
    return Exception(f"Invalid query parameter: '{field}' - {msg}")


def pagination_depends(max_limit: Optional[int] = None) -> Any:
    """
    pagination dependency
    """
    def pagination(skip: int = 0, limit: Optional[int] = max_limit) -> PAGINATION:
        if skip < 0:
            raise create_query_validation_exception(
                field="skip",
                msg="skip query parameter must be greater or equal to zero",
            )

        if limit is not None:
            if limit <= 0:
                raise create_query_validation_exception(
                    field="limit", msg="limit query parameter must be greater then zero"
                )

            elif max_limit and max_limit < limit:
                raise create_query_validation_exception(
                    field="limit",
                    msg=f"limit query parameter must be less then {max_limit}",
                )
        return {"skip": skip, "limit": limit}

    return Depends(pagination)