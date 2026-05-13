#!/usr/bin/env python3
import os

def fix_one_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 要替换的内容1: 导航栏滚动自动隐藏
        nav_hide_code = '''
        // 导航栏滚动自动隐藏
        (function() {
            let lastScrollY = 0;
            const header = document.getElementById('mainHeader');
            if (!header) return;
            
            window.addEventListener('scroll', function() {
                const currentScrollY = window.scrollY;
                if (currentScrollY > lastScrollY && currentScrollY > 100) {
                    header.classList.remove('visible');
                    header.classList.add('hidden');
                } else if (currentScrollY < lastScrollY) {
                    header.classList.remove('hidden');
                    header.classList.add('visible');
                }
                lastScrollY = currentScrollY;
            });
        })();
'''
        # 要替换的内容2: 页面自动回缩功能
        auto_collapse_code = '''
        
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
        
        # 执行替换
        updated = content
        updated = updated.replace(nav_hide_code, '')
        updated = updated.replace(auto_collapse_code, '')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated)
        
        print(f'✅ Fixed {os.path.basename(file_path)}')
        return True
        
    except Exception as e:
        print(f'❌ {os.path.basename(file_path)}: {e}')
        return False

def main():
    directory = '/workspace/xiaomotou-static'
    files = [
        'art.html', 'mod.html', 'user.html', 'remake.html',
        'cloudsave.html', 'feedback.html', 'card.html',
        'top.html', 'strategy.html', 'editor.html',
        'sign.html', 'demand.html', 'report.html',
        'forum.html', 'tool.html', 'vip.html',
        'game.html', 'activity.html', 'rank.html',
        'play.html', 'novel.html', 'author.html',
        'help.html'
    ]
    
    count = 0
    for filename in files:
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            if fix_one_file(filepath):
                count += 1
    
    print(f'\n✅ 完成！共修复 {count} 个文件！')
    print(f'\n问题已解决：')
    print(f'• 移除了导航栏滚动自动隐藏 - 不闪了！')
    print(f'• 移除了页面自动回缩功能 - 不收缩了！')
    print(f'• 保留☰导航菜单切换键 - 可用！')
    print(f'• 保留−顶部栏折叠键 - 可用！')
    print(f'\n现在都是用户手动控制！')

if __name__ == '__main__':
    main()
