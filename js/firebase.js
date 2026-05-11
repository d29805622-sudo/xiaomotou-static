// Firebase 配置和初始化
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.13.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/12.13.0/firebase-auth.js";
import { getDatabase, ref, set, get, child, update, remove } from "https://www.gstatic.com/firebasejs/12.13.0/firebase-database.js";

// Firebase 配置
const firebaseConfig = {
    apiKey: "AIzaSyD5KglKIReKoSCTb2oIsPM-ei2hWVSoJ94",
    authDomain: "xmt-play.firebaseapp.com",
    databaseURL: "https://xmt-play-default-rtdb.firebaseio.com",
    projectId: "xmt-play",
    storageBucket: "xmt-play.firebasestorage.app",
    messagingSenderId: "157977593826",
    appId: "1:157977593826:web:01c3715943552a579adbbb"
};

// 初始化 Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getDatabase(app);

// 导出功能
window.FirebaseApp = {
    // 注册用户
    async register(email, password, username) {
        try {
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            
            // 保存用户信息到数据库
            await set(ref(db, 'users/' + user.uid), {
                email: email,
                username: username,
                createdAt: new Date().toISOString(),
                stats: {
                    posts: 0,
                    favorites: 0,
                    points: 0,
                    signDays: 0
                }
            });
            
            return { success: true, user: user };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },
    
    // 登录用户
    async login(email, password) {
        try {
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            
            // 获取用户信息
            const snapshot = await get(child(ref(db), `users/${user.uid}`));
            const userData = snapshot.exists() ? snapshot.val() : {};
            
            // 保存到本地存储
            localStorage.setItem('currentUser', JSON.stringify({
                uid: user.uid,
                email: user.email,
                username: userData.username || '用户'
            }));
            
            return { success: true, user: user, userData: userData };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },
    
    // 退出登录
    async logout() {
        try {
            await signOut(auth);
            localStorage.removeItem('currentUser');
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },
    
    // 检查登录状态
    checkLogin() {
        return new Promise((resolve) => {
            onAuthStateChanged(auth, (user) => {
                if (user) {
                    resolve({ loggedIn: true, user: user });
                } else {
                    resolve({ loggedIn: false, user: null });
                }
            });
        });
    },
    
    // 获取当前用户
    getCurrentUser() {
        return auth.currentUser;
    },
    
    // 获取用户信息
    async getUserData(uid) {
        try {
            const snapshot = await get(child(ref(db), `users/${uid}`));
            return snapshot.exists() ? snapshot.val() : null;
        } catch (error) {
            console.error('获取用户数据失败:', error);
            return null;
        }
    },
    
    // 签到
    async signIn(uid) {
        const today = new Date().toISOString().split('T')[0];
        
        try {
            // 获取当前签到数据
            const snapshot = await get(child(ref(db), `signData/${uid}`));
            const signData = snapshot.exists() ? snapshot.val() : {
                dates: [],
                streak: 0,
                lastSignDate: null
            };
            
            // 检查今天是否已签到
            if (signData.dates.includes(today)) {
                return { success: false, message: '今日已签到' };
            }
            
            // 更新签到数据
            signData.dates.push(today);
            signData.lastSignDate = today;
            
            // 计算连续签到
            const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
            if (signData.lastSignDate === yesterday) {
                signData.streak++;
            } else {
                signData.streak = 1;
            }
            
            // 保存到数据库
            await set(ref(db, `signData/${uid}`), signData);
            
            // 更新用户积分
            const points = 5 + Math.min(signData.streak * 2, 15);
            await this.updateUserPoints(uid, points);
            
            return { success: true, streak: signData.streak, totalDays: signData.dates.length, points: points };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },
    
    // 获取签到数据
    async getSignData(uid) {
        try {
            const snapshot = await get(child(ref(db), `signData/${uid}`));
            return snapshot.exists() ? snapshot.val() : { dates: [], streak: 0, lastSignDate: null };
        } catch (error) {
            return { dates: [], streak: 0, lastSignDate: null };
        }
    },
    
    // 更新用户积分
    async updateUserPoints(uid, points) {
        try {
            const snapshot = await get(child(ref(db), `users/${uid}`));
            if (snapshot.exists()) {
                const userData = snapshot.val();
                const currentPoints = userData.stats?.points || 0;
                await update(ref(db, `users/${uid}/stats`), {
                    points: currentPoints + points
                });
            }
        } catch (error) {
            console.error('更新积分失败:', error);
        }
    },
    
    // 添加收藏
    async addFavorite(uid, item) {
        try {
            const favoritesRef = ref(db, `favorites/${uid}`);
            const snapshot = await get(favoritesRef);
            const favorites = snapshot.exists() ? snapshot.val() : [];
            
            // 检查是否已存在
            if (!favorites.find(f => f.id === item.id)) {
                favorites.push(item);
                await set(favoritesRef, favorites);
                await update(ref(db, `users/${uid}/stats`), { favorites: favorites.length });
            }
            
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },
    
    // 获取收藏列表
    async getFavorites(uid) {
        try {
            const snapshot = await get(child(ref(db), `favorites/${uid}`));
            return snapshot.exists() ? snapshot.val() : [];
        } catch (error) {
            return [];
        }
    },
    
    // 移除收藏
    async removeFavorite(uid, itemId) {
        try {
            const favoritesRef = ref(db, `favorites/${uid}`);
            const snapshot = await get(favoritesRef);
            const favorites = snapshot.exists() ? snapshot.val() : [];
            const filtered = favorites.filter(f => f.id !== itemId);
            await set(favoritesRef, filtered);
            await update(ref(db, `users/${uid}/stats`), { favorites: filtered.length });
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },
    
    // 发布帖子
    async createPost(uid, title, content) {
        try {
            const postId = Date.now().toString();
            const postData = {
                id: postId,
                uid: uid,
                title: title,
                content: content,
                createdAt: new Date().toISOString(),
                likes: [],
                comments: []
            };
            
            await set(ref(db, `posts/${postId}`), postData);
            
            // 更新用户发帖数
            const snapshot = await get(child(ref(db), `users/${uid}`));
            if (snapshot.exists()) {
                const userData = snapshot.val();
                const posts = userData.stats?.posts || 0;
                await update(ref(db, `users/${uid}/stats`), { posts: posts + 1 });
            }
            
            return { success: true, postId: postId };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },
    
    // 获取帖子列表
    async getPosts() {
        try {
            const snapshot = await get(child(ref(db), 'posts'));
            if (snapshot.exists()) {
                const posts = snapshot.val();
                return Object.values(posts).sort((a, b) => 
                    new Date(b.createdAt) - new Date(a.createdAt)
                );
            }
            return [];
        } catch (error) {
            return [];
        }
    },
    
    // 点赞帖子
    async toggleLike(postId, uid) {
        try {
            const postRef = ref(db, `posts/${postId}`);
            const snapshot = await get(postRef);
            if (snapshot.exists()) {
                const post = snapshot.val();
                const likes = post.likes || [];
                
                if (likes.includes(uid)) {
                    post.likes = likes.filter(id => id !== uid);
                } else {
                    post.likes.push(uid);
                }
                
                await set(postRef, post);
                return { success: true, likes: post.likes.length, liked: post.likes.includes(uid) };
            }
            return { success: false };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },
    
    // 添加评论
    async addComment(postId, uid, content) {
        try {
            const postRef = ref(db, `posts/${postId}`);
            const snapshot = await get(postRef);
            if (snapshot.exists()) {
                const post = snapshot.val();
                const comments = post.comments || [];
                
                comments.push({
                    id: Date.now().toString(),
                    uid: uid,
                    content: content,
                    createdAt: new Date().toISOString()
                });
                
                await update(ref(db, `posts/${postId}`), { comments: comments });
                return { success: true };
            }
            return { success: false };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },
    
    // 提交反馈
    async submitFeedback(uid, type, content, contact) {
        try {
            const feedbackId = Date.now().toString();
            const feedbackData = {
                id: feedbackId,
                uid: uid,
                type: type,
                content: content,
                contact: contact,
                createdAt: new Date().toISOString(),
                status: 'pending'
            };
            
            await set(ref(db, `feedback/${feedbackId}`), feedbackData);
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },
    
    // 获取用户反馈
    async getFeedback(uid) {
        try {
            const snapshot = await get(child(ref(db), 'feedback'));
            if (snapshot.exists()) {
                const feedbacks = snapshot.val();
                return Object.values(feedbacks)
                    .filter(f => f.uid === uid)
                    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
            }
            return [];
        } catch (error) {
            return [];
        }
    }
};
