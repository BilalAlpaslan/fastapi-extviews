from fastapi import HTTPException


def create_query_validation_exception(field: str, msg: str) -> HTTPException:
    return HTTPException(
        422,
        detail={
            "detail": [
                {"loc": ["query", field], "msg": msg,
                    "type": "type_error.integer"}
            ]
        },
    )