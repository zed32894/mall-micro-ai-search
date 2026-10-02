# tests/check_mysql_condition.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from smart_search.config.tools import tools

def check_mysql_condition():
    print("=" * 60)
    print("检查 MySQL 中符合条件的商品")
    print("=" * 60)
    
    conn = tools.get_mysql_conn()
    cursor = conn.cursor()
    
    # 查询华为手机
    cursor.execute("""
        SELECT id, sku_name, brand_name, price 
        FROM sku_info 
        WHERE deleted=0 AND brand_name LIKE '%华为%'
        LIMIT 10
    """)
    rows = cursor.fetchall()
    print(f"\n华为手机数量: {len(rows)}")
    for row in rows:
        print(f"  ID: {row[0]}, 名称: {row[1][:50]}..., 品牌: {row[2]}, 价格: {row[3]}")
    
    # 查询5000元以下的手机
    cursor.execute("""
        SELECT id, sku_name, brand_name, price 
        FROM sku_info 
        WHERE deleted=0 AND category_name='手机' AND price <= 5000
        LIMIT 10
    """)
    rows = cursor.fetchall()
    print(f"\n5000元以下手机数量: {len(rows)}")
    for row in rows:
        print(f"  ID: {row[0]}, 名称: {row[1][:50]}..., 品牌: {row[2]}, 价格: {row[3]}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    check_mysql_condition()