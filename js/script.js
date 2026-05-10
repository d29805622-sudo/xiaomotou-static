// 小魔头同人创作平台 - 脚本文件

// 主题切换
const themeBtn = document.getElementById('themeBtn');
if (themeBtn) {
    themeBtn.addEventListener('click', function() {
        document.body.classList.toggle('light-theme');
        
        // 保存主题偏好
        const isLight = document.body.classList.contains('light-theme');
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
        
        // 更新图标
        if (isLight) {
            themeBtn.classList.remove('fa-moon');
            themeBtn.classList.add('fa-sun');
        } else {
            themeBtn.classList.remove('fa-sun');
            themeBtn.classList.add('fa-moon');
        }
    });
    
    // 恢复主题偏好
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        themeBtn.classList.remove('fa-moon');
        themeBtn.classList.add('fa-sun');
    }
}

// 模拟在线人数更新
function updateOnlineNum() {
    const onlineNum = document.getElementById('onlineNum');
    if (onlineNum) {
        const base = 236;
        const random = Math.floor(Math.random() * 20) - 10;
        onlineNum.textContent = base + random;
    }
}

// 模拟今日访问量更新
function updateVisitNum() {
    const visitNum = document.getElementById('visitNum');
    if (visitNum) {
        const base = 5218;
        const random = Math.floor(Math.random() * 50);
        visitNum.textContent = base + random;
    }
}

// 定时更新数据
setInterval(updateOnlineNum, 30000);
setInterval(updateVisitNum, 60000);

// 搜索功能
const searchBtn = document.querySelector('.search-btn');
if (searchBtn) {
    searchBtn.addEventListener('click', function() {
        const searchInput = document.querySelector('.search-input');
        const keyword = searchInput.value.trim();
        
        if (keyword) {
            alert(`正在搜索："${keyword}"\n\n搜索功能演示中，实际功能需要后端支持`);
            // window.location.href = `search.html?q=${encodeURIComponent(keyword)}`;
        } else {
            alert('请输入搜索关键词');
        }
    });
}

// 收藏功能
const collectBtns = document.querySelectorAll('.collect-btn');
collectBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        
        const icon = this.querySelector('i');
        if (icon.classList.contains('fa-heart')) {
            icon.classList.remove('fa-heart');
            icon.classList.add('fa-heart-crack');
            this.style.background = 'var(--primary-color)';
            alert('已取消收藏');
        } else {
            icon.classList.remove('fa-heart-crack');
            icon.classList.add('fa-heart');
            this.style.background = 'rgba(255, 107, 157, 0.2)';
            alert('已添加到收藏夹');
        }
    });
});

// 悬浮看板娘点击效果
const kanban = document.querySelector('.kanban');
if (kanban) {
    kanban.addEventListener('click', function() {
        const img = this.querySelector('img');
        img.style.transform = 'scale(1.2) rotate(10deg)';
        setTimeout(() => {
            img.style.transform = 'scale(1) rotate(0deg)';
        }, 300);
    });
}

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const target = this.getAttribute('href');
        if (target !== '#') {
            e.preventDefault();
            const element = document.querySelector(target);
            if (element) {
                element.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        }
    });
});

// 回到顶部功能
const topBtn = document.querySelector('.tool-item:first-child');
if (topBtn) {
    topBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// 页面加载动画
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.5s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// 导航菜单移动端适配
const navMenu = document.querySelector('.nav-menu');
if (navMenu) {
    let touchStartX = 0;
    let touchEndX = 0;
    
    navMenu.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    });
    
    navMenu.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                navMenu.scrollLeft += 100;
            } else {
                navMenu.scrollLeft -= 100;
            }
        }
    }
}

// 表单验证（如果有登录/注册表单）
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function(e) {
        const inputs = this.querySelectorAll('input[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = '#ff6b9d';
            } else {
                input.style.borderColor = '';
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            alert('请填写所有必填项');
        }
    });
});

// 控制台欢迎信息
console.log('%c🎮 小魔头同人创作平台', 'font-size: 24px; color: #ff6b9d; font-weight: bold;');
console.log('%c欢迎来到同人创作的世界！', 'font-size: 14px; color: #a855f7;');
console.log('%c技术支持：纯静态网站演示', 'font-size: 12px; color: #666;');
