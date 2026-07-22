import uuid

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class RoleRoleResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None


class EndpointCreate(BaseModel):
    name: str
    description: Optional[str] = None

class EndpointUpdate(BaseModel):
    name: str
    description: Optional[str] = None


class EndpointResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None


class AccessRuleCreate(BaseModel):
    role_id: uuid.UUID
    element_id: uuid.UUID
    read_permission: bool = False
    read_all_permission: bool = False
    create_permission: bool = False
    update_permission: bool = False
    update_all_permission: bool = False
    delete_permission: bool = False
    delete_all_permission: bool = False


class AccessRuleResponse(BaseModel):
    id: uuid.UUID
    role_id: uuid.UUID
    element_id: uuid.UUID
    read_permission: bool = False
    read_all_permission: bool = False
    create_permission: bool = False
    update_permission: bool = False
    update_all_permission: bool = False
    delete_permission: bool = False
    delete_all_permission: bool = False
    updated_at: Optional[datetime]


class AccessRuleUpdate(BaseModel):
    read_permission: Optional[bool] = None
    read_all_permission: Optional[bool] = None
    create_permission: Optional[bool] = None
    update_permission: Optional[bool] = None
    update_all_permission: Optional[bool] = None
    delete_permission: Optional[bool] = None
    delete_all_permission: Optional[bool] = None


class UserRoleBase(BaseModel):
    user_id: uuid.UUID
    role_id: uuid.UUID
