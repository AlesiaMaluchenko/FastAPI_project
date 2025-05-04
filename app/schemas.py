import pydantic


class SchemaIdentifier(pydantic.BaseModel):
    id: int

class SchemaArticle(pydantic.BaseModel):
    id: int
    title: str

class SchemaDevice(pydantic.BaseModel):
    id: int
    name: str
    country: str

class SchemaApplication(pydantic.BaseModel):
    record_id: int
    device_id: str
    article_id: str
    seq_obj: str
