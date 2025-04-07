import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymysql
from pymysql import Error


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("系统登录")
        self.setFixedSize(400, 300)

        # 数据库连接配置（请根据实际情况修改）
        self.db_config = {
            'host': 'rm-2ze0mr80dxyl91832oo.mysql.rds.aliyuncs.com',
            'port':3306,
            'user': 'hww',
            'password': 'Huangwaiwai666',
            'database': 'mystore',
            'cursorclass': pymysql.cursors.DictCursor
        }

        # 主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 布局
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # 标题
        self.title_label = QLabel("欢迎登录")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.main_layout.addWidget(self.title_label)

        # 用户类型选择
        self.user_type_label = QLabel("用户类型：")
        self.user_type_combo = QComboBox()
        self.user_type_combo.addItems(["顾客", "店员"])

        type_layout = QHBoxLayout()
        type_layout.addWidget(self.user_type_label)
        type_layout.addWidget(self.user_type_combo)
        self.main_layout.addLayout(type_layout)

        # 用户名输入
        self.username_label = QLabel("用户名：")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")

        username_layout = QHBoxLayout()
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_input)
        self.main_layout.addLayout(username_layout)

        # 密码输入
        self.password_label = QLabel("密码：")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.Password)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)
        self.main_layout.addLayout(password_layout)

        # 按钮
        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white;")

        self.main_layout.addWidget(self.login_button)

        # 添加一些间距
        self.main_layout.addSpacing(20)

    # 将 ProductWindow 类移出 LoginWindow 类
    class ProductWindow(QMainWindow):
        def __init__(self, username):
            super().__init__()
            self.username = username
            self.setWindowTitle(f"一家售卖女装的小店 - 欢迎 {username}")
            self.setFixedSize(1200, 800)  # 扩大窗口尺寸
            
            # 数据库配置（复用登录窗口的配置）
            self.db_config = {
                'host': 'rm-2ze0mr80dxyl91832oo.mysql.rds.aliyuncs.com',
                'port': 3306,
                'user': 'hww',
                'password': 'Huangwaiwai666',
                'database': 'mystore',
                'cursorclass': pymysql.cursors.DictCursor
            }
            
            # 先定义方法需要使用的属性
            self.scroll_layout = None
            self.cart_scroll_layout = None
            self.orders_scroll_layout = None
            
            self.init_ui()
            # self.load_products()  # 现在这个方法已经被定义了
        
        def init_ui(self):
            # 主布局改为水平布局
            self.main_widget = QWidget()
            self.setCentralWidget(self.main_widget)
            self.main_layout = QHBoxLayout(self.main_widget)
            
            # 左侧选项卡
            self.tab_bar = QTabWidget()
            self.tab_bar.setTabPosition(QTabWidget.West)
            self.tab_bar.setStyleSheet("""
                QTabBar::tab {
                    width: 120px;
                    height: 180px;
                    font-size: 22px;
                }
            """)
            
            # 创建四个选项卡页面
            self.products_tab = QWidget()
            self.cart_tab = QWidget()
            self.orders_tab = QWidget()
            self.profile_tab = QWidget()
            
            # 添加选项卡
            self.tab_bar.addTab(self.products_tab, "浏览商品")
            self.tab_bar.addTab(self.cart_tab, "我的购物车")
            self.tab_bar.addTab(self.orders_tab, "我的订单")
            self.tab_bar.addTab(self.profile_tab, "个人信息")
            
            # 初始化各选项卡内容
            self.init_products_tab()
            self.init_cart_tab()
            self.init_orders_tab()
            self.init_profile_tab()
            
            self.main_layout.addWidget(self.tab_bar, stretch=1) #不知道什么意思
            # self.main_layout.addStretch(1)
        
        def init_products_tab(self):
            # 商品浏览页（原商品展示功能）
            layout = QVBoxLayout(self.products_tab)
            
            self.title_label = QLabel("商品列表")
            self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
            self.title_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.title_label)
            
            self.scroll_area = QScrollArea()
            self.scroll_content = QWidget()
            self.scroll_layout = QVBoxLayout(self.scroll_content)
            
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setWidget(self.scroll_content)
            
            layout.addWidget(self.scroll_area)
            self.load_products()  # 调用加载商品方法

        # 将load_products方法移到类级别
        def load_products(self):
            try:
                # 清空现有商品列表
                for i in reversed(range(self.scroll_layout.count())): 
                    self.scroll_layout.itemAt(i).widget().setParent(None)
                
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT product_id, name, description, main_image FROM products")
                    products = cursor.fetchall()
                    
                    for product in products:
                        self.add_product_item(product)
            except Error as e:
                QMessageBox.critical(self, "错误", f"加载商品失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
        
        def add_product_item(self, product):
            item_frame = QFrame()
            item_frame.setFrameShape(QFrame.StyledPanel)
            item_frame.setStyleSheet("margin: 10px; padding: 10px;")
            
            layout = QHBoxLayout(item_frame)
            
            # 商品图片
            if product['main_image']:
                image_label = QLabel()
                try:
                    pixmap = QPixmap(product['main_image'])
                    if not pixmap.isNull():
                        image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
                        layout.addWidget(image_label)
                except Exception as e:
                    print(f"图片加载错误：{str(e)}")
            
            # 商品信息
            info_layout = QVBoxLayout()
            
            name_label = QLabel(product['name'])
            name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
            info_layout.addWidget(name_label)
            
            desc_label = QLabel(product['description'])
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
            
            layout.addLayout(info_layout)
            
            # 查看详情按钮
            detail_btn = QPushButton("查看详情")
            detail_btn.clicked.connect(lambda: self.show_product_details(product))
            layout.addWidget(detail_btn)
            
            self.scroll_layout.addWidget(item_frame)
        
        def show_product_details(self, product):
            # 保存当前商品信息
            self.current_product = product
            # 商品详情对话框
            dialog = QDialog(self)
            dialog.setWindowTitle(product['name'])
            dialog.setFixedSize(600, 500)
            
            layout = QVBoxLayout(dialog)
            
            # 商品图片
            if product['main_image']:
                image_label = QLabel()
                try:
                    pixmap = QPixmap(product['main_image'])
                    if not pixmap.isNull():
                        image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
                        image_label.setAlignment(Qt.AlignCenter)
                        layout.addWidget(image_label)
                except Exception as e:
                    print(f"图片加载错误：{str(e)}")
            
            # 商品信息
            name_label = QLabel(product['name'])
            name_label.setStyleSheet("font-size: 24px; font-weight: bold;")
            name_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(name_label)
            
            desc_label = QLabel(product['description'])
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
            
            # 添加规格选择控件
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    # 查询商品的所有规格类型
                    cursor.execute("""
                        SELECT DISTINCT st.spec_type_id, st.name
                        FROM spec_types st
                        JOIN spec_values sv ON st.spec_type_id = sv.spec_type_id
                        JOIN sku_specs ss ON sv.spec_value_id = ss.spec_value_id
                        JOIN skus s ON ss.sku_id = s.sku_id
                        WHERE s.product_id = %s
                        ORDER BY st.spec_type_id
                    """, (product['product_id'],))
                    spec_types = cursor.fetchall()
                    
                    if not spec_types:
                        QMessageBox.information(self, "提示", "该商品暂无规格信息")
                        return
                    
                    self.spec_combos = {}
                    for spec_type in spec_types:
                        # 查询该规格类型下所有可用的规格值
                        cursor.execute("""
                            SELECT DISTINCT sv.spec_value_id, sv.value
                            FROM spec_values sv
                            JOIN sku_specs ss ON sv.spec_value_id = ss.spec_value_id
                            JOIN skus s ON ss.sku_id = s.sku_id
                            WHERE s.product_id = %s AND sv.spec_type_id = %s
                            ORDER BY sv.spec_value_id
                        """, (product['product_id'], spec_type['spec_type_id']))
                        spec_values = cursor.fetchall()
                        
                        if not spec_values:
                            continue
                            
                        # 创建下拉框
                        hbox = QHBoxLayout()
                        label = QLabel(spec_type['name'] + ":")
                        combo = QComboBox()
                        for value in spec_values:
                            combo.addItem(value['value'], value['spec_value_id'])
                        
                        hbox.addWidget(label)
                        hbox.addWidget(combo)
                        layout.addLayout(hbox)
                        self.spec_combos[spec_type['spec_type_id']] = combo
                        
                        # 添加选择变化事件
                        combo.currentIndexChanged.connect(self.update_sku_info)
                    
                    # 添加SKU信息显示区域
                    self.sku_info_label = QLabel("请选择完整规格")
                    self.sku_info_label.setStyleSheet("font-size: 16px; color: #FF9800;")
                    layout.addWidget(self.sku_info_label)
                    
            except Error as e:
                QMessageBox.critical(self, "错误", f"加载规格信息失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
            
            # 添加到购物车按钮
            add_to_cart_btn = QPushButton("添加到购物车")
            add_to_cart_btn.clicked.connect(lambda: self.add_to_cart(product))
            layout.addWidget(add_to_cart_btn)
            
            dialog.exec_()
        
        def init_cart_tab(self):
            # 购物车页实现
            layout = QVBoxLayout(self.cart_tab)
            
            self.cart_title_label = QLabel("我的购物车")
            self.cart_title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
            self.cart_title_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.cart_title_label)
            
            # 购物车商品列表
            self.cart_scroll_area = QScrollArea()
            self.cart_scroll_content = QWidget()
            self.cart_scroll_layout = QVBoxLayout(self.cart_scroll_content)
            
            self.cart_scroll_area.setWidgetResizable(True)
            self.cart_scroll_area.setWidget(self.cart_scroll_content)
            layout.addWidget(self.cart_scroll_area)
            
            # 结算按钮
            self.checkout_button = QPushButton("结算")
            self.checkout_button.setStyleSheet("background-color: #FF5722; color: white; font-size: 18px;")
            self.checkout_button.clicked.connect(self.handle_checkout)
            layout.addWidget(self.checkout_button)
            
            self.load_cart_items()
        
        def init_orders_tab(self):
            # 订单页实现
            layout = QVBoxLayout(self.orders_tab)
            
            self.orders_title_label = QLabel("我的订单")
            self.orders_title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
            self.orders_title_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.orders_title_label)
            
            # 订单列表
            self.orders_scroll_area = QScrollArea()
            self.orders_scroll_content = QWidget()
            self.orders_scroll_layout = QVBoxLayout(self.orders_scroll_content)
            
            self.orders_scroll_area.setWidgetResizable(True)
            self.orders_scroll_area.setWidget(self.orders_scroll_content)
            layout.addWidget(self.orders_scroll_area)
            
            self.load_orders()
        
        def init_profile_tab(self):
            # 个人信息页实现
            layout = QVBoxLayout(self.profile_tab)
            
            self.profile_title_label = QLabel("个人信息")
            self.profile_title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
            self.profile_title_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.profile_title_label)
            
            # 个人信息表单
            form_layout = QFormLayout()
            
            # 用户名
            self.username_label = QLabel(self.username)
            form_layout.addRow("用户名:", self.username_label)
            
            # 其他信息（可根据需要从数据库查询）
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM customers WHERE username = %s", (self.username,))
                    customer = cursor.fetchone()
                    
                    if customer:
                        # 显示用户信息
                        self.name_label = QLabel(customer.get('name', '未设置'))
                        self.phone_label = QLabel(customer.get('phone', '未设置'))
                        self.address_label = QLabel(customer.get('address', '未设置'))
                        
                        form_layout.addRow("姓名:", self.name_label)
                        form_layout.addRow("电话:", self.phone_label)
                        form_layout.addRow("地址:", self.address_label)
            except Error as e:
                QMessageBox.critical(self, "错误", f"加载个人信息失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
            
            layout.addLayout(form_layout)
            layout.addStretch()
        def load_cart_items(self):
            try:
                # 清空现有购物车列表
                for i in reversed(range(self.cart_scroll_layout.count())): 
                    self.cart_scroll_layout.itemAt(i).widget().setParent(None)
                
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    # 获取用户ID
                    cursor.execute("SELECT customer_id FROM customers WHERE username = %s", (self.username,))
                    customer = cursor.fetchone()
                    
                    if customer:
                        # 查询购物车及商品信息
                        cursor.execute("""
                            SELECT ci.cart_item_id, ci.quantity, 
                                   s.sku_id, s.price, s.stock,
                                   p.name, p.description, p.main_image
                            FROM cart_items ci
                            JOIN carts c ON ci.cart_id = c.cart_id
                            JOIN skus s ON ci.sku_id = s.sku_id
                            JOIN products p ON s.product_id = p.product_id
                            WHERE c.customer_id = %s
                        """, (customer['customer_id'],))
                        cart_items = cursor.fetchall()
                        
                        for item in cart_items:
                            self.add_cart_item(item)
            except Error as e:
                QMessageBox.critical(self, "错误", f"加载购物车失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
        
        def add_cart_item(self, item):
            item_frame = QFrame()
            item_frame.setFrameShape(QFrame.StyledPanel)
            item_frame.setStyleSheet("margin: 10px; padding: 10px;")
            
            layout = QHBoxLayout(item_frame)
            
            # 商品图片
            if item['main_image']:
                image_label = QLabel()
                try:
                    pixmap = QPixmap(item['main_image'])
                    if not pixmap.isNull():
                        image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
                        layout.addWidget(image_label)
                except Exception as e:
                    print(f"图片加载错误：{str(e)}")
            
            # 商品信息
            info_layout = QVBoxLayout()
            
            name_label = QLabel(item['name'])
            name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
            info_layout.addWidget(name_label)
            
            # 添加SKU规格信息
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT sv.value, st.name
                        FROM sku_specs ss
                        JOIN spec_values sv ON ss.spec_value_id = sv.spec_value_id
                        JOIN spec_types st ON sv.spec_type_id = st.spec_type_id
                        WHERE ss.sku_id = %s
                        ORDER BY st.spec_type_id
                    """, (item['sku_id'],))
                    specs = cursor.fetchall()
                    
                    if specs:
                        spec_text = " | ".join([f"{spec['name']}:{spec['value']}" for spec in specs])
                        spec_label = QLabel(spec_text)
                        spec_label.setWordWrap(True)  # 添加自动换行
                        info_layout.addWidget(spec_label)
            except Error as e:
                print(f"加载规格信息失败: {str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
            
            price_label = QLabel(f"价格: ¥{item['price']}")
            info_layout.addWidget(price_label)
            
            quantity_layout = QHBoxLayout()
            quantity_label = QLabel("数量:")
            quantity_spin = QSpinBox()
            quantity_spin.setRange(1, item['stock'])
            quantity_spin.setValue(item['quantity'])
            quantity_spin.valueChanged.connect(lambda value, item_id=item['cart_item_id']: self.update_cart_item_quantity(item_id, value))
            
            quantity_layout.addWidget(quantity_label)
            quantity_layout.addWidget(quantity_spin)
            info_layout.addLayout(quantity_layout)
            
            layout.addLayout(info_layout)
            
            # 删除按钮
            delete_btn = QPushButton("删除")
            delete_btn.setStyleSheet("background-color: #F44336; color: white;")
            delete_btn.clicked.connect(lambda _, item_id=item['cart_item_id']: self.remove_cart_item(item_id))
            layout.addWidget(delete_btn)
            
            self.cart_scroll_layout.addWidget(item_frame)
        
        def load_orders(self):
            try:
                # 清空现有订单列表
                for i in reversed(range(self.orders_scroll_layout.count())): 
                    self.orders_scroll_layout.itemAt(i).widget().setParent(None)
                
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    # 获取用户ID
                    cursor.execute("SELECT customer_id FROM customers WHERE username = %s", (self.username,))
                    customer = cursor.fetchone()
                    
                    if customer:
                        # 查询订单及商品信息
                        cursor.execute("""
                            SELECT o.order_id, o.status, o.created_at, 
                                   o.shipped_at, o.delivered_at, o.tracking_number,
                                   oi.order_item_id, oi.quantity, oi.price_at_order,
                                   p.name, p.main_image
                            FROM orders o
                            JOIN order_items oi ON o.order_id = oi.order_id
                            JOIN skus s ON oi.sku_id = s.sku_id
                            JOIN products p ON s.product_id = p.product_id
                            WHERE o.customer_id = %s
                            ORDER BY o.created_at DESC
                        """, (customer['customer_id'],))
                        orders = cursor.fetchall()
                        
                        # 按订单ID分组
                        orders_dict = {}
                        for item in orders:
                            if item['order_id'] not in orders_dict:
                                orders_dict[item['order_id']] = {
                                    'order_info': item,
                                    'items': []
                                }
                            orders_dict[item['order_id']]['items'].append(item)
                        
                        for order_id, order_data in orders_dict.items():
                            self.add_order_item(order_data['order_info'], order_data['items'])
            except Error as e:
                QMessageBox.critical(self, "错误", f"加载订单失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
        
        def add_order_item(self, order_info, items):
            order_frame = QFrame()
            order_frame.setFrameShape(QFrame.StyledPanel)
            order_frame.setStyleSheet("margin: 10px; padding: 10px;")
            
            layout = QVBoxLayout(order_frame)
            
            # 订单基本信息
            order_header = QLabel(f"订单号: {order_info['order_id']} | 状态: {order_info['status']} | 下单时间: {order_info['created_at']}")
            order_header.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(order_header)
            
            # 订单商品列表
            for item in items:
                item_layout = QHBoxLayout()
                
                # 商品图片
                if item['main_image']:
                    image_label = QLabel()
                    try:
                        pixmap = QPixmap(item['main_image'])
                        if not pixmap.isNull():
                            image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                            item_layout.addWidget(image_label)
                    except Exception as e:
                        print(f"图片加载错误：{str(e)}")
                
                # 商品信息
                info_layout = QVBoxLayout()
                name_label = QLabel(item['name'])
                info_layout.addWidget(name_label)
                
                price_label = QLabel(f"价格: ¥{item['price_at_order']} x {item['quantity']}")
                info_layout.addWidget(price_label)
                
                item_layout.addLayout(info_layout)
                layout.addLayout(item_layout)
            
            # 订单总价
            total_price = sum(item['price_at_order'] * item['quantity'] for item in items)
            total_label = QLabel(f"订单总价: ¥{total_price:.2f}")
            total_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(total_label)
            
            # 物流信息
            if order_info['tracking_number']:
                tracking_label = QLabel(f"物流单号: {order_info['tracking_number']}")
                layout.addWidget(tracking_label)
            
            self.orders_scroll_layout.addWidget(order_frame)
        
        def update_cart_item_quantity(self, cart_item_id, quantity):
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE cart_items 
                        SET quantity = %s 
                        WHERE cart_item_id = %s
                    """, (quantity, cart_item_id))
                    connection.commit()
            except Error as e:
                QMessageBox.critical(self, "错误", f"更新数量失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
        
        def remove_cart_item(self, cart_item_id):
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM cart_items WHERE cart_item_id = %s", (cart_item_id,))
                    connection.commit()
                    self.load_cart_items()  # 刷新购物车
            except Error as e:
                QMessageBox.critical(self, "错误", f"删除商品失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
        
        def handle_checkout(self):
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    # 获取用户ID
                    cursor.execute("SELECT customer_id FROM customers WHERE username = %s", (self.username,))
                    customer = cursor.fetchone()
                    
                    if customer:
                        # 获取购物车商品
                        cursor.execute("""
                            SELECT ci.sku_id, ci.quantity, s.price
                            FROM cart_items ci
                            JOIN carts c ON ci.cart_id = c.cart_id
                            JOIN skus s ON ci.sku_id = s.sku_id
                            WHERE c.customer_id = %s
                        """, (customer['customer_id'],))
                        cart_items = cursor.fetchall()
                        
                        if cart_items:
                            # 创建订单
                            cursor.execute("""
                                INSERT INTO orders (customer_id, status)
                                VALUES (%s, 'paid')
                            """, (customer['customer_id'],))
                            order_id = cursor.lastrowid
                            
                            # 添加订单商品
                            for item in cart_items:
                                cursor.execute("""
                                    INSERT INTO order_items (order_id, sku_id, quantity, price_at_order)
                                    VALUES (%s, %s, %s, %s)
                                """, (order_id, item['sku_id'], item['quantity'], item['price']))
                            
                            # 清空购物车
                            cursor.execute("""
                                DELETE ci FROM cart_items ci
                                JOIN carts c ON ci.cart_id = c.cart_id
                                WHERE c.customer_id = %s
                            """, (customer['customer_id'],))
                            
                            connection.commit()
                            QMessageBox.information(self, "成功", "订单创建成功！")
                            self.load_cart_items()  # 刷新购物车
                            self.load_orders()     # 刷新订单
                        else:
                            QMessageBox.warning(self, "警告", "购物车为空！")
            except Error as e:
                connection.rollback()
                QMessageBox.critical(self, "错误", f"结算失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()

        def update_sku_info(self):
            try:
                # 获取当前选择的规格
                selected_specs = {}
                for spec_type_id, combo in self.spec_combos.items():
                    if combo.currentIndex() >= 0:
                        selected_specs[spec_type_id] = combo.currentData()
                
                if len(selected_specs) < len(self.spec_combos):
                    self.sku_info_label.setText("请选择完整规格")
                    self.sku_info_label.setStyleSheet("font-size: 16px; color: #FF9800;")
                    return
                
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    # 查询匹配的SKU
                    cursor.execute("""
                        SELECT s.sku_id, s.price, s.stock
                        FROM skus s
                        JOIN sku_specs ss ON s.sku_id = ss.sku_id
                        JOIN spec_values sv ON ss.spec_value_id = sv.spec_value_id
                        WHERE s.product_id = %s AND sv.spec_value_id IN (%s)
                        GROUP BY s.sku_id
                        HAVING COUNT(DISTINCT sv.spec_type_id) = %s
                    """ % (self.current_product['product_id'], 
                          ','.join(map(str, selected_specs.values())), 
                          len(selected_specs)))
                    
                    sku = cursor.fetchone()
                    if sku:
                        stock_status = "有货" if sku['stock'] > 0 else "无货"
                        self.sku_info_label.setText(
                            f"当前选择: ¥{sku['price']} | 库存: {sku['stock']}件 | 状态: {stock_status}"
                        )
                        self.sku_info_label.setStyleSheet(
                            "font-size: 16px; color: #4CAF50;" if sku['stock'] > 0 
                            else "font-size: 16px; color: #F44336;"
                        )
                    else:
                        self.sku_info_label.setText("该规格组合无货")
                        self.sku_info_label.setStyleSheet("font-size: 16px; color: #F44336;")
            except Error as e:
                print(f"更新SKU信息失败: {str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
        def add_to_cart(self, product):
            try:
                # 获取用户选择的规格
                selected_specs = {}
                for spec_type_id, combo in self.spec_combos.items():
                    selected_specs[spec_type_id] = combo.currentData()
                
                # 查询匹配的SKU
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    # 查询匹配的SKU
                    cursor.execute("""
                        SELECT s.sku_id, s.price, s.stock
                        FROM skus s
                        JOIN sku_specs ss ON s.sku_id = ss.sku_id
                        JOIN spec_values sv ON ss.spec_value_id = sv.spec_value_id
                        WHERE s.product_id = %s AND sv.spec_value_id IN (%s)
                        GROUP BY s.sku_id
                        HAVING COUNT(DISTINCT sv.spec_value_id) = %s
                    """ % (product['product_id'], ','.join(map(str, selected_specs.values())), len(selected_specs)))
                    
                    sku = cursor.fetchone()
                    
                    if sku:
                        # 获取用户ID
                        cursor.execute("SELECT customer_id FROM customers WHERE username = %s", (self.username,))
                        customer = cursor.fetchone()
                        
                        if customer:
                            # 检查用户是否有购物车
                            cursor.execute("SELECT cart_id FROM carts WHERE customer_id = %s", (customer['customer_id'],))
                            cart = cursor.fetchone()
                            
                            if not cart:
                                # 创建购物车
                                cursor.execute("INSERT INTO carts (customer_id) VALUES (%s)", (customer['customer_id'],))
                                cart_id = cursor.lastrowid
                            else:
                                cart_id = cart['cart_id']
                            
                            # 检查购物车中是否已有该SKU
                            cursor.execute("""
                                SELECT cart_item_id, quantity 
                                FROM cart_items 
                                WHERE cart_id = %s AND sku_id = %s
                            """, (cart_id, sku['sku_id']))
                            existing_item = cursor.fetchone()
                            
                            if existing_item:
                                # 更新数量
                                new_quantity = existing_item['quantity'] + 1
                                cursor.execute("""
                                    UPDATE cart_items 
                                    SET quantity = %s 
                                    WHERE cart_item_id = %s
                                """, (new_quantity, existing_item['cart_item_id']))
                            else:
                                # 添加新商品
                                cursor.execute("""
                                    INSERT INTO cart_items (cart_id, sku_id, quantity)
                                    VALUES (%s, %s, 1)
                                """, (cart_id, sku['sku_id']))
                            
                            connection.commit()
                            QMessageBox.information(self, "添加成功", 
                                f"已添加 {product['name']} (SKU: {sku['sku_id']}) 到购物车")
                            self.load_cart_items()  # 刷新购物车
                    else:
                        QMessageBox.warning(self, "错误", "找不到匹配的SKU")
            except Error as e:
                QMessageBox.critical(self, "错误", f"添加到购物车失败: {str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
    
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        user_type = self.user_type_combo.currentText()

        if not username or not password:
            QMessageBox.warning(self, "警告", "用户名和密码不能为空！")
            return

        try:
            # 连接数据库
            connection = pymysql.connect(**self.db_config)
            cursor = connection.cursor()

            # 根据用户类型查询不同的表
            if user_type == "顾客":
                query = "SELECT * FROM customers WHERE username = %s AND password = %s"
            else:
                query = "SELECT * FROM staff WHERE username = %s AND password = %s"

            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                QMessageBox.information(self, "登录成功", f"欢迎，{username}!")
                if user_type == "顾客":
                    self.product_window = self.ProductWindow(username)
                    self.product_window.show()
                    self.close()  # 关闭登录窗口
            else:
                QMessageBox.warning(self, "登录失败", "用户名或密码错误！")
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"数据库连接错误：{str(e)}")
        finally:
            if 'connection' in locals() and connection.open:
                cursor.close()
                connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())


