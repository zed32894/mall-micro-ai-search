# tests/test_search_service_debug.py
import sys
import os
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import asyncio
import logging
from smart_search.core.search_service import SearchService

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    print("=" * 60)
    print("开始测试智能搜索服务 (调试模式)")
    print("=" * 60)
    
    try:
        print("\n1. 创建 SearchService 实例...")
        svc = SearchService()
        print("   ✅ SearchService 创建成功")
        
        # 测试条件提取
        print("\n2. 测试条件提取...")
        query = "价格在5000元以内的高性能游戏手机"
        print(f"   Query: {query}")
        
        try:
            resp = await svc.extract_search_condition(query)
            print(f"   ✅ 条件提取成功")
            print(f"   Keyword: {resp.keyword}")
            print(f"   Price range: {resp.min_price} - {resp.max_price}")
        except Exception as e:
            print(f"   ❌ 条件提取失败: {e}")
            traceback.print_exc()
        
        # 测试商品推荐
        print("\n3. 测试商品推荐...")
        tid = 888
        
        try:
            resp1 = await svc.recommend_product(query, thread_id=tid)
            print(f"   ✅ 商品推荐成功")
            print(f"   Summary: {resp1.summary}")
            print(f"   Product count: {len(resp1.product_list)}")
            if resp1.product_list:
                print(f"   第一个商品: {resp1.product_list[0].sku_name[:50]}...")
            print(f"   Reasons: {resp1.reason}")
        except Exception as e:
            print(f"   ❌ 商品推荐失败: {e}")
            traceback.print_exc()
        
        # 测试多轮对话
        print("\n4. 测试多轮对话...")
        try:
            resp2 = await svc.recommend_product("哪一款续航更好", thread_id=tid)
            print(f"   ✅ 多轮对话成功")
            print(f"   Summary: {resp2.summary}")
            print(f"   Product count: {len(resp2.product_list)}")
        except Exception as e:
            print(f"   ❌ 多轮对话失败: {e}")
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ 整体测试失败: {e}")
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())