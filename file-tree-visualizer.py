import os
import sys
import datetime
import pyperclip
from PySide6.QtWidgets import (QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QTextEdit,
                               QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QStatusBar, QFileDialog,
                               QMenu, QToolBar, QLabel, QSplitter, QFrame, QSizePolicy, QHeaderView)
from PySide6.QtCore import Qt, QMimeData, QUrl, QSize, QTimer, QTimer
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QAction, QColor, QFont, QPalette, QPixmap, QPainter
import platform


class FileExplorerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件树管理器 - 目录结构可视化工具 | 资速达 www.zisuda.com")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 650)

        # 状态变量
        self.current_path = None
        self.theme_mode = "dark"  # 默认使用暗色模式

        # 定义初始颜色变量
        self.tool_button_text_color = "#CDD6F4"  # 默认深色模式文字颜色

        # 设置应用字体 - 提高清晰度和可读性
        self.setup_fonts()

        # 设置 UI 和主题
        self.setup_theme()
        self.setup_ui()

        # 启用拖放功能
        self.setAcceptDrops(True)

    def setup_fonts(self):
        """设置应用字体，优化显示效果"""
        app_font = QFont()

        # 根据操作系统选择最佳字体
        if platform.system() == "Windows":
            app_font.setFamily("Microsoft YaHei UI")
        elif platform.system() == "Darwin":  # macOS
            app_font.setFamily("PingFang SC")
        else:  # Linux 和其他
            app_font.setFamily("Noto Sans CJK SC")

        app_font.setPointSize(10)
        app_font.setHintingPreference(QFont.PreferFullHinting)  # 提高字体清晰度
        QApplication.setFont(app_font)

        # 针对树视图设置稍大的字体
        self.tree_font = QFont(app_font)
        self.tree_font.setPointSize(11)

    def setup_theme(self):
        """设置暗色或亮色主题，使用现代化配色。"""
        if self.theme_mode == "dark":
            self.setStyleSheet("""
                QMainWindow, QDialog, QFileDialog {
                    background-color: #1E1E2E;
                    color: #CDD6F4;
                }
                QSplitter::handle {
                    background-color: #313244;
                    width: 1px;
                }
                QTreeWidget, QTextEdit {
                    background-color: #1E1E2E;
                    color: #CDD6F4;
                    border: 1px solid #313244;
                    border-radius: 8px;
                    padding: 5px;
                    selection-background-color: #45475A;
                    selection-color: #FFFFFF;
                }
                QTreeWidget::item:hover {
                    background-color: #313244;
                    border-radius: 4px;
                }
                QTreeWidget::item:selected {
                    background-color: #45475A;
                    border-radius: 4px;
                }
                QHeaderView::section {
                    background-color: #181825;
                    color: #CDD6F4;
                    padding: 5px;
                    border: none;
                    border-radius: 0px;
                    border-bottom: 2px solid #313244;
                }
                QPushButton {
                    background-color: #45475A;
                    color: #CDD6F4;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #585B70;
                }
                QPushButton:pressed {
                    background-color: #313244;
                }
                QPushButton:disabled {
                    background-color: #313244;
                    color: #6C7086;
                }
                QStatusBar {
                    background-color: #181825;
                    color: #CDD6F4;
                    border-top: 1px solid #313244;
                    padding: 3px;
                }
                QToolBar {
                    background-color: #181825;
                    border: none;
                    border-bottom: 1px solid #313244;
                    padding: 5px;
                    spacing: 5px;
                }
                QToolButton {
                    background-color: transparent;
                    color: #CDD6F4;
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                }
                QToolButton:hover {
                    background-color: #313244;
                }
                QToolButton:pressed {
                    background-color: #45475A;
                }
                QMenu {
                    background-color: #1E1E2E;
                    color: #CDD6F4;
                    border: 1px solid #313244;
                    border-radius: 6px;
                    padding: 5px;
                }
                QMenu::item {
                    padding: 8px 25px 8px 20px;
                    border-radius: 4px;
                }
                QMenu::item:selected {
                    background-color: #45475A;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #313244;
                    margin: 5px 15px;
                }
                QScrollBar:vertical {
                    background-color: #1E1E2E;
                    width: 12px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background-color: #45475A;
                    min-height: 30px;
                    border-radius: 5px;
                    margin: 3px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #585B70;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    background: none;
                    height: 0px;
                }
                QScrollBar:horizontal {
                    background-color: #1E1E2E;
                    height: 12px;
                    margin: 0px;
                }
                QScrollBar::handle:horizontal {
                    background-color: #45475A;
                    min-width: 30px;
                    border-radius: 5px;
                    margin: 3px;
                }
                QScrollBar::handle:horizontal:hover {
                    background-color: #585B70;
                }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    background: none;
                    width: 0px;
                }
            """)
            self.folder_icon_color = "#FAB387"  # 文件夹使用橙色
            self.file_icon_color = "#A6E3A1"  # 文件使用绿色
            self.copy_icon_color = "#89B4FA"  # 复制按钮使用蓝色
            self.error_color = "#F38BA8"  # 错误使用红色
            self.header_text_color = "#CDD6F4"  # 深色模式下的标题文字颜色
            self.tool_button_text_color = "#CDD6F4"  # 深色模式下工具按钮文字颜色
            self.dark_mode = True
        else:
            self.setStyleSheet("""
                QMainWindow, QDialog, QFileDialog {
                    background-color: #EFF1F5;
                    color: #4C4F69;
                }
                QSplitter::handle {
                    background-color: #9CA0B0;
                    width: 1px;
                }
                QTreeWidget, QTextEdit {
                    background-color: #FFFFFF;
                    color: #4C4F69;
                    border: 1px solid #DCE0E8;
                    border-radius: 8px;
                    padding: 5px;
                    selection-background-color: #CCCFD9;
                    selection-color: #4C4F69;
                }
                QTreeWidget::item:hover {
                    background-color: #EFF1F5;
                    border-radius: 4px;
                }
                QTreeWidget::item:selected {
                    background-color: #CCCFD9;
                    border-radius: 4px;
                }
                QHeaderView::section {
                    background-color: #8CAAEE;
                    color: #FFFFFF;
                    padding: 5px;
                    border: none;
                    border-radius: 0px;
                    border-bottom: 2px solid #7993DF;
                    font-weight: bold;
                }
                QPushButton {
                    background-color: #8CAAEE;
                    color: #FFFFFF;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #7993DF;
                }
                QPushButton:pressed {
                    background-color: #6980C5;
                }
                QPushButton:disabled {
                    background-color: #DCE0E8;
                    color: #9CA0B0;
                }
                QStatusBar {
                    background-color: #DCE0E8;
                    color: #4C4F69;
                    border-top: 1px solid #9CA0B0;
                    padding: 3px;
                }
                QToolBar {
                    background-color: #DCE0E8;
                    border: none;
                    border-bottom: 1px solid #9CA0B0;
                    padding: 5px;
                    spacing: 5px;
                }
                QToolButton {
                    background-color: #8CAAEE;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                }
                QToolButton:hover {
                    background-color: #7993DF;
                }
                QToolButton:pressed {
                    background-color: #6980C5;
                }
                QLabel[labelType="header"] {
                    color: #4C4F69;
                    font-weight: bold;
                    font-size: 13px;
                    margin-bottom: 5px;
                }
                QMenu {
                    background-color: #FFFFFF;
                    color: #4C4F69;
                    border: 1px solid #DCE0E8;
                    border-radius: 6px;
                    padding: 5px;
                }
                QMenu::item {
                    padding: 8px 25px 8px 20px;
                    border-radius: 4px;
                }
                QMenu::item:selected {
                    background-color: #CCCFD9;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #DCE0E8;
                    margin: 5px 15px;
                }
                QScrollBar:vertical {
                    background-color: #EFF1F5;
                    width: 12px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background-color: #CCCFD9;
                    min-height: 30px;
                    border-radius: 5px;
                    margin: 3px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #ACB0BE;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    background: none;
                    height: 0px;
                }
                QScrollBar:horizontal {
                    background-color: #EFF1F5;
                    height: 12px;
                    margin: 0px;
                }
                QScrollBar::handle:horizontal {
                    background-color: #CCCFD9;
                    min-width: 30px;
                    border-radius: 5px;
                    margin: 3px;
                }
                QScrollBar::handle:horizontal:hover {
                    background-color: #ACB0BE;
                }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    background: none;
                    width: 0px;
                }
            """)
            self.folder_icon_color = "#FE640B"  # 文件夹使用深橙色
            self.file_icon_color = "#40A02B"  # 文件使用深绿色
            self.copy_icon_color = "#1E66F5"  # 复制按钮使用深蓝色
            self.error_color = "#D20F39"  # 错误使用深红色
            self.header_text_color = "#4C4F69"  # 亮色模式下的标题文字颜色
            self.tool_button_text_color = "#FFFFFF"  # 亮色模式下工具按钮文字颜色
            self.dark_mode = False

    def toggle_theme(self):
        """切换暗色和亮色主题。"""
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        self.setup_theme()
        # 刷新文件树样式
        if self.current_path:
            self.generate_file_tree(self.current_path)
        self.show_message("已切换为" + ("亮色" if self.theme_mode == "light" else "暗色") + "主题")

        # 更新工具栏按钮图标
        self.update_toolbar_icons()
        self.update()  # 刷新 UI

    def create_custom_icon(self, icon_type, color_hex):
        """创建自定义颜色的图标"""
        # 为不同类型的图标创建不同的SVG内容
        svg_content = ""
        if icon_type == "folder-open":
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path fill="{color_hex}" d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/>
            </svg>
            """
        elif icon_type == "refresh":
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path fill="{color_hex}" d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
            </svg>
            """
        elif icon_type == "theme":
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path fill="{color_hex}" d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9zm0 16c-3.86 0-7-3.14-7-7s3.14-7 7-7 7 3.14 7 7-3.14 7-7 7z"/>
                <path fill="{color_hex}" d="M12 17.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
            </svg>
            """
        elif icon_type == "file":
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path fill="{color_hex}" d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
            </svg>
            """
        elif icon_type == "folder":
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path fill="{color_hex}" d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
            </svg>
            """
        elif icon_type == "copy":
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path fill="{color_hex}" d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
            </svg>
            """
        elif icon_type == "warning":
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path fill="{color_hex}" d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
            </svg>
            """
        else:  # 默认图标
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path fill="{color_hex}" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
            </svg>
            """

        # 将SVG转换为QPixmap
        pixmap = QPixmap()
        pixmap.loadFromData(bytes(svg_content, 'utf-8'))

        # 创建QIcon
        return QIcon(pixmap)

    def update_toolbar_icons(self):
        """更新工具栏按钮图标"""
        # 遍历工具栏上的所有按钮并更新其图标
        for action in self.toolbar.actions():
            action_text = action.text()
            if action_text == "选择文件夹":
                action.setIcon(self.create_custom_icon("folder-open",
                                                       self.tool_button_text_color))
            elif action_text == "刷新":
                action.setIcon(self.create_custom_icon("refresh",
                                                       self.tool_button_text_color))
            elif action_text == "切换主题":
                action.setIcon(self.create_custom_icon("theme",
                                                       self.tool_button_text_color))

    def setup_ui(self):
        """设置用户界面。"""
        # 工具栏 - 放在顶部
        self.toolbar = QToolBar("工具栏")
        self.toolbar.setIconSize(QSize(22, 22))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        # 工具栏按钮 - 使用自定义图标
        pick_action = QAction("选择文件夹", self)
        pick_action.triggered.connect(self.pick_directory)
        pick_action.setStatusTip("选择要分析的文件夹")
        self.toolbar.addAction(pick_action)

        self.toolbar.addSeparator()

        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(self.refresh_current_directory)
        refresh_action.setStatusTip("刷新当前文件夹视图")
        self.toolbar.addAction(refresh_action)

        self.toolbar.addSeparator()

        theme_action = QAction("切换主题", self)
        theme_action.triggered.connect(self.toggle_theme)
        theme_action.setStatusTip("在亮色和暗色主题之间切换")
        self.toolbar.addAction(theme_action)

        # 添加一个伸缩器以使后面的工具栏项右对齐
        empty_label = QLabel()
        empty_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(empty_label)
        self.toolbar.addSeparator()

        # 添加右对齐的应用标题
        app_title = QLabel("文件树管理器")
        app_title.setStyleSheet("font-weight: bold; margin-right: 10px;")
        self.toolbar.addWidget(app_title)

        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # 创建分割器 - 允许用户调整左右面板比例
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        # 左侧：文件树视图，添加边框和阴影
        tree_frame = QFrame()
        tree_layout = QVBoxLayout(tree_frame)
        tree_layout.setContentsMargins(0, 0, 0, 0)

        tree_header = QLabel("文件结构")
        tree_header.setProperty("labelType", "header")
        tree_header.setStyleSheet("font-weight: bold; font-size: 13px; margin-bottom: 5px;")
        tree_layout.addWidget(tree_header)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setFont(self.tree_font)
        self.tree_widget.setHeaderLabels(["名称", "类型", "修改时间", "大小"])

        # 设置列宽度，但允许名称列自动调整
        header = self.tree_widget.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 名称列自动伸缩填充可用空间
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # 类型列固定宽度
        header.setSectionResizeMode(2, QHeaderView.Fixed)  # 时间列固定宽度
        header.setSectionResizeMode(3, QHeaderView.Fixed)  # 大小列固定宽度

        # 设置初始列宽
        self.tree_widget.setColumnWidth(1, 100)
        self.tree_widget.setColumnWidth(2, 200)  # 确保时间列足够显示完整时间
        self.tree_widget.setColumnWidth(3, 100)

        # 设置工具提示，当名称被截断时显示全名
        self.tree_widget.setItemsExpandable(True)
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)  # 点击项目时更新状态栏
        tree_layout.addWidget(self.tree_widget)

        # 右侧：文本输出和复制按钮
        text_frame = QFrame()
        text_layout = QVBoxLayout(text_frame)
        text_layout.setContentsMargins(0, 0, 0, 0)

        text_header = QLabel("目录文本结构输出")
        text_header.setProperty("labelType", "header")
        text_header.setStyleSheet("font-weight: bold; font-size: 13px; margin-bottom: 5px;")
        text_layout.addWidget(text_header)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        text_layout.addWidget(self.text_edit)

        copy_layout = QHBoxLayout()

        self.copy_button = QPushButton("复制到剪贴板")
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        copy_layout.addWidget(self.copy_button)

        text_layout.addLayout(copy_layout)

        # 将框架添加到分割器
        splitter.addWidget(tree_frame)
        splitter.addWidget(text_frame)
        splitter.setSizes([int(self.width() * 0.6), int(self.width() * 0.4)])  # 初始分割比例

        main_layout.addWidget(splitter)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("准备就绪，请选择文件夹或拖放文件夹到应用窗口")

        # 初始化工具栏图标
        self.update_toolbar_icons()

    def on_tree_item_clicked(self, item, column):
        """处理树视图项目点击事件，更新状态栏信息"""
        if item:
            path = item.data(0, Qt.UserRole)
            if path:
                self.status_bar.showMessage(f"已选择: {path}")

    def refresh_current_directory(self):
        """刷新当前目录视图"""
        if self.current_path and os.path.exists(self.current_path):
            self.process_selected_directory(self.current_path)
            self.show_message("已刷新文件夹视图")
        else:
            self.show_error("没有当前文件夹可刷新")

    def dragEnterEvent(self, event: QDragEnterEvent):
        """处理拖入事件以支持拖放。"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """处理放下事件以支持拖放。"""
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if os.path.isdir(path):
                self.process_selected_directory(path)
            else:
                self.show_error("请拖放文件夹而非文件")

    def show_context_menu(self, position):
        """显示右键上下文菜单。"""
        item = self.tree_widget.itemAt(position)
        if item:
            path = item.data(0, Qt.UserRole)
            name = item.text(0)

            menu = QMenu(self)

            # 打开项目
            if os.path.isdir(path):
                open_action = menu.addAction("在资源管理器中打开")
                open_action.triggered.connect(lambda: self.open_in_explorer(path))
                open_action.setIcon(self.create_custom_icon("folder-open", self.folder_icon_color))
            elif os.path.isfile(path):
                open_action = menu.addAction("打开文件")
                open_action.triggered.connect(lambda: self.open_file(path))
                open_action.setIcon(self.create_custom_icon("file", self.file_icon_color))

            menu.addSeparator()

            # 复制选项
            copy_name_action = menu.addAction("复制名称")
            copy_name_action.triggered.connect(lambda: self.copy_item_info(name))
            copy_name_action.setIcon(self.create_custom_icon("copy", self.copy_icon_color))

            copy_path_action = menu.addAction("复制绝对路径")
            copy_path_action.triggered.connect(lambda: self.copy_item_info(self.normalize_path(path)))
            copy_path_action.setIcon(self.create_custom_icon("copy", self.copy_icon_color))

            if self.current_path:
                rel_path = os.path.relpath(path, self.current_path)
                rel_path = self.normalize_path(rel_path)
                copy_rel_action = menu.addAction("复制相对路径")
                copy_rel_action.triggered.connect(lambda: self.copy_item_info(rel_path))
                copy_rel_action.setIcon(self.create_custom_icon("copy", self.copy_icon_color))

            menu.exec_(self.tree_widget.mapToGlobal(position))

    def normalize_path(self, path):
        """统一路径分隔符，根据操作系统使用正确的分隔符"""
        # 在Windows上，使用标准的反斜杠作为路径分隔符
        if platform.system() == "Windows":
            return path.replace('/', '\\')
        # 在其他平台上，使用标准的正斜杠
        else:
            return path.replace('\\', '/')

    def open_in_explorer(self, path):
        """在系统文件浏览器中打开文件夹"""
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{path}"')
        else:  # Linux和其他系统
            os.system(f'xdg-open "{path}"')
        self.show_message(f"已在文件浏览器中打开: {path}")

    def open_file(self, path):
        """使用系统默认应用打开文件"""
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{path}"')
        else:  # Linux和其他系统
            os.system(f'xdg-open "{path}"')
        self.show_message(f"已打开文件: {path}")

    def pick_directory(self):
        """打开文件夹选择对话框。"""
        path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if path:
            self.process_selected_directory(path)

    def process_selected_directory(self, path):
        """处理选中的文件夹。"""
        self.current_path = path
        # 标准化路径
        normalized_path = self.normalize_path(path)
        self.status_bar.showMessage(f"当前路径: {normalized_path}")
        self.generate_file_tree(path)
        self.generate_file_tree_text(path)
        self.copy_button.setEnabled(True)

    def generate_file_tree(self, root_path):
        """生成文件树视图。"""
        self.tree_widget.clear()
        if not os.path.exists(root_path):
            self.show_error("路径不存在")
            return

        # 创建根项
        root_name = os.path.basename(root_path)
        if not root_name:  # 处理根目录情况
            root_name = root_path

        root_item = QTreeWidgetItem(self.tree_widget, [root_name])
        root_item.setData(0, Qt.UserRole, root_path)

        # 设置使用自定义图标
        folder_icon = self.create_custom_icon("folder", self.folder_icon_color)
        root_item.setIcon(0, folder_icon)
        root_item.setForeground(0, QColor(self.folder_icon_color))
        root_item.setExpanded(True)

        # 设置工具提示显示完整路径
        root_item.setToolTip(0, root_path)

        # 设置为加粗，以突出显示
        bold_font = self.tree_font
        bold_font.setBold(True)
        root_item.setFont(0, bold_font)

        self.add_directory_contents(root_path, root_item)

        # 调整列宽以适应内容
        self.tree_widget.header().setStretchLastSection(False)
        # 最后重新确认第一列是伸缩的
        self.tree_widget.header().setSectionResizeMode(0, QHeaderView.Stretch)

    def format_access_error(self, error, path):
        """格式化访问错误信息，提供更清晰的提示"""
        if isinstance(error, PermissionError):
            # 针对权限错误提供更明确的提示
            if platform.system() == "Windows":
                return "需要管理员权限访问"
            else:
                return "需要权限访问 (sudo)"
        elif isinstance(error, FileNotFoundError):
            return "文件或目录不存在"
        else:
            # 其他类型的错误保持简洁
            return f"访问受限: {type(error).__name__}"

    def add_directory_contents(self, directory_path, parent_item):
        """将文件夹内容添加到树视图。"""
        try:
            entries = os.listdir(directory_path)

            # 分离并排序目录和文件
            dirs = [(e, os.path.join(directory_path, e)) for e in entries if
                    os.path.isdir(os.path.join(directory_path, e)) and not e.startswith('.')]
            files = [(e, os.path.join(directory_path, e)) for e in entries if
                     os.path.isfile(os.path.join(directory_path, e)) and not e.startswith('.')]
            dirs.sort(key=lambda x: x[0].lower())
            files.sort(key=lambda x: x[0].lower())

            # 添加文件夹
            for name, path in dirs:
                item = QTreeWidgetItem(parent_item, [name])
                item.setData(0, Qt.UserRole, path)

                # 设置自定义图标和颜色
                folder_icon = self.create_custom_icon("folder", self.folder_icon_color)
                item.setIcon(0, folder_icon)
                item.setForeground(0, QColor(self.folder_icon_color))

                # 设置工具提示显示完整路径
                item.setToolTip(0, path)

                try:
                    stats = os.stat(path)
                    item.setText(1, "文件夹")

                    # 完整显示修改时间
                    mod_time = datetime.datetime.fromtimestamp(stats.st_mtime)
                    item.setText(2, mod_time.strftime("%Y-%m-%d %H:%M:%S"))
                    # 设置时间列的工具提示
                    item.setToolTip(2, mod_time.strftime("%Y-%m-%d %H:%M:%S"))

                    try:
                        item_count = len(os.listdir(path))
                        item.setText(3, f"{item_count} 项")
                    except (PermissionError, FileNotFoundError) as e:
                        # 使用更友好的错误提示
                        error_msg = self.format_access_error(e, path)
                        item.setText(3, error_msg)
                        item.setToolTip(3, f"错误: {str(e)}")
                        # 设置警告图标
                        warning_icon = self.create_custom_icon("warning", self.error_color)
                        item.setIcon(3, warning_icon)

                    # 递归添加子目录内容
                    self.add_directory_contents(path, item)

                except (PermissionError, FileNotFoundError) as e:
                    # 使用更友好的错误提示
                    error_msg = self.format_access_error(e, path)
                    item.setText(1, "访问受限")
                    item.setText(3, error_msg)
                    item.setToolTip(1, f"错误: {str(e)}")
                    item.setForeground(0, QColor(self.error_color))
                    # 设置警告图标
                    warning_icon = self.create_custom_icon("warning", self.error_color)
                    item.setIcon(1, warning_icon)

            # 添加文件
            for name, path in files:
                item = QTreeWidgetItem(parent_item, [name])
                item.setData(0, Qt.UserRole, path)

                # 设置自定义文件图标和颜色
                file_icon = self.create_custom_icon("file", self.file_icon_color)
                item.setIcon(0, file_icon)
                item.setForeground(0, QColor(self.file_icon_color))

                # 设置工具提示显示完整路径
                item.setToolTip(0, path)

                try:
                    stats = os.stat(path)
                    file_type = self.get_file_type(name)
                    item.setText(1, file_type)
                    item.setToolTip(1, file_type)

                    # 完整显示修改时间
                    mod_time = datetime.datetime.fromtimestamp(stats.st_mtime)
                    mod_time_str = mod_time.strftime("%Y-%m-%d %H:%M:%S")
                    item.setText(2, mod_time_str)
                    item.setToolTip(2, mod_time_str)

                    size_str = self.format_size(stats.st_size)
                    item.setText(3, size_str)
                    item.setToolTip(3, f"{stats.st_size} 字节 ({size_str})")
                except (PermissionError, FileNotFoundError) as e:
                    # 使用更友好的错误提示
                    error_msg = self.format_access_error(e, path)
                    item.setText(1, "访问受限")
                    item.setText(3, error_msg)
                    item.setToolTip(1, f"错误: {str(e)}")
                    item.setForeground(0, QColor(self.error_color))
                    # 设置警告图标
                    warning_icon = self.create_custom_icon("warning", self.error_color)
                    item.setIcon(1, warning_icon)

        except (PermissionError, FileNotFoundError) as e:
            # 使用更友好的错误提示
            error_msg = self.format_access_error(e, directory_path)
            error_item = QTreeWidgetItem(parent_item, [f"访问受限"])
            error_item.setForeground(0, QColor(self.error_color))
            error_item.setText(1, error_msg)
            error_item.setToolTip(0, f"错误信息: {str(e)}")
            # 设置警告图标
            warning_icon = self.create_custom_icon("warning", self.error_color)
            error_item.setIcon(0, warning_icon)

    def generate_file_tree_text(self, root_path):
        """生成文件树的文本输出。"""
        if not os.path.exists(root_path):
            self.text_edit.setText("路径不存在")
            return

        root_name = os.path.basename(root_path)
        if not root_name:  # 处理根目录情况
            root_name = root_path

        result = [root_name]
        self.add_directory_to_result(root_path, result, "")
        self.text_edit.setText("\n".join(result))

    def add_directory_to_result(self, directory, result, prefix):
        """递归地将文件夹内容添加到文本输出。"""
        try:
            entries = os.listdir(directory)

            # 分离并排序目录和文件
            directories = [d for d in entries if os.path.isdir(os.path.join(directory, d)) and not d.startswith('.')]
            files = [f for f in entries if os.path.isfile(os.path.join(directory, f)) and not f.startswith('.')]

            directories.sort(key=str.lower)
            files.sort(key=str.lower)

            # 添加目录
            for i, dirname in enumerate(directories):
                is_last = (i == len(directories) - 1 and not files)
                result.append(f"{prefix}{'└──' if is_last else '├──'} {dirname}")
                self.add_directory_to_result(os.path.join(directory, dirname), result,
                                             prefix + ("    " if is_last else "│   "))

            # 添加文件
            for i, filename in enumerate(files):
                result.append(f"{prefix}{'└──' if i == len(files) - 1 else '├──'} {filename}")

        except (PermissionError, FileNotFoundError) as e:
            # 使用更友好的错误提示
            error_msg = self.format_access_error(e, directory)
            result.append(f"{prefix}└── [权限受限: {error_msg}]")

    def copy_to_clipboard(self):
        """将文本输出复制到剪贴板。"""
        text = self.text_edit.toPlainText()
        if text:
            pyperclip.copy(text)
            self.show_message("文件树结构已复制到剪贴板")
        else:
            self.show_error("没有可复制的文件树内容")

    def copy_item_info(self, text):
        """将项目信息复制到剪贴板。"""
        pyperclip.copy(text)
        self.show_message(f"已复制: {text}")

    def show_message(self, message):
        """在状态栏显示临时消息，2秒后恢复为当前路径。"""
        self.status_bar.showMessage(message, 2000)
        # 2秒后恢复显示当前路径
        if self.current_path:
            # 使用QTimer创建延迟恢复状态
            QTimer.singleShot(2000, lambda: self.status_bar.showMessage(
                f"当前路径: {self.normalize_path(self.current_path)}"))
        else:
            QTimer.singleShot(2000, lambda: self.status_bar.showMessage("准备就绪，请选择文件夹或拖放文件夹到应用窗口"))

    def show_error(self, message):
        """在状态栏显示错误消息。"""
        self.status_bar.showMessage(f"错误: {message}", 3000)
        # 使用QTimer创建延迟恢复状态
        if self.current_path:
            QTimer.singleShot(3000, lambda: self.status_bar.showMessage(
                f"当前路径: {self.normalize_path(self.current_path)}"))
        else:
            QTimer.singleShot(3000, lambda: self.status_bar.showMessage("准备就绪，请选择文件夹或拖放文件夹到应用窗口"))

    def format_size(self, size_bytes):
        """将文件大小格式化为易读的字符串。"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

    def get_file_type(self, filename):
        """获取文件类型描述。"""
        ext = os.path.splitext(filename)[1].lower()
        types = {
            '.txt': "文本文件", '.md': "Markdown文件", '.log': "日志文件",
            '.py': "Python文件", '.js': "JavaScript文件", '.html': "HTML文件",
            '.css': "CSS文件", '.java': "Java文件", '.c': "C文件",
            '.cpp': "C++文件", '.h': "头文件", '.hpp': "C++头文件",
            '.jpg': "JPEG图像", '.jpeg': "JPEG图像", '.png': "PNG图像",
            '.gif': "GIF图像", '.bmp': "BMP图像", '.tiff': "TIFF图像",
            '.svg': "SVG矢量图", '.webp': "WebP图像",
            '.mp3': "MP3音频", '.wav': "WAV音频", '.ogg': "OGG音频",
            '.flac': "FLAC音频", '.aac': "AAC音频", '.wma': "WMA音频",
            '.mp4': "MP4视频", '.avi': "AVI视频", '.mov': "MOV视频",
            '.mkv': "MKV视频", '.wmv': "WMV视频", '.webm': "WebM视频",
            '.pdf': "PDF文档", '.doc': "Word文档", '.docx': "Word文档",
            '.xls': "Excel表格", '.xlsx': "Excel表格", '.csv': "CSV表格",
            '.ppt': "PowerPoint演示", '.pptx': "PowerPoint演示",
            '.zip': "ZIP压缩包", '.rar': "RAR压缩包", '.7z': "7Z压缩包",
            '.tar': "TAR归档", '.gz': "GZ压缩包", '.bz2': "BZ2压缩包",
            '.exe': "可执行程序", '.msi': "安装程序", '.bat': "批处理脚本",
            '.sh': "Shell脚本", '.json': "JSON文件", '.xml': "XML文件",
            '.yaml': "YAML文件", '.sql': "SQL脚本", '.db': "数据库文件",
            '.ini': "配置文件", '.cfg': "配置文件", '.conf': "配置文件",
            '.dll': "动态链接库", '.so': "共享库", '.dylib': "动态库"
        }
        return types.get(ext, "文件")


if __name__ == "__main__":
    app = QApplication(sys.argv)


    # 确保使用绝对路径或资源路径获取图标
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)


    # 设置应用程序图标
    app_icon = QIcon(resource_path('favicon.ico'))
    app.setWindowIcon(app_icon)

    # 创建应用实例
    window = FileExplorerApp()

    # Windows 任务栏特定设置
    if platform.system() == "Windows":
        import ctypes

        app_id = 'zisuda.filetreevisualizer.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    window.show()
    sys.exit(app.exec())