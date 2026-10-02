import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import logging
from smart_search.config.settings import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def debug_config():
    """调试配置"""
    print("=" * 50)
    print("配置检查:")
    print(f"  MYSQL_HOST: {settings.MYSQL_HOST}")
    print(f"  MYSQL_PORT: {settings.MYSQL_PORT}")
    print(f"  MYSQL_USER: {settings.MYSQL_USER}")
    print(f"  MYSQL_DB: {settings.MYSQL_DB}")
    print(f"  REDIS_URL: {settings.REDIS_URL[:20]}...")
    print(f"  INDEX_NAME: {settings.INDEX_NAME}")
    print("=" * 50)

if __name__ == "__main__":
    debug_config()
    
    try:
        from smart_search.core.vector_sync_service import ProductVectorSyncService
        print("开始同步数据...")
        svc = ProductVectorSyncService()
        result = svc.load_sku_from_mysql()
        print(f"结果: {result}")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()