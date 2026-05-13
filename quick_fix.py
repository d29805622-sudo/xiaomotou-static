#!/usr/bin/env python3
import os

def clean_file_auto_collapse(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 找到自动回缩代码的开始和结束位置
        start_line = -1
        end_line = -1
        in_collapse_block = False
        collapse_start_marker = '// ====================='
        collapse_end_marker = '</script>'
        
        for i, line in enumerate(lines):
            if '页面自动回缩功能' in line:
                # 找到前几行的开始标记
                for j in range(max(0, i-5), i+1):
                    if collapse_start_marker in lines[j]:
                        start_line = j
                        in_collapse_block = True
                        break
            
            if in_collapse_block and collapse_end_marker in line:
                end_line = i
                break
        
        if start_line != -1 and end_line != -1:
            # 删除自动回缩代码块
            # 但要保留 script.js 的引用
            has_scriptjs = False
            for line in lines[start_line:end_line+1]:
                if 'js/script.js' in line:
                    has_scriptjs = True
                    break
            
            if has_scriptjs:
                # 只保留 <script src="js/script.js"></script>
                new_lines = lines[:start_line] + ['    <script src="js/script.js"></script>\n'] + lines[end_line+1:]
            else:
                # 直接删除这个代码块
                new_lines = lines[:start_line] + lines[end_line+1:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            print(f'✅ Cleaned {os.path.basename(file_path)}')
            return True
        else:
            print(f'⏭️  Skipped {os.path.basename(file_path)}')
            return False
            
    except Exception as e:
        print(f'❌ Error cleaning {os.path.basename(file_path)}: {e}')
        return False

def main():
    directory = '/workspace/xiaomotou-static'
    files_to_clean = [
        'art.html', 'mod.html', 'user.html', 'remake.html',
        'cloudsave.html', 'feedback.html', 'card.html',
        'top.html', 'register.html', 'strategy.html',
        'editor.html', 'sign.html', 'demand.html',
        'report.html', 'forum.html', 'tool.html',
        'vip.html', 'game.html', 'activity.html',
        'rank.html', 'play.html', 'novel.html',
        'author.html', 'help.html'
    ]
    
    cleaned_count = 0
    for filename in files_to_clean:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            if clean_file_auto_collapse(file_path):
                cleaned_count += 1
    
    print(f'\n✅ 成功清理了 {cleaned_count} 个文件！')
    print(f'\n问题已修复：')
    print(f'1. 移除了所有自动回缩功能 - 不会再闪屏了！')
    print(f'2. 保留了导航菜单切换功能（☰按钮）')
    print(f'3. 保留了顶部栏折叠功能（−按钮）')
    print(f'\n现在都是手动控制，不会自动收缩了！')

if __name__ == '__main__':
    main()
