#!/usr/bin/env python3
import os
import re

def fix_single_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找自动回缩代码 - 从注释开始到script结束
        # 我们要匹配的模式:
        # // =====================
        # // 页面自动回缩功能...
        # ... (很多代码)
        # </script>
        pattern = r'(\s*// =+.*?// 页面自动回缩功能.*?</script>)'
        
        match = re.search(pattern, content, re.DOTALL)
        if match:
            matched_text = match.group(1)
            # 检查这个匹配中是否有script.js的引用
            if 'js/script.js' in matched_text:
                # 如果有，替换成只有script.js引用
                new_content = content.replace(matched_text, '\n    <script src="js/script.js"></script>')
            else:
                # 如果没有，直接删除
                new_content = content.replace(matched_text, '')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'✅ Fixed {os.path.basename(filepath)}')
            return True
        else:
            print(f'⏭️ Skipped {os.path.basename(filepath)}')
            return False
    except Exception as e:
        print(f'❌ Error fixing {os.path.basename(filepath)}: {e}')
        return False

def main():
    directory = '/workspace/xiaomotou-static'
    files_to_fix = [
        'art.html', 'mod.html', 'user.html', 'remake.html',
        'cloudsave.html', 'feedback.html', 'card.html',
        'top.html', 'register.html', 'strategy.html',
        'editor.html', 'sign.html', 'demand.html',
        'report.html', 'forum.html', 'tool.html',
        'vip.html', 'game.html', 'activity.html',
        'rank.html', 'play.html', 'novel.html',
        'author.html', 'help.html'
    ]
    
    count = 0
    for filename in files_to_fix:
        full_path = os.path.join(directory, filename)
        if os.path.exists(full_path):
            if fix_single_file(full_path):
                count += 1
    
    print(f'\n✅ 修复完成！共修复 {count} 个文件！')
    print(f'\n问题已解决：')
    print(f'• 移除了自动回缩功能 - 不再会闪屏了！')
    print(f'• 保留了☰导航菜单切换按钮')
    print(f'• 保留了−顶部栏折叠按钮')
    print(f'\n现在都是用户手动控制，不会自动收缩！')

if __name__ == '__main__':
    main()
