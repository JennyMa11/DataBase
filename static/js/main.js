document.addEventListener('DOMContentLoaded', function() {
    // 自动隐藏提示消息
    setTimeout(function() {
        var alerts = document.getElementsByClassName('alert');
        for (var i = 0; i < alerts.length; i++) {
            alerts[i].style.display = 'none';
        }
    }, 5000);

    // 购物车数量验证
    var quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            if (this.value < 1) {
                this.value = 1;
            }
        });
    });

    // 为卡片添加淡入动画
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('animate-fade-in');
        }, index * 100);
    });
});

// 退出登录确认
document.addEventListener('DOMContentLoaded', function() {
    const logoutLink = document.querySelector('a[href*="logout"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 创建确认模态框
            const confirmModal = document.createElement('div');
            confirmModal.innerHTML = `
                <div class="modal fade" id="logoutModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">确认退出</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <p>您确定要退出登录吗？</p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                                <button type="button" class="btn btn-danger" id="confirmLogout">确认退出</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(confirmModal);
            
            const modal = new bootstrap.Modal(document.getElementById('logoutModal'));
            modal.show();
            
            // 确认退出按钮事件
            document.getElementById('confirmLogout').addEventListener('click', function() {
                window.location.href = logoutLink.href;
            });
            
            // 模态框关闭后移除元素
            document.getElementById('logoutModal').addEventListener('hidden.bs.modal', function() {
                document.body.removeChild(confirmModal);
            });
        });
    }
});

// 购物车数量增减动画
function animateCartUpdate() {
    const cartButtons = document.querySelectorAll('.add-to-cart');
    cartButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 添加点击动画
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
}

// 搜索框自动完成效果
function initSearchAutocomplete() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            // 可以在这里添加搜索建议功能
            this.style.borderColor = this.value ? '#667eea' : '';
        });
    }
}

// 价格格式化
function formatPrices() {
    const priceElements = document.querySelectorAll('.price');
    priceElements.forEach(element => {
        const price = parseFloat(element.textContent);
        if (!isNaN(price)) {
            element.textContent = `¥${price.toFixed(2)}`;
        }
    });
}

// 表单验证增强
function enhanceFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#ff6b6b';
                    isValid = false;
                } else {
                    field.style.borderColor = '#11998e';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('请填写所有必填字段！');
            }
        });
    });
}

// 初始化所有功能
document.addEventListener('DOMContentLoaded', function() {
    animateCartUpdate();
    initSearchAutocomplete();
    formatPrices();
    enhanceFormValidation();
});

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});