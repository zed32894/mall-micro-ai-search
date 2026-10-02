import asyncio
from smart_search.core.search_service import SearchService
async def main():
    svc = SearchService()
    resp = await svc.extract_search_condition("价格在5000元以内的高性能游戏手机")
    print(resp)
    
    tid = 888
    resp1 = await svc.recommend_product("价格在5000元以内的高性能游戏手机", thread_id=tid)
    print(resp1.model_dump_json(indent=2))

    resp2 = await svc.recommend_product("哪一款续航更好", thread_id=tid)
    print(resp2.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(main())
