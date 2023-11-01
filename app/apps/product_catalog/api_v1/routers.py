from fastapi_utils.inferring_router import InferringRouter

from .views import products, reviews

router = InferringRouter()

router.include_router(
    products.router,
    prefix="/products",
    tags=[
        "Products",
    ],
)
router.include_router(
    reviews.router,
    prefix="/reviews",
    tags=[
        "Reviews",
    ],
)