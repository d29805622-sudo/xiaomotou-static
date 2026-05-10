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
        notification.textContent = message;
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
    
    // 6. 页面加载完成后初始化
    document.addEventListener('DOMContentLoaded', function() {
        updateLoginStatus();
        
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
