# tests/check_redis_index.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from smart_search.config.settings import settings
import redis

def check_redis():
    print("=" * 60)
    print("检查 Redis 向量索引")
    print("=" * 60)
    
    r = redis.Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True
    )
    
    # 1. 检查索引是否存在
    index_name = settings.INDEX_NAME
    print(f"索引名称: {index_name}")
    
    try:
        info = r.execute_command('FT.INFO', index_name)
        print(f"✅ 索引 '{index_name}' 存在")
        print(f"索引信息: {info}")
    except Exception as e:
        if 'no such index' in str(e).lower():
            print(f"❌ 索引 '{index_name}' 不存在")
            print("需要重新同步数据")
        else:
            print(f"❌ 错误: {e}")
    
    # 2. 检查所有键
    print("\n所有 Redis 键:")
    keys = r.keys('*')
    for key in keys[:20]:  # 只显示前20个
        print(f"  {key}")
    if len(keys) > 20:
        print(f"  ... 共 {len(keys)} 个键")

if __name__ == "__main__":
    check_redis()