
#!/usr/bin/env python3
import os
import re

kanban_name_style = """
        .kanban-name {
            position: absolute;
            bottom: -28px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, rgba(130, 100, 255, 0.9), rgba(255, 100, 150, 0.9));
            color: #fff;
            font-size: 13px;
            padding: 4px 12px;
            border-radius: 12px;
            white-space: nowrap;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
"""

def fix_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有 kanban-name 样式
    if '.kanban-name' in content:
        print(f"Skipping {file_path} - already has kanban-name style")
        return
    
    # 查找 .kanban img 样式块，在它后面添加 kanban-name 样式
    kanban_img_pattern = re.compile(
        r'(\.kanban img \{[^}]*\})',
        re.DOTALL
    )
    
    if kanban_img_pattern.search(content):
        # 替换，在 .kanban img 样式块后添加 kanban-name 样式
        new_content = kanban_img_pattern.sub(r'\1' + kanban_name_style, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Fixed {file_path}")
    else:
        print(f"No kanban img style found in {file_path}")

def main():
    directory = '/workspace/xiaomotou-static'
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            fix_html_file(file_path)

if __name__ == '__main__':
    main()
