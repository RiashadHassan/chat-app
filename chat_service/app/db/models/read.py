from app.db import BaseRead
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean, DateTime


class User(BaseRead):
    __tablename__ = "core_user"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    uid = Column(UUID(as_uuid=True))
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_staff = Column(Boolean)
    is_verified = Column(Boolean)
    is_deleted = Column(Boolean)

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return f"ID:{self.id}-{self.username}"


class Member(BaseRead):
    __tablename__ = "member_member"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    uid = Column(UUID(as_uuid=True))
    # user = Column()
    user_uid = Column(UUID(as_uuid=True))
    # server = Column()
    server_uid = Column(UUID(as_uuid=True))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)

    def __str__(self):
        return f"Member: {self.uid}"

    def __repr__(self):
        return f"Member:{self.id}- Server: {self.server_uid}"
