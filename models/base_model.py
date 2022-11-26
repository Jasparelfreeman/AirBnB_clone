#!/usr/bin/python3
"""A module that implements the BaseModel class"""

from uuid import uuid4
from datetime import datetime


class BaseModel:
    """A class that defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        if not kwargs:
            from models import storage
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            del kwargs["__class__"]
            kwargs["created_at"] = datetime.strptime(kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            kwargs["updated_at"] = datetime.strptime(kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
            self.__dict__.update(kwargs)

    def __str__(self):
        """
        Returns the string representation of BaseModel object.
        [<class name>] (<self.id>) <self.__dict__>
        """
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Updates 'self.updated_at' with the current datetime"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values of __dict__
        of the instance:
               - only instance attributes set will be returned
               - a key __class__ is added with the class name of the object
               - created_at and updated_at must be converted to string object in ISO object
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = self.__class__.__name__
        for key, value in self.__dict__.items():
            if key in ("created_at", "updated_at"):
                value = self.__dict__[key].isoformat()
                my_dict[key] = value
        return my_dict
