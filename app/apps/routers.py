from fastapi_utils.inferring_router import InferringRouter
from app.apps.product_catalog.api_v1.routers import router as product_router


router = InferringRouter()


router.include_router(product_router, prefix="")
