from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from config import Config
from models import db, login_manager
from models.user import User
from models.food import Food
from models.cart import Cart
from models.order import Order
from datetime import datetime
import random


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/admin')
    @login_required
    def admin():
        user = User.query.get(current_user.user_id)
        if user.role != 'admin':
            flash('没有权限访问该页面！')
            return redirect(url_for('index'))

        # 获取统计数据
        foods = Food.query.all()
        orders = Order.query.order_by(Order.order_date.desc()).limit(10).all()
        users = User.query.all()
        
        # 统计信息
        stats = {
            'total_foods': len(foods),
            'total_orders': Order.query.count(),
            'total_users': len(users),
            'total_revenue': sum([order.total_price for order in Order.query.all()])
        }
        
        return render_template('admin_dashboard.html', foods=foods, orders=orders, users=users, stats=stats)

    # 管理员添加菜品
    @app.route('/admin/add_food', methods=['POST'])
    @login_required
    def add_food():
        user = User.query.get(current_user.user_id)
        if user.role != 'admin':
            flash('没有权限执行此操作！')
            return redirect(url_for('home'))
        
        try:
            name = request.form.get('name')
            price = request.form.get('price')
            description = request.form.get('description', '')
            image_url = request.form.get('image_url', '')
            
            # 验证必填字段
            if not name or not price:
                flash('菜品名称和价格不能为空！')
                return redirect(url_for('admin'))
            
            # 验证价格
            try:
                price = float(price)
                if price <= 0:
                    flash('价格必须大于0！')
                    return redirect(url_for('admin'))
            except ValueError:
                flash('价格格式不正确！')
                return redirect(url_for('admin'))
            
            # 检查菜品名称是否已存在
            existing_food = Food.query.filter_by(name=name).first()
            if existing_food:
                flash(f'菜品"{name}"已存在！')
                return redirect(url_for('admin'))
            
            # 创建新菜品
            new_food = Food(
                name=name,
                price=price,
                description=description if description else f'美味的{name}',
                image_url=image_url if image_url else None
            )
            
            db.session.add(new_food)
            db.session.commit()
            
            flash(f'菜品"{name}"添加成功！')
            return redirect(url_for('admin'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'添加菜品失败：{str(e)}')
            return redirect(url_for('admin'))

    # 管理员删除菜品
    @app.route('/admin/delete_food/<int:food_id>')
    @login_required
    def delete_food(food_id):
        user = User.query.get(current_user.user_id)
        if user.role != 'admin':
            flash('没有权限执行此操作！')
            return redirect(url_for('home'))
        
        try:
            food = Food.query.get_or_404(food_id)
            food_name = food.name
            
            # 检查是否有相关的购物车项目
            cart_items = Cart.query.filter_by(food_id=food_id).all()
            if cart_items:
                flash(f'无法删除菜品"{food_name}"，因为有用户购物车中包含此菜品！')
                return redirect(url_for('admin'))
            
            db.session.delete(food)
            db.session.commit()
            
            flash(f'菜品"{food_name}"删除成功！')
            return redirect(url_for('admin'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'删除菜品失败：{str(e)}')
            return redirect(url_for('admin'))

    # 主页 - 显示随机菜品
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

    # 首页 - 显示随机推荐菜品
    @app.route('/home')
    @login_required
    def home():
        # 随机选择6个菜品进行推荐
        all_foods = Food.query.all()
        featured_foods = random.sample(all_foods, min(6, len(all_foods))) if all_foods else []
        return render_template('home.html', featured_foods=featured_foods)

    # 菜单页 - 显示所有菜品
    @app.route('/menu')
    @login_required
    def menu():
        search = request.args.get('search', '')
        if search:
            foods = Food.query.filter(Food.name.contains(search)).all()
        else:
            foods = Food.query.all()
        return render_template('menu.html', foods=foods, search=search)

    # 用户注册
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            phone_number = request.form['phone_number']

            # 检查用户名是否已存在
            if User.query.filter_by(username=username).first():
                flash('用户名已存在！')
                return render_template('register.html')

            # 创建新用户
            user = User(username=username, phone_number=phone_number)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash('注册成功！请登录。')
            return redirect(url_for('login'))

        return render_template('register.html')

    # 用户登录
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('用户名或密码错误！')

        return render_template('login.html')

    # 用户登出
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    # 添加到购物车
    @app.route('/add_to_cart/<int:food_id>')
    @login_required
    def add_to_cart(food_id):
        food = Food.query.get_or_404(food_id)

        # 检查购物车中是否已有该菜品
        cart_item = Cart.query.filter_by(user_id=current_user.user_id, food_id=food_id).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.total_price = cart_item.quantity * float(food.price)
        else:
            cart_item = Cart(
                user_id=current_user.user_id,
                food_id=food_id,
                quantity=1,
                total_price=float(food.price)
            )
            db.session.add(cart_item)

        db.session.commit()
        flash(f'{food.name} 已添加到购物车！')
        return redirect(request.referrer or url_for('home'))

    # 查看购物车
    @app.route('/cart')
    @login_required
    def view_cart():
        cart_items = db.session.query(Cart, Food).join(Food).filter(Cart.user_id == current_user.user_id).all()
        total = sum(item[0].total_price for item in cart_items)
        return render_template('cart.html', cart_items=cart_items, total=total)

    # 更新购物车数量
    @app.route('/update_cart/<int:cart_id>', methods=['POST'])
    @login_required
    def update_cart(cart_id):
        cart_item = Cart.query.get_or_404(cart_id)
        if cart_item.user_id != current_user.user_id:
            flash('无权限操作！')
            return redirect(url_for('view_cart'))

        quantity = int(request.form['quantity'])
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.total_price = quantity * float(cart_item.food.price)
            db.session.commit()
        else:
            db.session.delete(cart_item)
            db.session.commit()

        return redirect(url_for('view_cart'))

    # 删除购物车项
    @app.route('/remove_from_cart/<int:cart_id>')
    @login_required
    def remove_from_cart(cart_id):
        cart_item = Cart.query.get_or_404(cart_id)
        if cart_item.user_id != current_user.user_id:
            flash('无权限操作！')
            return redirect(url_for('view_cart'))

        db.session.delete(cart_item)
        db.session.commit()
        flash('已从购物车移除！')
        return redirect(url_for('view_cart'))

    # 结算
    @app.route('/checkout', methods=['GET', 'POST'])
    @login_required
    def checkout():
        if request.method == 'POST':
            try:
                # 调用存储过程，结算用户购物车
                db.session.execute(text('CALL checkout_user_cart(:user_id)'), {'user_id': current_user.user_id})
                flash('订单已成功提交！感谢您的购买。')
                # 跳转到订单页面，避免重复支付
                return redirect(url_for('my_orders'))  # 跳转到用户的订单页面
            except Exception as e:
                db.session.rollback()
                flash(f'结算失败，请重试！错误信息：{str(e)}')
                return redirect(url_for('view_cart'))  # 如果结算失败，跳转回购物车页面

        # 显示结算页面，获取购物车信息和计算总价
        try:
            # 直接从购物车中获取商品信息
            cart_items = db.session.query(Cart, Food).join(Food).filter(Cart.user_id == current_user.user_id).all()

            # 如果购物车为空，提示用户并跳转
            if not cart_items:
                flash('购物车为空！')
                return redirect(url_for('home'))

            # 计算购物车总金额
            total_amount = sum(item[0].total_price for item in cart_items)

            # 如果购物车总金额为 0，跳转到首页
            if total_amount == 0:
                flash('购物车为空！')
                return redirect(url_for('home'))

        # 渲染结算页面
            return render_template('checkout.html', cart_items=cart_items, total=total_amount)
        except Exception as e:
            flash(f'结算页面加载失败，请重试！错误信息：{str(e)}')
            return redirect(url_for('home'))

    # 我的订单
    @app.route('/my_orders')
    @login_required
    def my_orders():
        orders = Order.query.filter_by(user_id=current_user.user_id).order_by(Order.order_date.desc()).all()
        return render_template('my_orders.html', orders=orders)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()

        # 初始化示例数据（如果菜品表为空）
        if Food.query.count() == 0:
            sample_foods = [
                Food(name='汉堡包', description='经典牛肉汉堡', price=15.00),
                Food(name='炸鸡', description='香脆炸鸡', price=12.00),
                Food(name='薯条', description='金黄薯条', price=8.00),
                Food(name='可乐', description='冰镇可乐', price=5.00),
                Food(name='披萨', description='意式披萨', price=25.00),
            ]
            for food in sample_foods:
                db.session.add(food)
            db.session.commit()

        # 创建默认管理员用户（如果不存在）
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                phone_number='13800138000',
                role='admin'
            )
            admin_user.set_password('admin123')  # 默认密码
            db.session.add(admin_user)
            db.session.commit()
            print("已创建默认管理员账户: admin/admin123")

    app.run(debug=True)
