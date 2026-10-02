from fastapi import APIRouter
from smart_search.core.search_service import SearchService
from smart_search.core.vector_sync_service import ProductVectorSyncService
from smart_search.models.schemas import ProductRecommendResponse, Result, SearchCondition

# 实例化业务服务
searchService = SearchService()
productVectorSyncService = ProductVectorSyncService()

router = APIRouter(prefix="/api/v1", tags=["商品智能搜索接口"])

@router.get("/test", summary="示例")
def home():
    return {"message": "智能搜索服务启动成功"}

@router.get("/sync", summary="同步商品向量")
def sync() -> Result[str]:
    success = productVectorSyncService.load_sku_from_mysql()
    return Result(data=success)

@router.get("/recommend", summary="商品智能推荐")
async def recommend(query: str, thread_id: int = 0) -> Result[ProductRecommendResponse]:
    response_data = await searchService.recommend_product(query, thread_id)
    return Result(data=response_data)

@router.get("/extract", summary="商品查询条件拆解")
async def extract(query: str) -> Result[SearchCondition]:
    search_condition = await searchService.extract_search_condition(query)
    return Result(data=search_condition)
