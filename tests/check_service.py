# tests/check_service.py
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("=" * 60)
print("检查 search_service.py 文件")
print("=" * 60)

# 1. 检查文件是否存在
file_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'smart_search', 'core', 'search_service.py')
print(f"1. 文件路径: {file_path}")
print(f"   文件存在: {os.path.exists(file_path)}")

# 2. 读取文件内容
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"\n2. 文件大小: {len(content)} 字符")
    print(f"\n3. 文件前200个字符:")
    print("-" * 60)
    print(content[:200])
    print("-" * 60)
    
    # 3. 检查是否包含 SearchService
    if 'SearchService' in content:
        print("\n4. ✅ 找到 'SearchService'")
        # 查找类定义行
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'class SearchService' in line:
                print(f"   第 {i+1} 行: {line.strip()}")
                # 显示后面几行
                for j in range(i+1, min(i+5, len(lines))):
                    print(f"   {j+1}: {lines[j].strip()}")
                break
    else:
        print("\n4. ❌ 未找到 'SearchService'")
        
    # 4. 检查是否有语法错误
    print("\n5. 尝试导入...")
    try:
        import smart_search.core.search_service
        print("   ✅ 模块导入成功")
        print(f"   模块内容: {dir(smart_search.core.search_service)}")
    except Exception as e:
        print(f"   ❌ 导入失败: {e}")

print("\n" + "=" * 60)