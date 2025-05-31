from uuid import UUID
from pydantic import BaseModel


class UserOut(BaseModel):
    uid: UUID
    username: str
    first_name: str
    last_name: str
    email: str
    phone: str
    is_deleted: bool
    is_staff: bool
    is_verified: bool

    model_config = {"from_attributes": True}
