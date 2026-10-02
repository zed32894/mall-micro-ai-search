# tests/check_vector_data.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from smart_search.config.tools import tools
from smart_search.core.vector_sync_service import ProductVectorSyncService

def check_vector_store():
    print("=" * 60)
    print("检查向量库数据")
    print("=" * 60)
    
    try:
        # 1. 检查向量库连接
        vector_store = tools.get_vector_store()
        print("✅ 向量库连接成功")
        
        # 2. 尝试搜索
        print("\n尝试搜索 '手机'...")
        docs = vector_store.similarity_search("手机", k=5)
        print(f"找到 {len(docs)} 条结果")
        
        if docs:
            print("\n第一条结果:")
            print(f"  Page: {docs[0].page_content[:100]}...")
            print(f"  Meta: {docs[0].metadata}")
        else:
            print("❌ 向量库为空！")
            
            # 3. 尝试重新同步
            print("\n尝试重新同步数据...")
            svc = ProductVectorSyncService()
            result = svc.load_sku_from_mysql()
            print(f"同步结果: {result}")
            
            # 4. 再次检查
            print("\n再次检查...")
            docs = vector_store.similarity_search("手机", k=5)
            print(f"找到 {len(docs)} 条结果")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_vector_store()