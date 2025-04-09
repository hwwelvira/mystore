import sys
import os
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
            
            # 个人信息显示表单
            self.profile_form = QFormLayout()
            
            # 用户名显示和修改按钮
            self.username_label = QLabel()
            self.username_edit_btn = QPushButton("修改用户名")
            self.username_edit_btn.setStyleSheet("background-color: #2196F3; color: white;")
            self.username_edit_btn.clicked.connect(self.edit_username)
            
            username_layout = QHBoxLayout()
            username_layout.addWidget(self.username_label)
            username_layout.addWidget(self.username_edit_btn)
            self.profile_form.addRow("用户名:", username_layout)
            
            # 地址显示和修改按钮
            self.address_label = QLabel()
            self.address_label.setWordWrap(True)
            self.address_edit_btn = QPushButton("修改地址")
            self.address_edit_btn.setStyleSheet("background-color: #2196F3; color: white;")
            self.address_edit_btn.clicked.connect(self.edit_address)
            
            address_layout = QHBoxLayout()
            address_layout.addWidget(self.address_label)
            address_layout.addWidget(self.address_edit_btn)
            self.profile_form.addRow("收货地址:", address_layout)
            
            # 密码修改按钮
            self.password_edit_btn = QPushButton("修改密码")
            self.password_edit_btn.setStyleSheet("background-color: #2196F3; color: white;")
            self.password_edit_btn.clicked.connect(self.edit_password)
            self.profile_form.addRow("密码:", self.password_edit_btn)
            
            layout.addLayout(self.profile_form)
            layout.addStretch()
            
            self.load_profile_data()
        
        def load_profile_data(self):
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM customers WHERE username = %s", (self.username,))
                    customer = cursor.fetchone()
                    
                    if customer:
                        self.username_label.setText(customer['username'])
                        self.address_label.setText(customer.get('shipping_address', '未设置'))
            except Error as e:
                QMessageBox.critical(self, "错误", f"加载个人信息失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
        
        def edit_username(self):
            new_username, ok = QInputDialog.getText(
                self, "修改用户名", "请输入新用户名:", 
                QLineEdit.Normal, self.username_label.text()
            )
            
            if ok and new_username:
                if new_username == self.username_label.text():
                    return
                    
                try:
                    connection = pymysql.connect(**self.db_config)
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT customer_id FROM customers WHERE username = %s", (new_username,))
                        if cursor.fetchone():
                            QMessageBox.warning(self, "警告", "用户名已存在")
                            return
                            
                        cursor.execute(
                            "UPDATE customers SET username = %s WHERE username = %s",
                            (new_username, self.username)
                        )
                        connection.commit()
                        
                        self.username_label.setText(new_username)
                        self.username = new_username
                        QMessageBox.information(self, "成功", "用户名修改成功")
                except Error as e:
                    connection.rollback()
                    QMessageBox.critical(self, "错误", f"修改用户名失败：{str(e)}")
                finally:
                    if 'connection' in locals() and connection.open:
                        connection.close()
        
        def edit_address(self):
            new_address, ok = QInputDialog.getMultiLineText(
                self, "修改地址", "请输入新地址:", 
                self.address_label.text()
            )
            
            if ok:
                try:
                    connection = pymysql.connect(**self.db_config)
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE customers SET shipping_address = %s WHERE username = %s",
                            (new_address, self.username)
                        )
                        connection.commit()
                        
                        self.address_label.setText(new_address)
                        QMessageBox.information(self, "成功", "地址修改成功")
                except Error as e:
                    connection.rollback()
                    QMessageBox.critical(self, "错误", f"修改地址失败：{str(e)}")
                finally:
                    if 'connection' in locals() and connection.open:
                        connection.close()
        
        def edit_password(self):
            new_password, ok = QInputDialog.getText(
                self, "修改密码", "请输入新密码:", 
                QLineEdit.Password
            )
            
            if ok and new_password:
                confirm_password, ok = QInputDialog.getText(
                    self, "确认密码", "请再次输入新密码:", 
                    QLineEdit.Password
                )
                
                if ok and new_password == confirm_password:
                    try:
                        connection = pymysql.connect(**self.db_config)
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "UPDATE customers SET password = %s WHERE username = %s",
                                (new_password, self.username)
                            )
                            connection.commit()
                            QMessageBox.information(self, "成功", "密码修改成功")
                    except Error as e:
                        connection.rollback()
                        QMessageBox.critical(self, "错误", f"修改密码失败：{str(e)}")
                    finally:
                        if 'connection' in locals() and connection.open:
                            connection.close()
                elif ok:
                    QMessageBox.warning(self, "警告", "两次输入的密码不一致")
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
                        if customer:
                        # 查询订单及商品信息
                            cursor.execute("""
                            SELECT o.order_id, o.status, o.created_at, 
                                   o.shipped_at, o.delivered_at, o.tracking_number,
                                   o.shipping_address,
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
            status_map = {
                'paid': '已下单',
                'shipped': '正在派送',
                'delivered': '已收货'
            }
            status_text = status_map.get(order_info['status'], order_info['status'])
            
            order_header = QLabel(f"订单号: {order_info['order_id']} | 状态: {status_text} | 下单时间: {order_info['created_at']}")
            order_header.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(order_header)
            
            # 添加收货地址
            if order_info.get('shipping_address'):
                address_label = QLabel(f"收货地址: {order_info['shipping_address']}")
                address_label.setWordWrap(True)
                layout.addWidget(address_label)
            
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
    class StaffWindow(QMainWindow):
        def __init__(self, username, is_manager):
            super().__init__()
            self.username = username
            self.is_manager = is_manager  # True表示店长，False表示普通店员
            self.setWindowTitle(f"店员管理面板 - 欢迎 {username}")
            self.setFixedSize(1200, 800)
            
            self.db_config = {
                'host': 'rm-2ze0mr80dxyl91832oo.mysql.rds.aliyuncs.com',
                'port': 3306,
                'user': 'hww',
                'password': 'Huangwaiwai666',
                'database': 'mystore',
                'cursorclass': pymysql.cursors.DictCursor
            }
            
            self.init_ui()
        
        def init_ui(self):
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
            
            # 创建选项卡页面
            self.add_product_tab = QWidget()
            self.remove_product_tab = QWidget()
            self.ship_orders_tab = QWidget()
            
            # 添加基本选项卡
            self.tab_bar.addTab(self.add_product_tab, "上架新商品")
            self.tab_bar.addTab(self.remove_product_tab, "修改商品库存")
            self.tab_bar.addTab(self.ship_orders_tab, "订单发货")
            
            # 店长专属选项卡
            if self.is_manager:
                self.manage_staff_tab = QWidget()
                self.tab_bar.addTab(self.manage_staff_tab, "管理店员")
                self.init_manage_staff_tab()
            
            # 初始化各选项卡
            self.init_add_product_tab()
            self.init_remove_product_tab()
            self.init_ship_orders_tab()
            
            self.main_layout.addWidget(self.tab_bar, stretch=1)
        
        def init_add_product_tab(self):
            # 创建主滚动区域
            self.add_product_scroll = QScrollArea()
            self.add_product_scroll.setWidgetResizable(True)
            self.add_product_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.add_product_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
            # 创建滚动内容容器
            self.add_product_scroll_content = QWidget()
            self.add_product_scroll.setWidget(self.add_product_scroll_content)
            
            # 主布局放在滚动区域内
            layout = QVBoxLayout(self.add_product_scroll_content)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(15)
            
            # 商品基本信息表单
            form_layout = QFormLayout()
            form_layout.setSpacing(10)
            
            # 商品名称
            self.product_name_input = QLineEdit()
            form_layout.addRow("商品名称:", self.product_name_input)
            
            # 商品描述
            self.product_desc_input = QTextEdit()
            form_layout.addRow("商品描述:", self.product_desc_input)
            
            # 商品图片
            self.product_image_input = QLineEdit()
            self.browse_image_btn = QPushButton("浏览...")
            self.browse_image_btn.clicked.connect(self.browse_image)
            image_layout = QHBoxLayout()
            image_layout.addWidget(self.product_image_input)
            image_layout.addWidget(self.browse_image_btn)
            form_layout.addRow("商品图片:", image_layout)
            
            layout.addLayout(form_layout)
            
            # 规格管理区域
            self.spec_group = QGroupBox("规格管理")
            self.spec_group.setStyleSheet("QGroupBox { padding: 10px; }")
            self.spec_layout = QVBoxLayout()
            
            # 规格值表格
            self.spec_table = QTableWidget()
            self.spec_table.setColumnCount(2)
            self.spec_table.setHorizontalHeaderLabels(["规格类型", "规格值"])
            self.spec_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.spec_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.spec_layout.addWidget(self.spec_table)
            
            # 添加规格按钮
            self.add_spec_btn = QPushButton("添加商品规格类型")
            self.add_spec_btn.clicked.connect(self.show_add_spec_dialog)
            self.spec_layout.addWidget(self.add_spec_btn)
            
            self.spec_group.setLayout(self.spec_layout)
            layout.addWidget(self.spec_group)
            
            # SKU管理区域
            self.sku_group = QGroupBox("SKU管理")
            self.sku_group.setStyleSheet("QGroupBox { padding: 10px; }")
            self.sku_layout = QVBoxLayout()
            
            # SKU表格
            self.sku_table = QTableWidget()
            self.sku_table.setColumnCount(3)
            self.sku_table.setHorizontalHeaderLabels(["规格组合", "价格", "库存"])
            self.sku_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.sku_table.setColumnWidth(1, 100)
            self.sku_table.setColumnWidth(2, 100)
            self.sku_table.setFixedHeight(250)
            self.sku_layout.addWidget(self.sku_table)
            
            # 添加SKU按钮
            self.add_sku_btn = QPushButton("添加SKU")
            self.add_sku_btn.clicked.connect(self.add_sku)
            self.sku_layout.addWidget(self.add_sku_btn)
            
            self.sku_group.setLayout(self.sku_layout)
            layout.addWidget(self.sku_group)
            
            # 上架按钮
            self.add_product_btn = QPushButton("上架商品")
            self.add_product_btn.clicked.connect(self.add_product)
            layout.addWidget(self.add_product_btn)
            
            # 加载规格类型
            #self.load_spec_types()
            
            # 设置选项卡布局
            self.add_product_tab.setLayout(QVBoxLayout())
            self.add_product_tab.layout().addWidget(self.add_product_scroll)
            self.add_product_tab.layout().setContentsMargins(0, 0, 0, 0)
        
        def browse_image(self):
            file_path, _ = QFileDialog.getOpenFileName(self, "选择商品图片", "", "图片文件 (*.png *.jpg *.jpeg)")
            if file_path:
                # 转换为相对路径
                rel_path = file_path.replace(os.getcwd(), "").lstrip("\\/")
                self.product_image_input.setText(rel_path)
        def show_add_spec_dialog(self):
            # 第一步：选择规格类型
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM spec_types")
                    spec_types = cursor.fetchall()
                    
                    if not spec_types:
                        QMessageBox.warning(self, "提示", "没有可用的规格类型")
                        return
                        
                    # 创建选择规格类型的对话框
                    dialog = QDialog(self)
                    dialog.setWindowTitle("选择规格类型")
                    layout = QVBoxLayout(dialog)
                    
                    # 规格类型列表
                    spec_list = QListWidget()
                    for spec in spec_types:
                        item = QListWidgetItem(spec['name'])
                        item.setData(Qt.UserRole, spec['spec_type_id'])
                        spec_list.addItem(item)
                    
                    layout.addWidget(spec_list)
                    
                    # 确定按钮
                    btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                    btn_box.accepted.connect(dialog.accept)
                    btn_box.rejected.connect(dialog.reject)
                    layout.addWidget(btn_box)
                    
                    if dialog.exec_() == QDialog.Accepted:
                        selected_item = spec_list.currentItem()
                        if selected_item:
                            spec_type_id = selected_item.data(Qt.UserRole)
                            spec_type_name = selected_item.text()
                            self.show_select_spec_value_dialog(spec_type_id, spec_type_name)
            except Error as e:
                QMessageBox.critical(self, "错误", f"加载规格类型失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()

        def show_select_spec_value_dialog(self, spec_type_id, spec_type_name):
            # 第二步：选择或添加规格值
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    # 获取该规格类型的所有规格值
                    cursor.execute("""
                        SELECT * FROM spec_values 
                        WHERE spec_type_id = %s
                    """, (spec_type_id,))
                    spec_values = cursor.fetchall()
                    
                    dialog = QDialog(self)
                    dialog.setWindowTitle(f"选择{spec_type_name}规格值")
                    layout = QVBoxLayout(dialog)
                    
                    # 现有规格值列表
                    value_list = QListWidget()
                    for value in spec_values:
                        item = QListWidgetItem(value['value'])
                        item.setData(Qt.UserRole, value['spec_value_id'])
                        value_list.addItem(item)
                    
                    layout.addWidget(QLabel(f"现有{spec_type_name}规格值:"))
                    layout.addWidget(value_list)
                    
                    # 添加新规格值区域
                    layout.addWidget(QLabel("或添加新规格值:"))
                    new_value_input = QLineEdit()
                    layout.addWidget(new_value_input)
                    
                    btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                    btn_box.accepted.connect(dialog.accept)
                    btn_box.rejected.connect(dialog.reject)
                    layout.addWidget(btn_box)
                    
                    if dialog.exec_() == QDialog.Accepted:
                        selected_value = None
                        if value_list.currentItem():
                            selected_value = value_list.currentItem().text()
                        elif new_value_input.text().strip():
                            new_value = new_value_input.text().strip()
                            cursor.execute("""
                                INSERT INTO spec_values (spec_type_id, value)
                                VALUES (%s, %s)
                            """, (spec_type_id, new_value))
                            connection.commit()
                            selected_value = new_value
                        
                        if selected_value:
                            # 添加到主界面表格
                            row = self.spec_table.rowCount()
                            self.spec_table.insertRow(row)
                            self.spec_table.setItem(row, 0, QTableWidgetItem(spec_type_name))
                            self.spec_table.setItem(row, 1, QTableWidgetItem(selected_value))
                            
                            # 不再自动生成SKU，改为提示用户手动生成
                            QMessageBox.information(
                                self, '提示', 
                                '规格值已添加，请手动点击"添加SKU"按钮生成SKU记录'
                            )
            except Error as e:
                QMessageBox.critical(self, "错误", f"操作规格值失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
        def add_sku_from_specs(self):
            """从规格表中生成SKU记录"""
            if self.spec_table.rowCount() == 0:
                QMessageBox.warning(self, "警告", "请先添加规格值")
                return
                
            # 收集所有规格值
            specs = []
            for row in range(self.spec_table.rowCount()):
                spec_type = self.spec_table.item(row, 0).text()
                spec_value = self.spec_table.item(row, 1).text()
                specs.append(f"{spec_type}:{spec_value}")
            
            # 检查是否已存在相同规格组合
            for row in range(self.sku_table.rowCount()):
                if self.sku_table.item(row, 0).text() == " | ".join(specs):
                    QMessageBox.warning(self, "警告", "该规格组合已存在")
                    return
                    
            # 添加新SKU记录
            row = self.sku_table.rowCount()
            self.sku_table.insertRow(row)
            self.sku_table.setItem(row, 0, QTableWidgetItem(" | ".join(specs)))
            self.sku_table.setItem(row, 1, QTableWidgetItem("点击设置价格"))
            self.sku_table.setItem(row, 2, QTableWidgetItem("点击设置库存"))
            
            # 清空规格表以便添加新规格
            self.spec_table.setRowCount(0)
            QMessageBox.information(self, "成功", "SKU记录已生成")

        def add_sku(self):
            """为当前规格组合创建SKU记录"""
            # 检查规格表中是否有规格值
            if self.spec_table.rowCount() > 0:
                # 如果有规格值，先调用add_sku_from_specs生成SKU记录
                self.add_sku_from_specs()
                return
                
            # 检查SKU表中是否有待设置的SKU记录
            if self.sku_table.rowCount() == 0:
                QMessageBox.warning(self, "警告", "请先添加规格组合")
                return
                
            # 获取最后添加的SKU记录(最新添加的)
            last_row = self.sku_table.rowCount() - 1
            sku_item = self.sku_table.item(last_row, 0)
            
            if not sku_item or "点击" not in self.sku_table.item(last_row, 1).text():
                QMessageBox.warning(self, "警告", "请先添加规格组合")
                return
                
            # 设置价格
            price, ok1 = QInputDialog.getDouble(
                self, "设置价格", "请输入价格:", 
                0, 0, 10000, 2
            )
            if ok1:
                self.sku_table.setItem(last_row, 1, QTableWidgetItem(f"¥{price:.2f}"))
                
            # 设置库存
            stock, ok2 = QInputDialog.getInt(
                self, "设置库存", "请输入库存:", 
                0, 0, 10000
            )
            if ok2:
                self.sku_table.setItem(last_row, 2, QTableWidgetItem(f"{stock}件"))
        def add_product(self):
            # 验证基本信息
            name = self.product_name_input.text().strip()
            desc = self.product_desc_input.toPlainText().strip()
            image = self.product_image_input.text().strip()
            
            if not name:
                QMessageBox.warning(self, "警告", "请输入商品名称")
                return
                
            if self.sku_table.rowCount() == 0:
                QMessageBox.warning(self, "警告", "请至少添加一个SKU")
                return
                
            # 验证所有SKU是否已设置价格和库存
            for row in range(self.sku_table.rowCount()):
                price_item = self.sku_table.item(row, 1)
                stock_item = self.sku_table.item(row, 2)
                if not price_item or not stock_item or "点击" in price_item.text() or "点击" in stock_item.text():
                    QMessageBox.warning(self, "警告", f"第{row+1}行SKU的价格或库存未设置")
                    return
                    
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    # 添加商品基本信息
                    cursor.execute(
                        "INSERT INTO products (name, description, main_image) VALUES (%s, %s, %s)",
                        (name, desc, image)
                    )
                    product_id = cursor.lastrowid
                    
                    # 添加所有SKU信息
                    for row in range(self.sku_table.rowCount()):
                        price = float(self.sku_table.item(row, 1).text().replace("¥", ""))
                        stock = int(self.sku_table.item(row, 2).text().replace("件", ""))
                        
                        # 添加SKU
                        cursor.execute(
                            "INSERT INTO skus (product_id, price, stock) VALUES (%s, %s, %s)",
                            (product_id, price, stock)
                        )
                        sku_id = cursor.lastrowid
                        
                        # 解析规格组合并添加到sku_specs表
                        specs = self.sku_table.item(row, 0).text().split(" | ")
                        for spec in specs:
                            spec_type, spec_value = spec.split(":")
                            cursor.execute("""
                                SELECT sv.spec_value_id 
                                FROM spec_values sv
                                JOIN spec_types st ON sv.spec_type_id = st.spec_type_id
                                WHERE st.name = %s AND sv.value = %s
                            """, (spec_type, spec_value))
                            spec_value_id = cursor.fetchone()['spec_value_id']
                            
                            cursor.execute(
                                "INSERT INTO sku_specs (sku_id, spec_value_id) VALUES (%s, %s)",
                                (sku_id, spec_value_id)
                            )
                    
                    connection.commit()
                    QMessageBox.information(self, "成功", "商品上架成功")
                    
                    # 清空表单
                    self.product_name_input.clear()
                    self.product_desc_input.clear()
                    self.product_image_input.clear()
                    self.sku_table.setRowCount(0)
                    self.spec_table.setRowCount(0)
                    
            except Error as e:
                connection.rollback()
                QMessageBox.critical(self, "错误", f"上架商品失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()
        
        def init_remove_product_tab(self):
            layout = QVBoxLayout(self.remove_product_tab)
            
            # 搜索框
            search_layout = QHBoxLayout()
            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("输入商品名称搜索...")
            search_btn = QPushButton("搜索")
            search_btn.clicked.connect(self.search_products)
            search_layout.addWidget(self.search_input)
            search_layout.addWidget(search_btn)
            layout.addLayout(search_layout)
            
            # 商品列表
            self.product_list = QListWidget()
            self.product_list.itemClicked.connect(self.load_product_skus)
            layout.addWidget(self.product_list)
            
            # SKU表格
            self.sku_table = QTableWidget()
            self.sku_table.setColumnCount(4)
            self.sku_table.setHorizontalHeaderLabels(["规格组合", "价格", "库存", "操作"])
            self.sku_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            layout.addWidget(self.sku_table)
            
            # 下架按钮
            self.delete_product_btn = QPushButton("下架该商品")
            self.delete_product_btn.clicked.connect(self.delete_product)
            layout.addWidget(self.delete_product_btn)
            
            self.current_product_id = None

        def search_products(self):
            keyword = self.search_input.text().strip()
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    query = "SELECT * FROM products WHERE name LIKE %s AND is_delete = 0"
                    cursor.execute(query, (f"%{keyword}%",))
                    products = cursor.fetchall()
                    
                    self.product_list.clear()
                    for product in products:
                        item = QListWidgetItem(product['name'])
                        item.setData(Qt.UserRole, product['product_id'])
                        self.product_list.addItem(item)
            except Error as e:
                QMessageBox.critical(self, "错误", f"搜索商品失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()

        def load_product_skus(self, item):
            self.current_product_id = item.data(Qt.UserRole)
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    # 查询商品的所有SKU
                    cursor.execute("""
                        SELECT s.sku_id, s.price, s.stock, 
                               GROUP_CONCAT(sv.value ORDER BY st.spec_type_id SEPARATOR ', ') as specs
                        FROM skus s
                        LEFT JOIN sku_specs ss ON s.sku_id = ss.sku_id
                        LEFT JOIN spec_values sv ON ss.spec_value_id = sv.spec_value_id
                        LEFT JOIN spec_types st ON sv.spec_type_id = st.spec_type_id
                        WHERE s.product_id = %s
                        GROUP BY s.sku_id
                    """, (self.current_product_id,))
                    skus = cursor.fetchall()
                    
                    self.sku_table.setRowCount(0)
                    for row, sku in enumerate(skus):
                        self.sku_table.insertRow(row)
                        
                        # 规格组合
                        self.sku_table.setItem(row, 0, QTableWidgetItem(sku['specs']))
                        
                        # 价格(可编辑)
                        price_item = QTableWidgetItem(str(sku['price']))
                        price_item.setFlags(price_item.flags() | Qt.ItemIsEditable)
                        self.sku_table.setItem(row, 1, price_item)
                        
                        # 库存(可编辑)
                        stock_item = QTableWidgetItem(str(sku['stock']))
                        stock_item.setFlags(stock_item.flags() | Qt.ItemIsEditable)
                        self.sku_table.setItem(row, 2, stock_item)
                        
                        # 保存按钮
                        save_btn = QPushButton("保存")
                        save_btn.clicked.connect(lambda _, r=row: self.save_sku_changes(r))
                        self.sku_table.setCellWidget(row, 3, save_btn)
                        
                        # 保存SKU ID
                        self.sku_table.item(row, 0).setData(Qt.UserRole, sku['sku_id'])
            except Error as e:
                QMessageBox.critical(self, "错误", f"加载SKU失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()

        def save_sku_changes(self, row):
            try:
                sku_id = self.sku_table.item(row, 0).data(Qt.UserRole)
                new_price = float(self.sku_table.item(row, 1).text())
                new_stock = int(self.sku_table.item(row, 2).text())
                
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE skus 
                        SET price = %s, stock = %s 
                        WHERE sku_id = %s
                    """, (new_price, new_stock, sku_id))
                    connection.commit()
                    QMessageBox.information(self, "成功", "修改已保存")
            except ValueError:
                QMessageBox.warning(self, "警告", "请输入有效的数字")
            except Error as e:
                QMessageBox.critical(self, "错误", f"保存失败：{str(e)}")
            finally:
                if 'connection' in locals() and connection.open:
                    connection.close()

        def delete_product(self):
            if not self.current_product_id:
                QMessageBox.warning(self, "警告", "请先选择商品")
                return
                
            reply = QMessageBox.question(
                self, '确认', 
                '确定要下架该商品吗？下架后商品将不再显示',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    connection = pymysql.connect(**self.db_config)
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            UPDATE products 
                            SET is_delete = 1 
                            WHERE product_id = %s
                        """, (self.current_product_id,))
                        connection.commit()
                        
                        # 清空当前选择
                        self.current_product_id = None
                        self.product_list.clear()
                        self.sku_table.setRowCount(0)
                        
                        QMessageBox.information(self, "成功", "商品已下架")
                except Error as e:
                    QMessageBox.critical(self, "错误", f"下架失败：{str(e)}")
                finally:
                    if 'connection' in locals() and connection.open:
                        connection.close()
        
        def init_ship_orders_tab(self):
            layout = QVBoxLayout(self.ship_orders_tab)
            
            # 订单列表
            self.order_list = QTableWidget()
            self.order_list.setColumnCount(5)
            self.order_list.setHorizontalHeaderLabels(["订单号", "下单时间", "状态", "操作", "物流单号"])
            layout.addWidget(self.order_list)
            
            self.load_orders()
        
        def load_orders(self):
            # 加载待发货订单
            pass
        
        def init_manage_staff_tab(self):
            layout = QVBoxLayout(self.manage_staff_tab)
            
            # 店员列表
            self.staff_list = QTableWidget()
            self.staff_list.setColumnCount(4)
            self.staff_list.setHorizontalHeaderLabels(["用户名", "职位", "操作", "删除"])
            layout.addWidget(self.staff_list)
            
            # 添加店员表单
            form_layout = QFormLayout()
            
            self.new_staff_username = QLineEdit()
            self.new_staff_password = QLineEdit()
            self.new_staff_password.setEchoMode(QLineEdit.Password)
            self.new_staff_position = QComboBox()
            self.new_staff_position.addItems(["店员", "店长"])
            
            form_layout.addRow("用户名:", self.new_staff_username)
            form_layout.addRow("密码:", self.new_staff_password)
            form_layout.addRow("职位:", self.new_staff_position)
            
            self.add_staff_btn = QPushButton("添加店员")
            self.add_staff_btn.clicked.connect(self.add_staff)
            form_layout.addRow(self.add_staff_btn)
            
            layout.addLayout(form_layout)
            
            self.load_staff_list()
        
        def load_staff_list(self):
            # 加载店员列表
            pass
        
        def add_staff(self):
            # 实现添加店员逻辑
            pass

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        user_type = self.user_type_combo.currentText()

        if not username or not password:
            QMessageBox.warning(self, "警告", "用户名和密码不能为空！")
            return

        try:
            connection = pymysql.connect(**self.db_config)
            with connection.cursor() as cursor:
                if user_type == "顾客":
                    query = "SELECT * FROM customers WHERE username = %s AND password = %s"
                    params = (username, password)
                else:
                    query = "SELECT * FROM staff WHERE name = %s AND password = %s"
                    params = (username, password)

                cursor.execute(query, params)
                result = cursor.fetchone()

                if result:
                    QMessageBox.information(self, "登录成功", f"欢迎，{username}!")
                    if user_type == "顾客":
                        self.product_window = self.ProductWindow(username)
                        self.product_window.show()  # 添加这行
                    else:
                        is_manager = bool(result['role'])
                        self.staff_window = self.StaffWindow(username, is_manager)
                        self.staff_window.show()  # 添加这行
                    self.close()
                else:
                    QMessageBox.warning(self, "登录失败", "用户名或密码错误！")
        except Error as e:
            QMessageBox.critical(self, "错误", f"登录失败：{str(e)}")
        finally:
            if 'connection' in locals() and connection.open:
                connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())


