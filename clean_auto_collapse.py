#!/usr/bin/env python3
import os
import re

def remove_auto_collapse_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到自动回缩的代码块并移除
        # 模式1: 完整的自动回缩代码块
        auto_collapse_pattern = r'\s*// =====================\s*// 页面自动回缩功能 - 高性能版本\s*// =====================\s*let collapseTimer = null;.*?(?=\s*</script>|\s*<script)'
        
        # 模式2: 在script.js标签内的自动回缩代码
        scriptjs_pattern = r'<script src="js/script\.js">\s*// =====================\s*// 页面自动回缩功能 - 高性能版本\s*// =====================\s*let collapseTimer = null;.*?</script>'
        
        # 先尝试模式2
        content = re.sub(scriptjs_pattern, '<script src="js/script.js"></script>', content, flags=re.DOTALL)
        
        # 再尝试模式1
        content = re.sub(auto_collapse_pattern, '', content, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'Cleaned {os.path.basename(file_path)}')
        return True
        
    except Exception as e:
        print(f'Error cleaning {os.path.basename(file_path)}: {e}')
        return False

def main():
    directory = '/workspace/xiaomotou-static'
    files_to_fix = [
        'index.html', 'login.html', 'register.html', 'sign.html',
        'user.html', 'game.html', 'mod.html', 'play.html',
        'editor.html', 'forum.html', 'tool.html', 'demand.html',
        'novel.html', 'art.html', 'author.html', 'card.html',
        'top.html', 'activity.html', 'rank.html', 'strategy.html',
        'help.html', 'feedback.html', 'remake.html', 'report.html',
        'vip.html', 'privacy.html', 'cloudsave.html'
    ]
    
    cleaned_count = 0
    for filename in files_to_fix:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            if remove_auto_collapse_from_file(file_path):
                cleaned_count += 1
    
    print(f'\n✅ 成功清理 {cleaned_count} 个文件！')
    print(f'\n修复说明：')
    print(f'1. 移除了所有自动回缩功能 - 解决闪屏问题')
    print(f'2. 保留导航菜单切换功能（☰按钮）')
    print(f'3. 保留顶部栏折叠功能（−按钮）')
    print(f'\n现在：')
    print(f'• 点击 ☰ 可以切换导航菜单的展开/收起')
    print(f'• 点击 − 可以折叠/展开顶部状态栏')
    print(f'• 不会再自动收缩，避免闪屏！')

if __name__ == '__main__':
    main()
