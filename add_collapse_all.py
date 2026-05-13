
#!/usr/bin/env python3
import os

# 顶部栏和导航栏自动回缩功能的CSS和JavaScript代码
collapse_css = '''
        .top-bar {
            transition: all 0.3s ease;
        }
        .top-bar.collapsed {
            transform: translateY(-100%);
            margin-bottom: -60px;
        }
        .header {
            transition: all 0.3s ease;
        }
        .header.hidden {
            transform: translateY(-100%);
        }
'''

collapse_js = '''
        // 页面自动回缩功能
        let collapseTimer = null;
        let lastActivity = Date.now();
        const COLLAPSE_DELAY = 5000; // 5秒无操作后自动回缩

        function resetCollapseTimer() {
            lastActivity = Date.now();
            if (collapseTimer) {
                clearTimeout(collapseTimer);
            }
            collapseTimer = setTimeout(() => {
                autoCollapse();
            }, COLLAPSE_DELAY);
        }

        function autoCollapse() {
            const topBar = document.getElementById('topBar');
            const header = document.getElementById('mainHeader');
            
            if (topBar) {
                topBar.classList.add('collapsed');
                localStorage.setItem('topBarCollapsed', 'true');
            }
            if (header) {
                header.classList.add('hidden');
            }
        }

        function expandAll() {
            const topBar = document.getElementById('topBar');
            const header = document.getElementById('mainHeader');
            
            if (topBar) {
                topBar.classList.remove('collapsed');
                localStorage.setItem('topBarCollapsed', 'false');
            }
            if (header) {
                header.classList.remove('hidden');
                header.classList.add('visible');
            }
            resetCollapseTimer();
        }

        // 监听用户活动事件
        document.addEventListener('mousemove', () => {
            expandAll();
        });
        document.addEventListener('scroll', () => {
            expandAll();
        });
        document.addEventListener('keydown', () => {
            expandAll();
        });
        document.addEventListener('click', () => {
            expandAll();
        });

        // 页面加载时启动定时器
        document.addEventListener('DOMContentLoaded', () => {
            resetCollapseTimer();
        });
'''

def add_collapse_to_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查文件是否已经有回缩功能
    if 'autoCollapse' in content:
        print(f"Skipping {file_path} - already has collapse feature")
        return
    
    # 在合适的位置插入CSS和JavaScript
    # 先插入CSS
    if '</style>' in content:
        # 在</style>标签前插入CSS
        content = content.replace('</style>', collapse_css + '</style>')
    elif '<style>' in content:
        # 在<style>标签后插入CSS
        content = content.replace('<style>', '<style>' + collapse_css)
    
    # 再插入JavaScript
    if '</script>' in content:
        # 在最后一个</script>标签前插入JavaScript
        parts = content.split('</script>')
        if len(parts) > 1:
            parts[-2] = parts[-2] + collapse_js
            content = '</script>'.join(parts)
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Added collapse feature to {file_path}")

def main():
    directory = '/workspace/xiaomotou-static'
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            add_collapse_to_file(file_path)

if __name__ == '__main__':
    main()
