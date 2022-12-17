from fastapi import HTTPException, status


class MyException:
    def unauthorized_exception(self):
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        return exception

    def not_exist_item(self):
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found!",
        )
        return exception

    def not_admin(self):
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not admin",
        )
        return exception

    def wrong_code(self):
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong message",
        )
        return exception

    def exist_item(self):
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This is item already exist",
        )
        return exception


my_exception = MyException()


def my_permission():
    def wrapper(user, product):
        if product.user == user:
            return True

    return wrapper