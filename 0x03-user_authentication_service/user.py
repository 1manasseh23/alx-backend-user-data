#!/usr/bin/env python3
"""
User model for the users table
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user in the detabase

    Atributes:
        id (int): The primary key for the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password for the user.
        session_id (str): The session ID associated with the user.
        reset_token (str): The reset token for password recovery.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
