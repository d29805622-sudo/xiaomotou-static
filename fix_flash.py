#!/usr/bin/env python3
import os
import re

def fix_page(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否需要修复
        if '// 导航栏滚动自动隐藏/显示功能' not in content:
            print(f'Skipping {os.path.basename(file_path)} - no auto-hide code')
            return False
        
        # 替换为简化版本 - 移除冲突的自动隐藏逻辑
        # 只保留导航菜单切换和顶部栏折叠功能
        old_script = '''    <script>
        // 导航栏滚动自动隐藏/显示功能
        (function() {
            let lastScrollY = 0;
            const header = document.getElementById('mainHeader');
            const scrollThreshold = 100;
            let isUserScrolling = false;
            
            function handleScroll() {
                const currentScrollY = window.scrollY;
                
                // 向下滚动超过阈值，隐藏导航栏
                if (currentScrollY > lastScrollY && currentScrollY > scrollThreshold) {
                    if (!header.classList.contains('hidden')) {
                        header.classList.remove('visible');
                        header.classList.add('hidden');
                    }
                } 
                // 向上滚动，显示导航栏
                else if (currentScrollY < lastScrollY) {
                    if (header.classList.contains('hidden')) {
                        header.classList.remove('hidden');
                        header.classList.add('visible');
                    }
                }
                
                lastScrollY = currentScrollY;
            }
            
            // 使用 requestAnimationFrame 优化性能
            let ticking = false;
            window.addEventListener('scroll', function() {
                if (!ticking) {
                    window.requestAnimationFrame(function() {
                        handleScroll();
                        ticking = false;
                    });
                    ticking = true;
                }
            });
            
            function toggleNavMenu() {
            const navMenu = document.getElementById('navMenu');
            const menuToggle = document.getElementById('menuToggle');
            
            if (navMenu) {
                navMenu.classList.toggle('expanded');
                menuToggle.textContent = navMenu.classList.contains('expanded') ? '✕' : '☰';
            }
        }
        
        // 顶部栏折叠功能
            const topBar = document.getElementById('topBar');
            const collapseBtn = document.getElementById('collapseBtn');
            const expandTopBtn = document.getElementById('expandTopBtn');
            
            function updateCollapseState(collapsed) {
                if (topBar) {
                    if (collapsed) {
                        topBar.classList.add('collapsed');
                    } else {
                        topBar.classList.remove('collapsed');
                    }
                }
                if (collapseBtn) {
                    collapseBtn.textContent = collapsed ? '+' : '−';
                }
                if (expandTopBtn) {
                    expandTopBtn.style.display = collapsed ? 'inline-block' : 'none';
                }
            }
            
            function toggleCollapse() {
                const currentCollapsed = topBar ? topBar.classList.contains('collapsed') : false;
                const newCollapsed = !currentCollapsed;
                updateCollapseState(newCollapsed);
                localStorage.setItem('topBarCollapsed', newCollapsed);
            }
            
            const isCollapsed = localStorage.getItem('topBarCollapsed') === 'true';
            updateCollapseState(isCollapsed);
            
            if (collapseBtn) {
                collapseBtn.addEventListener('click', toggleCollapse);
            }
            if (expandTopBtn) {
                expandTopBtn.addEventListener('click', toggleCollapse);
            }
        })();
    </script>
    <script src="js/common.js"></script>
    <script src="js/script.js">
        
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

</script>'''
        
        new_script = '''    <script>
        // 导航菜单切换功能
        function toggleNavMenu() {
            const navMenu = document.getElementById('navMenu');
            const menuToggle = document.getElementById('menuToggle');
            
            if (navMenu) {
                navMenu.classList.toggle('expanded');
                menuToggle.textContent = navMenu.classList.contains('expanded') ? '✕' : '☰';
            }
        }
        
        // 顶部栏折叠功能
        (function() {
            const topBar = document.getElementById('topBar');
            const collapseBtn = document.getElementById('collapseBtn');
            const expandTopBtn = document.getElementById('expandTopBtn');
            
            function updateCollapseState(collapsed) {
                if (topBar) {
                    if (collapsed) {
                        topBar.classList.add('collapsed');
                    } else {
                        topBar.classList.remove('collapsed');
                    }
                }
                if (collapseBtn) {
                    collapseBtn.textContent = collapsed ? '+' : '−';
                }
                if (expandTopBtn) {
                    expandTopBtn.style.display = collapsed ? 'inline-block' : 'none';
                }
            }
            
            function toggleCollapse() {
                const currentCollapsed = topBar ? topBar.classList.contains('collapsed') : false;
                const newCollapsed = !currentCollapsed;
                updateCollapseState(newCollapsed);
                localStorage.setItem('topBarCollapsed', newCollapsed);
            }
            
            const isCollapsed = localStorage.getItem('topBarCollapsed') === 'true';
            updateCollapseState(isCollapsed);
            
            if (collapseBtn) {
                collapseBtn.addEventListener('click', toggleCollapse);
            }
            if (expandTopBtn) {
                expandTopBtn.addEventListener('click', toggleCollapse);
            }
        })();
    </script>
    <script src="js/common.js"></script>
    <script src="js/script.js"></script>'''
        
        content = content.replace(old_script, new_script)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'Fixed {os.path.basename(file_path)}')
        return True
        
    except Exception as e:
        print(f'Error fixing {os.path.basename(file_path)}: {e}')
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
    
    fixed_count = 0
    for filename in files_to_fix:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            if fix_page(file_path):
                fixed_count += 1
    
    print(f'\n✅ 成功修复 {fixed_count} 个文件！')
    print(f'\n修复内容：')
    print(f'1. 移除了冲突的滚动自动隐藏逻辑 - 解决闪屏问题')
    print(f'2. 保留导航菜单切换功能')
    print(f'3. 保留顶部栏折叠功能')

if __name__ == '__main__':
    main()
