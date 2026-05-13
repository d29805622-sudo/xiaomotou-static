#!/usr/bin/env python3
import os
import re

# 高性能回缩功能的JavaScript代码
high_perf_collapse_js = '''
        // =====================
        // 页面自动回缩功能 - 高性能版本
        // =====================
        let collapseTimer = null;
        let lastActivity = Date.now();
        const COLLAPSE_DELAY = 5000; // 5秒无操作后自动回缩
        let isCollapsed = false;
        
        // 节流包装 - 16ms约等于60FPS
        function throttleCollapse(func, limit = 16) {
            let inThrottle = false;
            return function() {
                const context = this;
                const args = arguments;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        }
        
        function resetCollapseTimer() {
            lastActivity = Date.now();
            if (collapseTimer) {
                clearTimeout(collapseTimer);
            }
            if (isCollapsed) {
                expandAll();
            }
            collapseTimer = setTimeout(() => {
                autoCollapse();
            }, COLLAPSE_DELAY);
        }
        
        function autoCollapse() {
            const topBar = document.getElementById('topBar');
            const header = document.getElementById('mainHeader');
            
            if (topBar && !topBar.classList.contains('collapsed')) {
                topBar.classList.add('collapsed');
                localStorage.setItem('topBarCollapsed', 'true');
            }
            if (header && !header.classList.contains('hidden')) {
                header.classList.add('hidden');
                header.classList.remove('visible');
            }
            isCollapsed = true;
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
            isCollapsed = false;
            resetCollapseTimer();
        }
        
        // 优化后的事件监听 - 使用passive: true提高滚动性能
        const throttledExpand = throttleCollapse(expandAll);
        
        document.addEventListener('mousemove', throttledExpand, { passive: true });
        document.addEventListener('scroll', throttledExpand, { passive: true });
        document.addEventListener('keydown', throttledExpand, { passive: true });
        document.addEventListener('click', throttledExpand, { passive: true });
        document.addEventListener('touchstart', throttledExpand, { passive: true });
        document.addEventListener('touchmove', throttledExpand, { passive: true });
        
        // 页面加载时初始化
        document.addEventListener('DOMContentLoaded', function() {
            resetCollapseTimer();
        });
'''

def update_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有高性能版本的回缩代码
        if '高性能版本' in content and 'throttleCollapse' in content:
            print(f'Skipping {file_path} - already optimized')
            return False
        
        # 找到旧的回缩代码并替换
        # 匹配旧代码的开始标记
        old_code_pattern = r'(// 页面自动回缩功能[\s\S]*?)(?=\s*// [^=]|\s*$)'
        
        # 如果找到旧代码，替换它
        if '// 页面自动回缩功能' in content:
            # 使用正则替换
            new_content = re.sub(
                r'// 页面自动回缩功能[\s\S]*?// 页面加载时启动定时器[\s\S]*?resetCollapseTimer\(\);[\s\S]*?\);',
                high_perf_collapse_js,
                content
            )
            
            # 如果没有成功替换，尝试另一种方式
            if new_content == content:
                # 查找script标签并在合适位置插入
                script_end_pattern = r'(</script>\s*$)'
                new_content = re.sub(
                    script_end_pattern,
                    high_perf_collapse_js + '\n        </script>',
                    content
                )
        else:
            # 如果没有回缩代码，尝试添加
            # 找到合适的位置插入
            script_pattern = r'(<script>[\s\S]*?)(?=</script>)'
            new_content = re.sub(
                script_pattern,
                r'\1' + high_perf_collapse_js,
                content
            )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f'Updated {file_path} with high-performance collapse')
        return True
    except Exception as e:
        print(f'Error updating {file_path}: {e}')
        return False

def main():
    directory = '/workspace/xiaomotou-static'
    updated_count = 0
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            if update_file(file_path):
                updated_count += 1
    print(f'\nSuccessfully updated {updated_count} files!')

if __name__ == '__main__':
    main()
