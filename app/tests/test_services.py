import json
from fastapi import HTTPException
import pytest

from app.apps.db.base import LocalJSONFileHandler
from app.apps.product_catalog.api_v1.schemas.products import CreateProductSchema, UpdateProductSchema
from app.apps.product_catalog.api_v1.schemas.reviews import ReviewSchema, CreateReviewSchema
from app.apps.product_catalog.core.services import ProductDB, ReviewDB


class TestProductDB:
    @pytest.fixture
    def json_db(self, tmp_path):
        # Create a temporary JSON file for testing
        file_path = tmp_path / "test_data.json"
        data = {
            "products": [],
            "categories": [],
            "reviews": [],
        }
        with open(file_path, "w") as file:
            json.dump(data, file)
        return LocalJSONFileHandler(file_path)

    def test_add_product(self, json_db):
        product_db = ProductDB(json_db)
        product_data = CreateProductSchema(name="Product1", description="Description", price=10.0, category="CategoryA")
        product_db.add_product(product_data)

        # Verify that the product is added
        products = product_db.get_products()
        assert len(products) == 1
        assert products[0]["name"] == "Product1"

    def test_update_product(self, json_db):
        product_db = ProductDB(json_db)
        product_data = CreateProductSchema(name="Product1", description="Description", price=10.0, category="CategoryA")
        product_db.add_product(product_data)

        products = product_db.get_products()

        # Update the product
        updated_data = UpdateProductSchema(name="UpdatedProduct", description="Updated Description", price=20.0, category="CategoryB")
        product_db.update_product(product_id=products[0]["id"], updated_product=updated_data)

        # Verify that the product is updated
        products = product_db.get_products()
        assert len(products) == 1
        assert products[0]["name"] == "UpdatedProduct"

    def test_delete_product(self, json_db):
        product_db = ProductDB(json_db)
        product_data = CreateProductSchema(name="Product1", description="Description", price=10.0, category="CategoryA")
        product_db.add_product(product_data)

        products = product_db.get_products()

        # Delete the product
        product_id = products[0]["id"]
        product_db.delete_product(product_id)

        # Verify that the product is deleted
        products = product_db.get_products()
        assert len(products) == 0

    def test_update_product_not_found(self, json_db):
        product_db = ProductDB(json_db)
        with pytest.raises(HTTPException):
            product_db.update_product(product_id="non_existing_id", updated_product=UpdateProductSchema(name="UpdatedProduct"))

    def test_delete_product_not_found(self, json_db):
        product_db = ProductDB(json_db)
        with pytest.raises(HTTPException):
            product_db.delete_product(product_id="non_existing_id")


class TestReviewDB:
    @pytest.fixture
    def json_db(self, tmp_path):
        # Create a temporary JSON file for testing
        file_path = tmp_path / "test_data.json"
        data = {
            "products": [],
            "categories": [],
            "reviews": [],
        }
        with open(file_path, "w") as file:
            json.dump(data, file)
        return LocalJSONFileHandler(file_path)

    def test_add_review(self, json_db):
        # TODO - move to fixture product creation
        product_db = ProductDB(json_db)
        product_data = CreateProductSchema(name="Product1", description="Description", price=10.0, category="CategoryA",
                                           id="test_id")
        product_db.add_product(product_data)


        review_db = ReviewDB(json_db)
        review_data = ReviewSchema(id="review1", text="Review text", product_id="test_id")
        review_db.add_review(review_data)

        # Verify that the review is added
        reviews = review_db.get_reviews("test_id")
        assert len(reviews) == 1


    def test_update_review(self, json_db):
        # TODO - move to fixture product creation
        product_db = ProductDB(json_db)
        product_data = CreateProductSchema(name="Product1", description="Description", price=10.0, category="CategoryA",
                                           id="test_id")
        product_db.add_product(product_data)

        review_db = ReviewDB(json_db)
        review_data = CreateReviewSchema(id="review1", text="Review text", product_id="test_id")
        review_db.add_review(review_data)

        # Update the review
        updated_data = ReviewSchema(text="Updated Review", product_id="test_id")
        review_db.update_review(review_id="review1", updated_review=updated_data)

        # Verify that the review is updated
        reviews = review_db.get_reviews("test_id")
        assert len(reviews) == 1
        assert reviews[0]["text"] == "Updated Review"

    def test_delete_review(self, json_db):
        # TODO - move to fixture product creation
        product_db = ProductDB(json_db)
        product_data = CreateProductSchema(name="Product1", description="Description", price=10.0, category="CategoryA",
                                           id="test_id")
        product_db.add_product(product_data)

        review_db = ReviewDB(json_db)
        review_data = CreateReviewSchema(id="review1", text="Review text", product_id="test_id")
        review_db.add_review(review_data)

        # Delete the review
        review_db.delete_review("review1")

        # Verify that the review is deleted
        reviews = review_db.get_reviews("product1")
        assert len(reviews) == 0

    def test_update_review_not_found(self, json_db):
        review_db = ReviewDB(json_db)
        with pytest.raises(HTTPException):
            review_db.update_review(review_id="non_existing_id", updated_review=ReviewSchema(id="review1", text="Updated Review", product_id="product1"))

    def test_delete_review_not_found(self, json_db):
        review_db = ReviewDB(json_db)
        with pytest.raises(HTTPException):
            review_db.delete_review(review_id="non_existing_id")
