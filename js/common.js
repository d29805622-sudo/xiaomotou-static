// 全局通用脚本
(function() {
    // 1. 页面加载完成效果
    document.addEventListener('DOMContentLoaded', function() {
        document.body.classList.add('loaded');
    });
    
    // 2. 统一登录状态检查和导航栏更新
    function updateLoginStatus() {
        const navButtons = document.getElementById('navButtons');
        if (!navButtons) return;
        
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        
        if (currentUser) {
            navButtons.innerHTML = `
                <span style="color: #c0b4ff; margin-right: 10px; font-size: 14px;">👋 ${currentUser.username}</span>
                <a href="sign.html" class="sign-btn">每日签到</a>
                <a href="user.html" class="common-btn">个人中心</a>
                <a href="javascript:void(0);" class="common-btn" onclick="window.logout && window.logout()">退出登录</a>
            `;
        }
    }
    
    // 3. 退出登录函数
    window.logout = function() {
        if (confirm('确定要退出登录吗？')) {
            localStorage.removeItem('currentUser');
            showNotification('已成功退出登录', 'success');
            setTimeout(function() {
                location.reload();
            }, 800);
        }
    };
    
    // 4. 返回顶部功能
    window.scrollToTop = function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };
    
    // 5. 显示通知
    window.showNotification = function(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `<span class="notification-icon">${type === 'success' ? '✓' : '✕'}</span><span class="notification-text">${message}</span>`;
        document.body.appendChild(notification);
        
        setTimeout(function() {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100px)';
            notification.style.transition = 'all 0.3s ease';
            
            setTimeout(function() {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    };
    
    // 6. 检查登录状态
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
    
    // 7. 收藏功能
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
    
    // 8. 获取收藏状态
    window.isFavorited = function(itemId) {
        const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        return favorites.some(f => f.id === itemId);
    };
    
    // 9. 获取用户统计数据
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
    
    // 10. 页面加载完成后初始化
    document.addEventListener('DOMContentLoaded', function() {
        updateLoginStatus();
        
        // 添加通知样式
        const style = document.createElement('style');
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
                animation: slideIn 0.3s ease;
                max-width: 320px;
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
                    transform: translateX(100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
        `;
        document.head.appendChild(style);
        
        // 绑定返回顶部按钮
        const scrollTopBtn = document.getElementById('scrollTopBtn');
        if (scrollTopBtn) {
            scrollTopBtn.addEventListener('click', window.scrollToTop);
        }
        
        // 滚动时显示/隐藏返回顶部
        window.addEventListener('scroll', function() {
            if (scrollTopBtn) {
                scrollTopBtn.style.display = window.scrollY > 300 ? 'block' : 'none';
            }
        });
    });
})();
