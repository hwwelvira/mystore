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
            
            self.init_ui()
            self.load_products()
        
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
            self.load_products()
        
        def init_cart_tab(self):
            # 购物车页（待实现）
            layout = QVBoxLayout(self.cart_tab)
            label = QLabel("购物车功能待实现")
            label.setStyleSheet("font-size: 24px;")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
        
        def init_orders_tab(self):
            # 订单页（待实现）
            layout = QVBoxLayout(self.orders_tab)
            label = QLabel("订单功能待实现")
            label.setStyleSheet("font-size: 24px;")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
        
        def init_profile_tab(self):
            # 个人信息页（待实现）
            layout = QVBoxLayout(self.profile_tab)
            label = QLabel("个人信息功能待实现")
            label.setStyleSheet("font-size: 24px;")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
        
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
            
            # 商品图片（修改为加载本地路径图片）
            if product['main_image']:
                image_label = QLabel()
                try:
                    # 假设图片存储在 static/images 目录下
                    image_path = f"{product['main_image']}"
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
                        layout.addWidget(image_label)
                    else:
                        print(f"无法加载图片：{image_path}")
                except Exception as e:
                    print(f"图片加载错误：{str(e)}")
            
            # 商品信息
            info_layout = QVBoxLayout()
            
            name_label = QLabel(product['name'])
            name_label.setStyleSheet("font-size: 34px; font-weight: bold;")
            info_layout.addWidget(name_label)
            
            # 添加商品描述
            desc_label = QLabel(product['description'])
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("font-size: 18px; color: #555;")
            info_layout.addWidget(desc_label)
            
            layout.addLayout(info_layout)
            layout.addStretch()
            
            # 查看详情按钮
            detail_btn = QPushButton("查看商品详细信息")
            detail_btn.setStyleSheet("background-color: #2196F3; color: white;")
            detail_btn.clicked.connect(lambda: self.show_product_details(product))
            
            # 将按钮添加到布局
            button_layout = QVBoxLayout()
            button_layout.addWidget(detail_btn)
            button_layout.addStretch()
            layout.addLayout(button_layout)
            
            self.scroll_layout.addWidget(item_frame)
        def show_product_details(self, product):
            try:
                connection = pymysql.connect(**self.db_config)
                with connection.cursor() as cursor:
                    # 查询商品规格类型
                    cursor.execute("""
                        SELECT st.spec_type_id, st.name, 
                               GROUP_CONCAT(sv.spec_value_id, ':', sv.value SEPARATOR '|') AS spec_values
                        FROM spec_types st
                        JOIN spec_values sv ON st.spec_type_id = sv.spec_type_id
                        JOIN sku_specs ss ON sv.spec_value_id = ss.spec_value_id
                        JOIN skus s ON ss.sku_id = s.sku_id
                        WHERE s.product_id = %s
                        GROUP BY st.spec_type_id
                    """, (product['product_id'],))
                    spec_types = cursor.fetchall()
                    
                    # 创建详情窗口
                    detail_window = QDialog(self)
                    detail_window.setWindowTitle(f"{product['name']} - 商品详情")
                    detail_window.setFixedSize(500, 400)
                    
                    layout = QVBoxLayout()
                    
                    # 显示商品基本信息
                    name_label = QLabel(f"商品名称: {product['name']}")
                    name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
                    layout.addWidget(name_label)
                    
                    desc_label = QLabel(f"商品描述: {product['description']}")
                    desc_label.setWordWrap(True)
                    layout.addWidget(desc_label)
                    
                    # 添加规格选择区域
                    self.spec_combos = {}
                    for spec in spec_types:
                        spec_label = QLabel(f"{spec['name']}:")
                        spec_combo = QComboBox()
                        
                        # 添加规格选项
                        for value_pair in spec['spec_values'].split('|'):
                            value_id, value = value_pair.split(':')
                            spec_combo.addItem(value, value_id)
                        
                        spec_layout = QHBoxLayout()
                        spec_layout.addWidget(spec_label)
                        spec_layout.addWidget(spec_combo)
                        layout.addLayout(spec_layout)
                        
                        self.spec_combos[spec['spec_type_id']] = spec_combo
                    
                    # 添加确定按钮
                    confirm_btn = QPushButton("确定选择")
                    confirm_btn.clicked.connect(lambda: self.add_to_cart(product))
                    layout.addWidget(confirm_btn)
                    
                    detail_window.setLayout(layout)
                    detail_window.exec_()
                    
            except Error as e:
                QMessageBox.critical(self, "错误", f"加载商品详情失败: {str(e)}")
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
                    # 这里需要根据选择的规格值查询对应的SKU
                    # 实际实现可能需要更复杂的SQL查询
                    cursor.execute("""
                        SELECT s.sku_id, s.price, s.stock
                        FROM skus s
                        JOIN sku_specs ss ON s.sku_id = ss.sku_id
                        WHERE s.product_id = %s AND ss.spec_value_id IN (%s)
                        GROUP BY s.sku_id
                        HAVING COUNT(DISTINCT ss.spec_value_id) = %s
                    """, (product['product_id'], ','.join(map(str, selected_specs.values())), len(selected_specs)))
                    
                    sku = cursor.fetchone()
                    
                    if sku:
                        QMessageBox.information(self, "添加成功", 
                            f"已添加 {product['name']} (SKU: {sku['sku_id']}) 到购物车")
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


