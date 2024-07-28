from pydantic import BaseModel, StrictStr
from typing import Any, List, Dict, Optional


class LoginRequest(BaseModel):
    host: Optional[StrictStr]
    username: Optional[StrictStr]
    password: Optional[StrictStr]
    port: Optional[int] = 45567
    database: Optional[str] = 'railway'


class DatabaseConnectionInfo(BaseModel):
    host: str
    username: str
    password: str


class QueryRequest(BaseModel):
    database: Optional[str] = 'railway'
    query: str


class QueryResponse(BaseModel):
    sql_query: str
    response: List[Dict[str, Any]]


class PostDatabaseSchema(BaseModel):
    user: str
    database: str
    user_query: str
    processed_query: Any
    response: Any
    connection: Any
