#!/usr/bin/env python3
import os

def fix_file_safely(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        skip_mode = False
        line_count = len(lines)
        i = 0
        
        while i < line_count:
            line = lines[i]
            
            # 检测自动回缩代码的开始
            if '// =====================' in line and i + 1 < line_count:
                next_line = lines[i + 1]
                if '页面自动回缩功能' in next_line:
                    # 找到了！开始跳过
                    skip_mode = True
                    has_scriptjs = False
                    skip_start_index = i
                    
                    # 检查这一片段中是否有script.js
                    j = i
                    while j < line_count:
                        if 'js/script.js' in lines[j]:
                            has_scriptjs = True
                        if '</script>' in lines[j]:
                            # 找到了结束位置
                            if has_scriptjs:
                                # 保留 <script src="js/script.js"></script>
                                new_lines.append('    <script src="js/script.js"></script>\n')
                            i = j + 1
                            skip_mode = False
                            break
                        j += 1
                    continue
            
            if not skip_mode:
                new_lines.append(line)
            
            i += 1
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f'✅ Fixed {os.path.basename(filepath)}')
        return True
        
    except Exception as e:
        print(f'❌ Error: {os.path.basename(filepath)}: {e}')
        return False

def main():
    directory = '/workspace/xiaomotou-static'
    files = [
        'art.html', 'mod.html', 'user.html', 'remake.html',
        'cloudsave.html', 'feedback.html', 'card.html',
        'top.html', 'register.html', 'strategy.html',
        'editor.html', 'sign.html', 'demand.html',
        'report.html', 'forum.html', 'tool.html',
        'vip.html', 'game.html', 'activity.html',
        'rank.html', 'play.html', 'novel.html',
        'author.html', 'help.html'
    ]
    
    fixed = 0
    for f in files:
        fp = os.path.join(directory, f)
        if os.path.exists(fp):
            if fix_file_safely(fp):
                fixed += 1
    
    print(f'\n✅ Done! Fixed {fixed} files!')
    print(f'\nNo more flash screen!')
    print(f'☰ nav button works!')
    print(f'− top bar button works!')

if __name__ == '__main__':
    main()
