
from sqlmodel import Relationship, SQLModel, Field, create_engine, Session
from typing import Optional
from infra.database import Connection


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    email: str
    profile: Optional["Profile"] = Relationship(back_populates="user")


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    profession: str
    description: str
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="profile")



def create_user(user: User, profile: Profile = None):
    with Connection() as conn:
        conn.add(user)
        conn.commit()
        conn.refresh(user)

        if profile:
            profile.user_id = user.id
            conn.add(profile)
            conn.commit()


def update_user(user: User):
    with Connection() as conn:
        existing_user = conn.get(User, user.id)
        if existing_user:
            merged_user = conn.merge(user)
            conn.commit()
            conn.refresh(merged_user)
            return merged_user


def get_user(id: int):
    with Connection() as conn:
        user = conn.get(User, id)
        return user, user.profile


def delete_user(id: int):
    with Connection() as conn:
        user = conn.get(User, id)
        if user:
            conn.delete(user.profile)
            conn.delete(user)
            conn.commit()