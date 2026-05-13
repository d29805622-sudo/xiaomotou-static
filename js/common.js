// 全局通用脚本 - 高性能优化版本
(function() {
    // =====================
    // 性能优化工具函数
    // =====================
    
    // 节流函数 - 限制函数调用频率，确保高刷新率流畅
    function throttle(func, limit = 16) { // 约60FPS，16ms一帧
        let inThrottle = false;
        let lastFunc = null;
        let lastRan = 0;
        
        return function() {
            const context = this;
            const args = arguments;
            
            if (!inThrottle) {
                func.apply(context, args);
                lastRan = Date.now();
                inThrottle = true;
            } else {
                clearTimeout(lastFunc);
                lastFunc = setTimeout(function() {
                    if (Date.now() - lastRan >= limit) {
                        func.apply(context, args);
                        lastRan = Date.now();
                    }
                }, limit - (Date.now() - lastRan));
            }
        };
    }
    
    // requestAnimationFrame包装器
    function raf(callback) {
        return window.requestAnimationFrame ? 
            window.requestAnimationFrame(callback) : 
            setTimeout(callback, 16);
    }
    
    // 批量DOM更新
    function batchUpdate(callback) {
        raf(() => {
            callback();
        });
    }
    
    // =====================
    // 页面加载优化
    // =====================
    
    // 页面加载完成效果
    document.addEventListener('DOMContentLoaded', function() {
        batchUpdate(() => {
            document.body.classList.add('loaded');
        });
        updateLoginStatus();
    });
    
    // =====================
    // 登录状态管理
    // =====================
    
    function updateLoginStatus() {
        const navButtons = document.getElementById('navButtons');
        if (!navButtons) return;
        
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        
        if (currentUser) {
            batchUpdate(() => {
                navButtons.innerHTML = `
                    <span style="color: #c0b4ff; margin-right: 10px; font-size: 14px;">👋 ${currentUser.username}</span>
                    <a href="sign.html" class="sign-btn">每日签到</a>
                    <a href="user.html" class="common-btn">个人中心</a>
                    <a href="javascript:void(0);" class="common-btn" onclick="window.logout && window.logout()">退出登录</a>
                `;
            });
        }
    }
    
    // =====================
    // 退出登录
    // =====================
    
    window.logout = function() {
        if (confirm('确定要退出登录吗？')) {
            localStorage.removeItem('currentUser');
            showNotification('已成功退出登录', 'success');
            setTimeout(function() {
                location.reload();
            }, 800);
        }
    };
    
    // =====================
    // 返回顶部 - 高性能版本
    // =====================
    
    window.scrollToTop = function() {
        const startY = window.scrollY;
        const targetY = 0;
        const duration = 300;
        const startTime = performance.now();
        
        function scrollStep(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            const currentY = startY + (targetY - startY) * easeProgress;
            
            window.scrollTo(0, currentY);
            
            if (progress < 1) {
                raf(scrollStep);
            }
        }
        
        raf(scrollStep);
    };
    
    // =====================
    // 通知系统 - 优化性能
    // =====================
    
    window.showNotification = function(message, type = 'success') {
        batchUpdate(() => {
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            notification.innerHTML = `<span class="notification-icon">${type === 'success' ? '✓' : '✕'}</span><span class="notification-text">${message}</span>`;
            document.body.appendChild(notification);
            
            setTimeout(function() {
                notification.style.opacity = '0';
                notification.style.transform = 'translateX(100px) translateZ(0)';
                notification.style.transition = 'transform 0.25s ease-out, opacity 0.25s ease-out';
                
                setTimeout(function() {
                    if (notification.parentNode) {
                        document.body.removeChild(notification);
                    }
                }, 250);
            }, 3000);
        });
    };
    
    // =====================
    // 登录检查
    // =====================
    
    window.checkLogin = function(redirectToLogin = true) {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        if (!currentUser) {
            if (redirectToLogin) {
                if (confirm('请先登录后再进行此操作，是否前往登录页面？')) {
                    window.location.href = 'login.html';
                }
            }
            return false;
        }
        return true;
    };
    
    // =====================
    // 收藏功能
    // =====================
    
    window.toggleFavorite = function(itemId, itemName, itemType) {
        if (!checkLogin(true)) return;
        
        let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        const existingIndex = favorites.findIndex(f => f.id === itemId);
        
        if (existingIndex >= 0) {
            favorites.splice(existingIndex, 1);
            showNotification(`已取消收藏：${itemName}`, 'success');
            return false;
        } else {
            favorites.push({
                id: itemId,
                name: itemName,
                type: itemType,
                addTime: new Date().toLocaleString()
            });
            showNotification(`已添加到收藏夹：${itemName}`, 'success');
            return true;
        }
    };
    
    window.isFavorited = function(itemId) {
        const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        return favorites.some(f => f.id === itemId);
    };
    
    // =====================
    // 用户统计
    // =====================
    
    window.getUserStats = function() {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const posts = JSON.parse(localStorage.getItem('posts') || '[]');
        const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        const signData = JSON.parse(localStorage.getItem('signData') || '{}');
        const userPosts = currentUser ? posts.filter(p => p.author === currentUser.username) : [];
        const userFavorites = currentUser ? favorites.filter(f => f.type !== undefined) : [];
        
        return {
            postCount: userPosts.length,
            favoriteCount: userFavorites.length,
            totalPoints: signData.points || 0,
            signDays: signData.totalDays || 0
        };
    };
    
    // =====================
    // 初始化 - 高性能版本
    // =====================
    
    document.addEventListener('DOMContentLoaded', function() {
        updateLoginStatus();
        
        // 添加通知样式 - 只执行一次
        if (!document.getElementById('notification-styles')) {
            const style = document.createElement('style');
            style.id = 'notification-styles';
            style.textContent = `
                .notification {
                    position: fixed;
                    top: 80px;
                    right: 20px;
                    background: rgba(24, 27, 52, 0.95);
                    backdrop-filter: blur(10px);
                    border-radius: 12px;
                    padding: 14px 20px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    box-shadow: 0 8px 26px rgba(0,0,0,0.35);
                    border: 1px solid rgba(130,100,255,0.25);
                    z-index: 9999;
                    animation: slideIn 0.25s ease-out;
                    max-width: 320px;
                    will-change: transform, opacity;
                    transform: translateZ(0);
                }
                .notification.success {
                    border-left: 4px solid #4ade80;
                }
                .notification.error {
                    border-left: 4px solid #f87171;
                }
                .notification-icon {
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 14px;
                    font-weight: bold;
                }
                .notification.success .notification-icon {
                    background: rgba(74, 222, 128, 0.2);
                    color: #4ade80;
                }
                .notification.error .notification-icon {
                    background: rgba(248, 113, 113, 0.2);
                    color: #f87171;
                }
                .notification-text {
                    color: #e8ebf2;
                    font-size: 14px;
                }
                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateX(100px) translateZ(0);
                    }
                    to {
                        opacity: 1;
                        transform: translateX(0) translateZ(0);
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        // 绑定返回顶部按钮
        const scrollTopBtn = document.getElementById('scrollTopBtn');
        if (scrollTopBtn) {
            scrollTopBtn.addEventListener('click', window.scrollToTop);
            
            // 使用节流优化滚动事件
            const handleScroll = throttle(function() {
                if (scrollTopBtn) {
                    scrollTopBtn.style.display = window.scrollY > 300 ? 'block' : 'none';
                }
            }, 16);
            
            window.addEventListener('scroll', handleScroll, { passive: true });
        }
    });
    
    // 导出工具函数供其他模块使用
    window.throttle = throttle;
    window.raf = raf;
    window.batchUpdate = batchUpdate;
})();
