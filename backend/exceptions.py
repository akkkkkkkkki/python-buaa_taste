class UserAlreadyExists(Exception):
    def __init__(self, user_name: str):
        self.user_name = user_name

    def __str__(self) -> str:
        return "user_name '%s' already exist!" % self.user_name


class UserNotFound(Exception):
    def __init__(self, user: str):
        self.user = user

    def __str__(self) -> str:
        return "user '%s' not found!" % self.user


class WrongPassword(Exception):
    def __str__(self) -> str:
        return 'Wrong password!'


class UsernameTaken(Exception):
    def __init__(self, user_name: str):
        self.user_name = user_name

    def __str__(self) -> str:
        return "user_name '%s' is already taken!" % self.user_name


class DishNotFound(Exception):
    def __init__(self, dish_uuid: str):
        self.dish_uuid = dish_uuid

    def __str__(self) -> str:
        return "dish_uuid '%s' not found!" % self.dish_uuid


class UnauthorizedAccess(Exception):
    def __str__(self) -> str:
        return 'insufficient privileges!'


class UserNotExist(Exception):
    def __init__(self, user_name: str):
        self.user_name = user_name

    def __str__(self) -> str:
        return "user_uuid '%s' doesn't exist!" % self.user_name
    
    
class CanteenNotFound(Exception):
    def __str__(self):
        return "canteen_uuid {} doesn't exist".format(self.args[0])
    
class CommentNotExist(Exception):
    def __str__(self):
        return "comment_uuid {} doesn't exist".format(self.args[0])

class RecordNotFound(Exception):
    def __str__(self):
        return "record_uuid {} doesn't exist".format(self.args[0])

class CounterNotExist(Exception):
    def __str__(self):
        return "record_uuid {} doesn't exist".format(self.args[0])

    
class CanteenNotExist(Exception):
    def __str__(self):
        return "canteen_uuid {} doesn't exist".format(self.args[0])