import pydantic


class SchemaIdentifier(pydantic.BaseModel):
    id: int

class SchemaArticle(pydantic.BaseModel):
    id: int
    title: str
