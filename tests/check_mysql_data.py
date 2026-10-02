# tests/check_mysql_data.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from smart_search.config.tools import tools

def check_mysql():
    print("=" * 60)
    print("检查 MySQL 商品数据")
    print("=" * 60)
    
    try:
        conn = tools.get_mysql_conn()
        cursor = conn.cursor()
        
        # 查询商品数量
        cursor.execute("SELECT COUNT(*) FROM sku_info WHERE deleted=0")
        count = cursor.fetchone()[0]
        print(f"商品总数: {count}")
        
        if count == 0:
            print("❌ MySQL 中没有商品数据！")
            print("请先在 MySQL 中导入商品数据")
        else:
            # 查询示例商品
            cursor.execute("""
                SELECT id, sku_name, brand_name, price 
                FROM sku_info 
                WHERE deleted=0 
                LIMIT 5
            """)
            rows = cursor.fetchall()
            print("\n示例商品:")
            for row in rows:
                print(f"  ID: {row[0]}, 名称: {row[1][:30]}..., 品牌: {row[2]}, 价格: {row[3]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_mysql()