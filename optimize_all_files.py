#!/usr/bin/env python3
import os
import re

# 高性能CSS优化 - 替换旧的transition: all
css_optimization = '''
        /* 高性能回缩动画优化 */
        .top-bar {
            transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), 
                        opacity 0.25s ease, 
                        margin-bottom 0.25s ease;
            will-change: transform;
            backface-visibility: hidden;
        }
        .top-bar.collapsed {
            transform: translateY(-100%) translateZ(0);
            margin-bottom: -60px;
        }
        .header {
            transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            will-change: transform;
            backface-visibility: hidden;
        }
        .header.hidden {
            transform: translateY(-100%) translateZ(0);
        }
'''

# 高性能JavaScript回缩功能
js_optimization = '''
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

def optimize_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经优化过
        if '高性能版本' in content and 'throttleCollapse' in content:
            print(f'Skipping {os.path.basename(file_path)} - already optimized')
            return False
        
        modified = False
        new_content = content
        
        # 1. 优化CSS - 替换旧的CSS部分
        old_css_pattern = r'\.top-bar\s*\{[\s\S]*?\.header\.hidden\s*\{[\s\S]*?transform:\s*translateY\([^}]*\}\s*}'
        
        if re.search(old_css_pattern, new_content):
            new_content = re.sub(
                r'\.top-bar\s*\{[\s\S]*?\.header\.hidden\s*\{[\s\S]*?transform:\s*translateY\([^}]*\}\s*}',
                css_optimization,
                new_content,
                flags=re.DOTALL
            )
            modified = True
        
        # 2. 优化JavaScript - 替换旧的回缩功能
        old_js_pattern = r'//\s*页面自动回缩功能[\s\S]*?//\s*页面加载时启动定时器[\s\S]*?resetCollapseTimer\(\);[\s\S]*?\);'
        
        if re.search(old_js_pattern, new_content):
            new_content = re.sub(
                old_js_pattern,
                js_optimization,
                new_content,
                flags=re.DOTALL
            )
            modified = True
        else:
            # 如果没有找到回缩功能，尝试在合适位置添加
            if '<script src="js/common.js">' in new_content:
                insert_point = '<script src="js/common.js">'
                new_content = new_content.replace(
                    insert_point,
                    f'<script>{js_optimization}</script>\n    {insert_point}'
                )
                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Optimized {os.path.basename(file_path)}')
            return True
        else:
            print(f'No changes needed for {os.path.basename(file_path)}')
            return False
            
    except Exception as e:
        print(f'Error optimizing {os.path.basename(file_path)}: {e}')
        return False

def main():
    directory = '/workspace/xiaomotou-static'
    optimized_count = 0
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    
    print(f'Found {len(html_files)} HTML files to optimize...\n')
    
    for filename in html_files:
        file_path = os.path.join(directory, filename)
        if optimize_html_file(file_path):
            optimized_count += 1
    
    print(f'\nSuccessfully optimized {optimized_count}/{len(html_files)} files!')
    print('\nPerformance optimizations applied:')
    print('• Replaced transition: all with specific properties')
    print('• Added will-change and GPU acceleration')
    print('• Used cubic-bezier for smoother animations')
    print('• Added throttling to event listeners')
    print('• Used passive: true for better scroll performance')

if __name__ == '__main__':
    main()
