from fastapi import Depends, Request, Query
from fastapi_utils.inferring_router import InferringRouter
from starlette import status

from app.apps.db.base import JSONFileHandler, get_file_db
from app.apps.product_catalog.api_v1.schemas.products import ProductSchema, CreateProductSchema, UpdateProductSchema
from app.apps.product_catalog.core.services import ProductDB

router = InferringRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_products(file_db: JSONFileHandler = Depends(get_file_db)):
    data = file_db.read_data()
    return data


@router.post("/", status_code=status.HTTP_200_OK)
async def create_product(
        product: CreateProductSchema,
        file_db: JSONFileHandler = Depends(get_file_db),
):
    product_db = ProductDB(file_db)
    product_db.add_product(product)
    return {"message": "Product added successfully"}


@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
        product_id: str,
        updated_product: UpdateProductSchema,
        file_db: JSONFileHandler = Depends(get_file_db),
):
    product_db = ProductDB(file_db)
    product_db.update_product(product_id, updated_product)
    return {"message": "Product updated successfully"}


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_id: str,
        file_db: JSONFileHandler = Depends(get_file_db),
):
    product_db = ProductDB(file_db)
    product_db.delete_product(product_id)
    return


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_products(
        name: str = Query(None, description="Product name to search for"),
        category: str = Query(None, description="Product category to search for"),
        min_price: float = Query(None, description="Minimum price for products"),
        max_price: float = Query(None, description="Maximum price for products"),
        logical_operator: str = Query("AND", description="Logical operator (AND, OR, NOT) to combine criteria"),
        file_db: JSONFileHandler = Depends(get_file_db),
):
    data = file_db.read_data()
    products = data["products"]
    # Filter products based on search criteria
    filtered_products = []
    if name:
        filtered_products.extend([p for p in products if name in p["name"]])
    if category:
        filtered_products.extend([p for p in products if category == p["category"]])
    if min_price is not None:
        filtered_products.extend([p for p in products if p["price"] >= min_price])
    if max_price is not None:
        filtered_products.extend([p for p in products if p["price"] <= max_price])
    # Apply the logical operator to combine criteria
    if logical_operator == "OR":
        result_products = filtered_products
    elif logical_operator == "NOT":
        result_products = [p for p in products if p not in filtered_products]
    else:  # Default is "AND"
        result_products = [p for p in products if all(p in filtered_products for p in [name, category, min_price, max_price])]
    return result_products


