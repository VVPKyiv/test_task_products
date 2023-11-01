import uuid

from pydantic import BaseModel


class ReviewSchema(BaseModel):
    text: str
    product_id: str


class CreateReviewSchema(ReviewSchema):
    id: str = str(uuid.uuid4())


class UpdateReviewSchema(ReviewSchema):
    pass
