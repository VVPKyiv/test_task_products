import uuid

from fastapi import Depends, Path
from starlette import status
from fastapi_utils.inferring_router import InferringRouter

from app.apps.db.base import JSONFileHandler, get_file_db
from app.apps.product_catalog.api_v1.schemas.reviews import ReviewSchema, CreateReviewSchema, UpdateReviewSchema
from app.apps.product_catalog.core.services import ReviewDB

router = InferringRouter()


@router.post("/{product_id}", status_code=status.HTTP_201_CREATED)
async def create_review(
        product_id: str,
        review: CreateReviewSchema,
        file_db: JSONFileHandler = Depends(get_file_db),
):
    review = ReviewSchema(id=str(uuid.uuid4()), product_id=product_id, text=review.text)
    review_db = ReviewDB(file_db)
    review_db.add_review(review)
    return {"message": "Review added successfully"}


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_reviews(
        product_id: str = Path(..., description="ID of the product to retrieve reviews for"),
        file_db: JSONFileHandler = Depends(get_file_db),
):
    review_db = ReviewDB(file_db)
    reviews = review_db.get_reviews(product_id)
    return reviews


@router.put("/{review_id}", status_code=status.HTTP_200_OK)
async def update_review(
        review_id: str,
        updated_review: UpdateReviewSchema,
        file_db: JSONFileHandler = Depends(get_file_db),
):
    review_db = ReviewDB(file_db)
    review_db.update_review(review_id, updated_review)
    return {"message": "Review updated successfully"}


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
        review_id: str,
        file_db: JSONFileHandler = Depends(get_file_db),
):
    review_db = ReviewDB(file_db)
    review_db.delete_review(review_id)
    return
