import uuid

from pydantic import BaseModel
from typing import List, Optional

from app.apps.product_catalog.api_v1.schemas.reviews import ReviewSchema


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    category: str


class CreateProductSchema(ProductSchema):
    id: str = str(uuid.uuid4())


class UpdateProductSchema(ProductSchema):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category: Optional[str]


class RetrieveProductSchema(ProductSchema):
    reviews: List[Optional[ReviewSchema]]


