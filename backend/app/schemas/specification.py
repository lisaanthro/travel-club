from pydantic import BaseModel


class Specification(BaseModel):
    property1: str | None
    property2: str | None
    property3: str | None


class SpecificationUpdateRequest(BaseModel):
    property1: str | None = None
    property2: str | None = None
    property3: str | None = None
