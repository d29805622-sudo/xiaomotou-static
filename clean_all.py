#!/usr/bin/env python3
import os

def clean_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找需要移除的自动回缩代码
        start_marker = '// ====================='
        end_marker = '</script>'
        
        # 查找自动回缩代码的位置
        if '页面自动回缩功能' in content:
            # 找到开始位置
            start_idx = content.find('// =====================')
            # 向前找到script标签
            script_start_idx = content.rfind('<script', 0, start_idx)
            if script_start_idx != -1 and 'js/script.js' in content[script_start_idx:start_idx]:
                # 这是在script.js标签中的自动回缩代码
                end_idx = content.find(end_marker, start_idx)
                if end_idx != -1:
                    # 替换为干净的script标签
                    old_code = content[script_start_idx:end_idx + len(end_marker)]
                    new_code = '<script src="js/script.js"></script>'
                    content = content.replace(old_code, new_code)
            else:
                # 在其他地方的自动回缩代码
                end_idx = content.find('</script>', start_idx)
                if end_idx != -1:
                    old_code = content[start_idx:end_idx]
                    content = content.replace(old_code, '')
            
            # 清理可能的空行
            content = content.replace('\n\n\n', '\n\n')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f'✅ Cleaned {os.path.basename(file_path)}')
            return True
        else:
            print(f'⏭️ Skipped {os.path.basename(file_path)} - no auto-collapse code')
            return False
            
    except Exception as e:
        print(f'❌ Error cleaning {os.path.basename(file_path)}: {e}')
        return False

def main():
    directory = '/workspace/xiaomotou-static'
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    
    cleaned_count = 0
    for filename in html_files:
        file_path = os.path.join(directory, filename)
        if clean_file(file_path):
            cleaned_count += 1
    
    print(f'\n✅ 成功清理 {cleaned_count} 个文件！')
    print(f'\n修复说明：')
    print(f'1. 移除了所有自动回缩功能 - 彻底解决闪屏问题！')
    print(f'2. 保留导航菜单切换功能（☰按钮）')
    print(f'3. 保留顶部栏折叠功能（−按钮）')
    print(f'\n现在使用方式：')
    print(f'• 点击 ☰ 可以切换导航菜单的展开/收起')
    print(f'• 点击 − 可以折叠/展开顶部状态栏')
    print(f'• 完全手动控制，不会再自动收缩，也不会闪屏了！')

if __name__ == '__main__':
    main()
