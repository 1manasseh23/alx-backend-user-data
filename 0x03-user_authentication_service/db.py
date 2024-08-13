#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Dict
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        self._session

        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        self.__session.add(new_user)
        self.__session.commit()
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """Find a user by specified attributes.

        Raises:
            error: NoResultFound: When no results are found.
            error: InvalidRequestError: When invalid query arguments are passed

        Returns:
            User: First row found in the `users` table.
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        # print("Type of user: {}".format(type(user)))
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.
        Args:
            user_id (int): The ID of the user to update.
        kwargs: Arbitrary keyword arguments representing
                the attributes to update.
        Raises:
            ValueError: If an attribute that does not exist
        """
        # Locate the user by user_id
        user = self.find_user_by(id=user_id)

        # Iterate through the provided attributes
        for key, value in kwargs.items():
            # Check if the attribute exists on the User object
            if not hasattr(user, key):
                raise ValueError(f"Attribute {key} does not exist")

            # Update the attribute
            setattr(user, key, value)

        # Commit the changes to the database
        self._session.commit()
