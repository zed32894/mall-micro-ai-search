import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from smart_search.api.v1 import router as v1_router
from smart_search.models.schemas import Result

logger = logging.getLogger(__name__)

app = FastAPI(
    title="商品智能搜索",
    description="商品智能搜索",
    version="1.0.0"
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, e: Exception):
    logger.error(f"全局异常 - 请求路径: {request.url.path} - 错误信息: {str(e)}", exc_info=True)
    resp = Result(
        code=500,
        msg=f"服务器内部错误:{str(e)}"
    )
    return JSONResponse(
        content=resp.model_dump()
    )

# 注册v1路由
app.include_router(v1_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("smart_search.main:app", host="0.0.0.0", port=9010, reload=True)
