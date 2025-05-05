from typing import Annotated
import pydantic


class SchemaIdentifier(pydantic.BaseModel):
    id: Annotated[int, pydantic.Field(ge=0)]

class SchemaArticle(pydantic.BaseModel):
    id: Annotated[int, pydantic.Field(ge=0)]
    title: str

class SchemaDevice(pydantic.BaseModel):
    id: Annotated[int, pydantic.Field(ge=0)]
    name: str
    country: str

class SchemaApplication(pydantic.BaseModel):
    record_id: Annotated[int, pydantic.Field(ge=0)]
    device_id: str
    article_id: str
    seq_obj: str
