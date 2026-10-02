from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class GoodsInfo(BaseModel):
    """商品SKU信息"""
    id: int
    spu_id: int
    sku_name: str
    price: float
    sku_default_img: str


class Result(BaseModel, Generic[T]):
    """接口通用返回体"""
    code: int = Field(default=200)
    msg: str = Field(default="操作成功")
    data: Optional[T] = None

class SearchCondition(BaseModel):
    """从自然语言解析出来的商品搜索条件"""
    keyword: Optional[str] = Field(None, description="商品关键字，如手机、电视、骁龙865")
    min_price: Optional[float] = Field(description="最低价格",default=0)
    max_price: Optional[float] = Field(description="最高价格",default=100000)

class ProductRecommendResponse(BaseModel):
    """商品大模型推荐返回结果"""
    summary: str = Field(description="总结导语")
    product_list: List[GoodsInfo] = Field(description="推荐商品列表")
    reason: List[str] = Field(description="整体推荐理由")
