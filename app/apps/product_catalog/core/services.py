import uuid
from typing import List, Optional

from fastapi import HTTPException
from starlette import status

from app.apps.db.base import JSONFileHandler
from app.apps.product_catalog.api_v1.schemas.products import ProductSchema, CreateProductSchema, UpdateProductSchema, \
    ReviewSchema


class ProductDB:
    def __init__(self, json_db: JSONFileHandler):
        self.json_db = json_db

    def get_products(self) -> List[ProductSchema]:
        data = self.json_db.read_data()
        return data["products"]

    def add_product(self, product: CreateProductSchema):
        data = self.json_db.read_data()
        products = data["products"]

        # Check if the product already exists based on its name
        existing_product = next((p for p in products if p["name"] == product.name), None)

        if existing_product:
            # Product with the same name already exists, generate a new ID
            product.id = str(uuid.uuid4())
            products.append(product.dict())
        else:
            products.append(product.dict())

        data["products"] = products
        self.json_db.write_data(data)

    def update_product(self, product_id: str, updated_product: UpdateProductSchema):
        data = self.json_db.read_data()
        products = data["products"]

        # Find the product with the given ID
        product_to_update = next((p for p in products if p["id"] == product_id), None)

        if product_to_update:
            product_to_update.update(updated_product.dict())
            data["products"] = products
            self.json_db.write_data(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product with id - {product_id}")

    def delete_product(self, product_id: str):
        data = self.json_db.read_data()
        products = data["products"]

        # Find the product with the given ID
        product_to_delete = next((p for p in products if p["id"] == product_id), None)

        if product_to_delete:
            products.remove(product_to_delete)
            data["products"] = products
            self.json_db.write_data(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product with id - {product_id}")


class ReviewDB:
    def __init__(self, json_db: JSONFileHandler):
        self.json_db = json_db

    def get_reviews(self, product_id: str) -> List[ReviewSchema]:
        data = self.json_db.read_data()
        reviews = data["reviews"]
        product_reviews = [review for review in reviews if review["product_id"] == product_id]
        return product_reviews

    def add_review(self, review: ReviewSchema):
        data = self.json_db.read_data()
        reviews = data["reviews"]

        # Check if a product with the given product_id exists
        product_id = review.product_id
        product_exists = any(p["id"] == product_id for p in data["products"])

        if product_exists:
            reviews.append(review.dict())
            data["reviews"] = reviews
            self.json_db.write_data(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product with id - {product_id}")

    def update_review(self, review_id: str, updated_review: ReviewSchema):
        data = self.json_db.read_data()
        reviews = data["reviews"]

        # Find the review with the given ID
        review_to_update = next((r for r in reviews if r["id"] == review_id), None)

        # Check if a product with the given product_id exists
        product_id = updated_review.product_id
        product_exists = any(p["id"] == product_id for p in data["products"])

        if review_to_update and product_exists:
            review_to_update.update(updated_review.dict())
            data["reviews"] = reviews
            self.json_db.write_data(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product with id - {product_id}")

    def delete_review(self, review_id: str):
        data = self.json_db.read_data()
        reviews = data["reviews"]

        # Find the review with the given ID
        review_to_delete = next((r for r in reviews if r["id"] == review_id), None)

        if review_to_delete:
            product_id = review_to_delete["product_id"]

            # Check if a product with the given product_id exists
            product_exists = any(p["id"] == product_id for p in data["products"])

            if product_exists:
                reviews.remove(review_to_delete)
                data["reviews"] = reviews
                self.json_db.write_data(data)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product with id - {product_id}")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No review with id - {review_id}")


