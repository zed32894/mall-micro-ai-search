# tests/check_embedding.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from smart_search.config.tools import tools

def check_embedding():
    print("=" * 60)
    print("检查向量模型")
    print("=" * 60)
    
    try:
        embeddings = tools.get_embeddings()
        print("✅ 向量模型初始化成功")
        
        # 测试向量生成
        text = "华为手机"
        print(f"\n测试文本: '{text}'")
        vector = embeddings.embed_query(text)
        print(f"向量长度: {len(vector)}")
        print(f"向量前5个值: {vector[:5]}")
        print("✅ 向量生成成功")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_embedding()