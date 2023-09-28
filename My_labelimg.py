# 把所有和UI有关的代码都放在一个类里面，创建窗口只要创建类的实例就可以了
# 通过QDesktopWidget类相应的API可以得到整个屏幕的尺寸,通过move方法移动窗口
# 用到了水平布局和垂直布局，引入QHBoxLayout，QVBoxLayout
# 需要一个控件，引入了QWidget，QWidget是所有的可视控件的基类
# 需要butoon，引入了QPushButton，按钮有多个控件，它的父类QAbstractButton
# 显示控件的提示信息需要用到 QToolTip(setToolTip)
# 通过QIcon设置窗口图标
# 通过QPixmap加载图片
# 对话框的基类QDialog
# 在基类基础上有五种对话框
# QMessageBox 消息对话框 关于,错误,警告,提问,消息对话框
# QColorDialog 颜色对话框
# QFileDialog  显示文件打开或保存对话框
# QFontDialog  设置字体对话框
# QInputDialog  输入信息对话框
# 文件对话框 QFileDialog最常用的是打开文件和保存文件对话框
import sys
import os
# 从PyQt里面创建窗口和应用
import random

from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QApplication, QWidget
from PyQt5.QtWidgets import QListView, QLineEdit, QDialogButtonBox
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QToolTip, QAction, QSizePolicy, QFrame
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMenu, QInputDialog
# 用来添加图标
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, QStringListModel, QDir
from PyQt5 import QtPrintSupport, QtGui, QtWidgets, QtCore
from PyQt5.QtPrintSupport import QPageSetupDialog, QPrintDialog, QPrinter
from PyQt5.QtCore import QRect, QRectF,QPointF,QPoint
from PyQt5.QtGui import QPen, QPainter, QColor


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        # 创建并设置一个名为"Dialog"的对话框
        Dialog.setObjectName("Dialog")
        Dialog.resize(285, 336)  # 设置对话框的大小为 285x336

        # 设置对话框的尺寸策略为 Preferred，不进行水平或垂直的拉伸
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)

        # 设置对话框的最小和最大尺寸均为 285x336
        Dialog.setMinimumSize(QtCore.QSize(285, 336))
        Dialog.setMaximumSize(QtCore.QSize(285, 336))

        # 在对话框中创建一个按钮组
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 39, 193, 28))  # 设置按钮组的位置和尺寸
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)  # 按钮水平排列
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)  # 设置两个标准按钮：取消和确定
        self.buttonBox.setObjectName("buttonBox")

        # 在对话框中创建一个不可编辑的单行文本框
        self.leditChoosedLabel = QLineEdit(Dialog)
        self.leditChoosedLabel.setGeometry(QtCore.QRect(11, 11, 261, 21))  # 设置单行文本框的位置和尺寸
        self.leditChoosedLabel.setObjectName("leditChoosedLabel")
        # self.leditChoosedLabel.setEnabled(False)  # 设置单行文本框为不可编辑状态

        # 在对话框中创建一个列表视图，用于显示标签
        self.listView = QListView(Dialog)
        self.listView.setGeometry(QtCore.QRect(10, 80, 261, 241))  # 设置列表视图的位置和尺寸
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 设置列表项不可编辑
        self.listView.setObjectName("listView")

        # PyQt(和PySide) 的一个非常有用的方法，主要用于自动连接通过特定命名定命名on_myButton_clicked的槽
        # 当你创建一个 PyQt 应用时，你可能会使用设计师（Qt Designer）来设计你的界面，设计师允许你为部件设置一个“对象名称”（object name)
        # 利用这个特性，你可以使用 connectSlotsByName 方法来自动连接信号和槽，而不需要手动为每个信号写一个 connect 语句。
        QtCore.QMetaObject.connectSlotsByName(Dialog)


# 这个类扩展了上面的Ui_Dialog，添加了实际的功能。
class DialogChoooseLabelWin(QDialog, Ui_Dialog):
    def __init__(self, local_pos,label_rect, parent=None):
        super(DialogChoooseLabelWin, self).__init__()
        QDialog.__init__(self, parent)
        self.label_rect=label_rect
        self.local_pos =local_pos
        self.setupUi(self)
        self.labelList = ["object1","object2","object3"]
        self.initLableList()
        self.buttonBox.accepted.connect(self.validate)
        self.buttonBox.rejected.connect(self.reject)
        self.listView.clicked.connect(self.clickedlist)

    def initLableList(self):
        self.move(self.local_pos)
        for data in self.label_rect:
            self.labelList.append(data[4])
        self.labelList = list(set(self.labelList))
        self.labelslm = QStringListModel()
        self.labelslm.setStringList(self.labelList)
        self.listView.setModel(self.labelslm)

    def clickedlist(self, qModelIndex):
        self.leditChoosedLabel.setText(self.labelList[qModelIndex.row()])

    def getValue(self):
        return self.leditChoosedLabel.text()

    def validate(self):
        if self.leditChoosedLabel.text() != '':
            self.accept()


# 定义一个类，这个类从QMainWindow里面继承
class ImageLabel(QLabel):
    def __init__(self,listWidget_file, listWidget_label, parent=None):
        super(QLabel, self).__init__(parent)
        self.labelindex = 0
        self.seed=1
        self.image_transparency = 0.2
        self.label_rect_List = []
        self.imagedict = {}
        self.rect = QRectF()
        self.selected_rect_fillColor=QRect()
        self.selectedRect = None
        self.resizing = False
        self.moving = False
        self.menu = True
        self.hovered = False
        self.Rightpress= False
        self.startPos = None
        self.setMouseTracking(True)
        self.listWidget_label = listWidget_label
        self.listWidget_file = listWidget_file

    def wheelEvent(self, event):
        # 滚轮事件缩放图片
        angle = event.angleDelta().y()
        factor = 1.1 if angle > 0 else 0.9
        old_scale_factor = self.scale_factor
        self.scale_factor *= factor
        self.scale_factor = min(max(self.scale_factor, 0.1), 5.0)  # 限制缩放范围

        # 获取鼠标相对于图片的位置
        mouse_pos = event.pos()

        # 计算新的图片位置
        new_width = self.scale_factor * self.pixmap().size().width()
        new_height = self.scale_factor * self.pixmap().size().height()
        old_width = old_scale_factor * self.pixmap().size().width()
        old_height = old_scale_factor * self.pixmap().size().height()

        delta_width = new_width - old_width
        delta_height = new_height - old_height
        # 分配制
        ratio_x = mouse_pos.x() / old_width
        ratio_y = mouse_pos.y() / old_height

        # 调整QLabel的位置
        self.move(int(self.x() - delta_width * ratio_x), int(self.y() - delta_height * ratio_y))
        self.resize(int(new_width), int(new_height))

        # 计算新的矩形框的位置,新的文本框的位置
        for i in range(len(self.label_rect_List)):
            self.label_rect_List[i][0]=self.label_rect_List[i][0]* (self.scale_factor / old_scale_factor)
            self.label_rect_List[i][1]=self.label_rect_List[i][1]* (self.scale_factor / old_scale_factor)
            self.label_rect_List[i][2]=self.label_rect_List[i][2]* (self.scale_factor / old_scale_factor)
            self.label_rect_List[i][3]=self.label_rect_List[i][3]* (self.scale_factor / old_scale_factor)

    # 鼠标按下事件
    def mousePressEvent(self, event):
        # 绘制矩形框起点
        if event.button() == Qt.LeftButton:
            self.startPos=event.pos()
            self.start_x = event.pos().x()
            self.start_y = event.pos().y()

        # 中键移动
        elif event.button() == Qt.MidButton:

            # event.globalPos()相对于整个屏幕的坐标
            # self.frameGeometry().topLeft()用于获取窗口的左上角位置相对于主窗口
            # self.frameGeometry()返回一个QRect对象，表示窗口的几何属性，包括位置、大小和边框等。

            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(QCursor(Qt.ClosedHandCursor))
            event.accept()

        # 移动，修改矩形框
        elif event.button() == Qt.RightButton:
            self.startPos = event.pos()
            self.menu=True
            for index, data in enumerate(self.label_rect_List):
                rect = QRectF(QPointF(data[0], data[1]), QPointF(data[2], data[3]))
                left_top = abs(rect.left() - self.startPos.x()) < 15 and abs(rect.top() - self.startPos.y()) < 15
                right_top = abs(rect.right() - self.startPos.x()) < 15 and abs(rect.top() - self.startPos.y()) < 15
                left_bottom = abs(rect.left() - self.startPos.x()) < 15 and abs(rect.bottom() - self.startPos.y()) < 15
                right_bottom = abs(rect.right() - self.startPos.x()) < 15 and abs(
                    rect.bottom() - self.startPos.y()) < 15

                if rect.contains(self.startPos) or left_top or left_bottom or right_top or right_bottom:
                    self.selectedRect = rect
                    self.text_index = index
                    self.seed = index
                    if left_top:
                        self.resizing = True
                        self.flag = 1
                    elif right_top:
                        self.resizing = True
                        self.flag = 2
                    elif left_bottom:
                        self.resizing = True
                        self.flag = 3
                    elif right_bottom:
                        self.resizing = True
                        self.flag = 4
                    elif rect.contains(self.startPos):
                        self.moving = True
                        self.Rightpress = True
                        self.image_transparency = 0.6
                else:
                    self.Rightpress = False
                    self.image_transparency = 0.2
            self.update()
    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        # 绘制矩形框终点
        if event.button() == Qt.LeftButton:
            try:
                if self.end_x < self.start_x:
                    # 如果终点在起点的左侧，则交换 x 坐标
                    self.start_x, self.end_x = self.end_x, self.start_x

                if self.end_y < self.start_y:
                    # 如果终点高于起点，则交换 y 坐标
                    self.start_y, self.end_y = self.end_y, self.start_y
            except  AttributeError:
                return

            local_pos = self.mapToGlobal(QPoint(int(self.rect.right()), int(self.rect.bottom())))
            # 获得标签名
            dialogChooseLabel = DialogChoooseLabelWin(local_pos,self.label_rect_List)
            if dialogChooseLabel.exec_():
                label_name = dialogChooseLabel.getValue()
                self.save_data(label_name)

                item = QListWidgetItem(label_name)
                item.setCheckState(Qt.Checked)  # 设置为选中状态
                self.listWidget_label.addItem(item)

            current_row = self.listWidget_file.currentRow()
            current_image = self.listWidget_file.item(current_row).text()
            if self.label_rect_List:
                self.imagedict[current_image]=self.label_rect_List
            self.rect=QRectF()

        elif event.button() == Qt.MidButton:
            self.drag_position = None
            self.setCursor(QCursor(Qt.OpenHandCursor))
            event.accept()

        elif event.button() == Qt.RightButton:
            self.moving = False
            self.resizing = False
            # self.selectedRect = None


    # 与event.button()不同，event.buttons()返回在事件发生时所有被按下的按钮的组合
    # 使用了位运算符 & 来检查特定的按钮是否被按下。这是因为event.buttons()实际上返回了一个位掩码，代表所有被按下的按钮。
    def mouseMoveEvent(self, event):
        self.mouse_pos = event.pos()
        self.update()
        for index, data in enumerate(self.label_rect_List): #问题self.hovered的值取决于最后一个rect需要加上breck
            rect = QRectF(QPointF(data[0], data[1]), QPointF(data[2], data[3]))
            if rect.contains(self.mouse_pos):
                self.hovered = True
                self.selected_rect_fillColor=rect
                break
            else:
                if not self.Rightpress:
                    self.hovered = False

        # 实时绘制矩形框
        if event.buttons() & Qt.LeftButton:
            self.end_x = event.pos().x()
            self.end_y = event.pos().y()
            self.rect = QRectF(self.startPos, event.pos())
            self.update()

        elif event.buttons() & Qt.MidButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

        elif event.buttons() & Qt.RightButton:
            self.menu=False
            if self.selectedRect:
                if self.moving:
                    dx = event.x() - self.startPos.x()
                    dy = event.y() - self.startPos.y()
                    # self.selectedRect.translate(dx, dy)  # 将矩形在x和y方向上平移指定的距离，其实改变了rectlist
                    self.label_rect_List[self.text_index][0] = self.label_rect_List[self.text_index][0] + dx
                    self.label_rect_List[self.text_index][1] = self.label_rect_List[self.text_index][1] + dy
                    self.label_rect_List[self.text_index][2] = self.label_rect_List[self.text_index][2] + dx
                    self.label_rect_List[self.text_index][3] = self.label_rect_List[self.text_index][3] + dy
                    self.startPos = event.pos()
                    self.update()

                elif self.resizing:
                    if self.flag == 1:
                        self.selectedRect.setTopLeft(event.pos())
                        self.label_rect_List[self.text_index][0] = event.pos().x()
                        self.label_rect_List[self.text_index][1] = event.pos().y()
                    elif self.flag == 2:
                        self.selectedRect.setTopRight(event.pos())
                        self.label_rect_List[self.text_index][2] = event.pos().x()
                        self.label_rect_List[self.text_index][1] = event.pos().y()
                    elif self.flag == 3:
                        self.selectedRect.setBottomLeft(event.pos())
                        self.label_rect_List[self.text_index][0] = event.pos().x()
                        self.label_rect_List[self.text_index][3] = event.pos().y()
                    elif self.flag == 4:
                        self.selectedRect.setBottomRight(event.pos())
                        self.label_rect_List[self.text_index][2] = event.pos().x()
                        self.label_rect_List[self.text_index][3] = event.pos().y()

            self.update()


    def contextMenuEvent(self, event):
        if self.menu:
            if self.selectedRect:
                context_menu = QMenu(self)

                action1 = QAction("Delete", self)
                context_menu.addAction(action1)
                action1.triggered.connect(self.deleteItem)

                action2 = QAction("Modify", self)
                context_menu.addAction(action2)
                action2.triggered.connect(self.modifyItem)

                context_menu.exec_(event.globalPos())

    def deleteItem(self):

        self.listWidget_label.takeItem(self.text_index)
        self.label_rect_List.pop(self.text_index)

    def modifyItem(self):
        # 弹出一个对话框以获得新的文本
        text, ok = QInputDialog.getText(self, 'Modify item', '修改标签:',
                                        text=self.label_rect_List[self.text_index][4])
        if ok:
            print(self.label_rect_List)
            item=self.listWidget_label.item(self.text_index)
            item.setText(text) # 触发了label
            print(self.label_rect_List)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        # 一个用于设置绘图器(QPainter)的渲染提示的函数。其中QPainter.Antialiasing是一个枚举值，表示抗锯齿渲染提示。
        # 抗锯齿是一种图形渲染技术，通过对图形边缘进行平滑处理，使得边缘看起来更加平滑，减少锯齿状的边缘出现，提高图形的质  量和细节。
        # 当使用painter.setRenderHint(QPainter.Antialiasing)时，绘图器将应用抗锯齿渲染提示，
        # 以在绘制图形时实现平滑的边缘效果。这通常用于绘制需要更高质量的图形，例如曲线、圆形和其他具有平滑边缘的图形。
        # 使用抗锯齿渲染提示可能会增加绘图的计算成本，因为绘图器需要进行额外的计算来实现平滑效果。
        # 因此，如果绘图操作较为简单，或者对于绘制的图形质量要求不高，可以选择不使用抗锯齿渲染提示，以提高绘图的性能。
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
        painter.drawRect(self.rect)
        for data in self.label_rect_List:
            # 绘制矩形框
            painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
            painter.drawRect(QRectF(QPointF(data[0],data[1]),QPointF(data[2],data[3])))
            # 绘制文字
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawText(QPointF(data[0],data[1]-3), data[4])

        # # 绘制横向辅助线
        # painter.setPen(QColor(200, 200, 200))
        # painter.drawLine(0, self.height() // 2, self.width(), self.height() // 2)
        #
        # # 绘制纵向辅助线
        # painter.setPen(QColor(200, 200, 200))
        # painter.drawLine(self.width() // 2, 0, self.width() // 2, self.height())

        # 绘制鼠标位置的十字丝
        if hasattr(self, 'mouse_pos'):  # 检查对象 self 是否具有名为 'mouse_pos' 的属性。
            painter.setPen(QColor(255, 0, 0))
            painter.drawLine(0, self.mouse_pos.y(), self.width(), self.mouse_pos.y())
            painter.drawLine(self.mouse_pos.x(), 0, self.mouse_pos.x(), self.height())
        if self.hovered and self.selected_rect_fillColor:
            color = QColor()
            random.seed(self.seed)
            color.setRgbF(random.random(), random.random(), random.random(), self.image_transparency)
            painter.fillRect(self.selected_rect_fillColor, color)


    # data保存到列表
    def save_data(self, label_name):
        data = [self.start_x, self.start_y, self.end_x, self.end_y, label_name, self.labelindex]
        self.label_rect_List.append(data)
        self.labelindex += 1



class Mainwindow(QMainWindow):

    # 初始化
    def __init__(self):
        super(Mainwindow, self).__init__()
        # 调用初始化ui的一个方法
        self.center()
        self.initUI()
        self.printer = QPrinter()
        self.file_path = ''
        self.scale_factor = 1.0
        # 编写初始化UI的方法

    def initUI(self):
        # 设置字体字号
        QToolTip.setFont(QFont('SansSerif', 12))
        # 给窗口设置提示，支持富文本
        self.setToolTip('添加文件读入图片')
        # 设置窗口的位置和尺寸
        # self.setGeometry(x,y,x_width,y,_height)

        # 设置主窗口的标题
        self.setWindowTitle('照片')
        self.setMouseTracking(True)
        # 获取菜单栏
        bar = self.menuBar()
        # 给菜单栏添加 "文件"
        file1 = bar.addMenu("文件")

        # 给文件添加动作 "新建"      # 第一种添加方式
        open_action = file1.addAction("打开")
        open_action.triggered.connect(self.open_file)
        open_action.setShortcut("Ctrl+N")  # 字符间不能加空格

        # 添加动作"文档"
        dir_action = QAction("文件", self)
        dir_action.setShortcut("Ctrl+Shift+N")
        dir_action.triggered.connect(self.loadImageNames)
        file1.addAction(dir_action)

        # 添加动作 "保存" 并设置快捷键
        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file1.addAction(save_action)

        # 添加动作 "保存标签" 并设置快捷键
        save_action = QAction("保存标签", self)
        save_action.setShortcut("Ctrl+Shift+S")
        save_action.triggered.connect(self.saveXml_in_bulk)
        file1.addAction(save_action)

        # 添加动作 "关闭" 并设置快捷键
        quit_action = QAction("关闭", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.Message)
        file1.addAction(quit_action)

        # 创建工具栏
        toolbar = self.addToolBar("file")
        # 添加分隔符
        toolbar.addSeparator()
        # 添加伸展的空白控件
        spacer = QWidget()
        # 用于设置一个占位符小部件（QSpacerItem）的大小策略。
        # 在这个方法中，QSizePolicy.Expanding表示在可用空间内尽可能地扩展，而QSizePolicy.Preferred表示尽量保持小部件的首选大小。
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        # 往工具添加动作,添加图标，添加文本,self  表示放在当前的窗口上
        print = QAction(QIcon('./images/print.jpg'), "打印", self)
        # 添加动作  # 工具栏默认按钮：只显示图标，将文本作为悬停提示展示
        toolbar.addAction(print)
        print.triggered.connect(self.print)

        toolbar.addSeparator()
        # 在工具栏添加“重置位置”按钮
        reset = QAction(QIcon('./images/square.jpg'), "清空", self)
        toolbar.addAction(reset)
        reset.triggered.connect(self.resetImagePosition)

        toolbar.addSeparator()
        # 在工具栏添加“重置位置”按钮
        reset = QAction(QIcon('./images/delete.png'), "", self)
        toolbar.addAction(reset)
        reset.triggered.connect(self.clearRectanges)

        # 添加上一张Button
        self.button_up = QPushButton()
        self.button_up.setMaximumWidth(50)
        self.button_up.setIcon(QIcon("./images/up_image.jpg"))
        self.button_up.clicked.connect(self.up_Image)

        # 添加下一张Button
        self.button_down = QPushButton()
        self.button_down.setMaximumWidth(50)
        self.button_down.setIcon(QIcon("./images/down_image.jpg"))
        self.button_down.clicked.connect(self.down_Image)

        # 创建 QListWidget来显示文件夹内容
        self.listWidget_file = QListWidget(self)
        self.listWidget_file.setMaximumWidth(200)
        self.listWidget_file.currentItemChanged.connect(self.displayImage) #返回值是现在的和之前

        # 设置样式表   list_widget1.setStyleSheet("background-color: yellow;")
        self.listWidget_label = QListWidget(self)
        self.listWidget_label.setMaximumWidth(200)
        self.listWidget_label.itemClicked.connect(self.displayRect)

        # 这里我们为QListWidget设置上下文菜单策略为CustomContextMenu。这意味着我们希望为这个控件提供一个自定义的上下文菜单（也就是当你右键点击时弹出的菜单）。
        # customContextMenuRequested是一个信号，当上下文菜单策略设置为
        # CustomContextMenu并且用户请求一个上下文菜单（通常是通过右键点击）
        self.listWidget_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget_label.customContextMenuRequested.connect(self.showContextMenu)
        # 连接复选框
        self.listWidget_label.itemChanged.connect(self.handleItemChanged)

        # 放置一个主框架并创建一个标签用于显示图片，设置其父部件为centralwidget
        self.centralwidget = QWidget(self)
        self.label_pic = ImageLabel(self.listWidget_file, self.listWidget_label, self.centralwidget)
        self.label_pic.setText("欢迎来到MyPhoto")
        self.label_pic.setFont(QFont("欢迎来到MyPhoto", 18))
        self.label_pic.setScaledContents(True)

        # # 边框     !!边框长度与label控件一致（如果要修改长度，只需要修改上方的setGeometry的第三个参数
        # # 设置边框样式
        # self.label_pic.setFrameShape(QtWidgets.QFrame.Box)
        # # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        # self.label_pic.setFrameShadow(QtWidgets.QFrame.Raised)
        # # 设置背景颜色，包括边框颜色
        # # self.label.setStyleSheet()
        # self.label_pic.setFrameShape(QFrame.Box)
        # # 设置边框样式
        # # 设置背景填充颜色'background-color: rgb(0, 0, 0)'
        # # 设置边框颜色border-color: rgb(255, 170, 0);
        # self.label_pic.setStyleSheet(
        #     'border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);background-color: rgb(100, 149, 237);')
        # # 调整文字与边框的对齐，可以多试几个参数，比如AlignTop
        # self.label_pic.setAlignment(QtCore.Qt.AlignVCenter)

        h_layout_botton = QHBoxLayout()

        h_layout_botton.addWidget(self.button_up)

        # 创建 QVBoxLayout 来管理垂直居中
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label_pic)
        v_layout.setAlignment(self.label_pic, Qt.AlignCenter)

        # 创建水平布局
        h_layout = QHBoxLayout()
        h_layout.addLayout(v_layout)
        h_layout.setAlignment(v_layout, Qt.AlignCenter)

        h_layout_botton.addLayout(h_layout)
        h_layout_botton.addWidget(self.button_down)

        v_layout_list = QVBoxLayout()
        v_layout_list.addWidget(self.listWidget_file)
        v_layout_list.addWidget(self.listWidget_label)

        h_layout_botton.addLayout(v_layout_list)
        # 把主框架放在窗口上
        self.centralwidget.setLayout(h_layout_botton)
        self.setCentralWidget(self.centralwidget)

        self.menuBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.menuBar().customContextMenuRequested.connect(self.contextMenuEvent)
        # 获得状态栏
        self.status = self.statusBar()
        # 在状态栏上，设置消息的状态时间5000ms
        self.status.showMessage('只存在5秒的消息', 5000)

    # 添加center方法，作用就是让窗口居中
    def center(self):
        # 创建实例，获得屏幕对象,得到屏幕的坐标系
        screen = QDesktopWidget().screenGeometry()
        # 设置窗口的尺寸
        self.resize(int(0.618 * screen.width()), int(0.618 * screen.height()))
        # 得到窗口的坐标系
        size = self.frameGeometry()
        # 获取屏幕的宽度、高度
        # 窗口边缘的坐标等于(屏幕的宽度-窗口的宽度)/2
        newLeft = int((screen.width() - size.width()) / 2)
        newTop = int((screen.height() - size.height()) / 2)

        # 移动窗口
        self.move(newLeft, newTop)

    # 按钮的单击事件的方法(自定义的槽)
    def close_window(self):
        sender = self.sender()
        print(sender.text() + '按钮被按下')
        # 得到实例
        app = QApplication.instance()
        # 退出应用程序
        app.quit()

    def Dialog(self):
        # 创建对话框
        dialog = QDialog()
        # 在对话框dialog里面放一个button
        button = QPushButton('确定', dialog)
        # 点击button按钮关闭  现成的槽
        button.clicked.connect(self.close_window)
        # 移动button
        button.move(50, 50)
        # 给dialog设置标题
        dialog.setWindowTitle('对话框')
        # 设置对话框为模式状态，模式状态：即模式状态开启时，对话框窗口里的所有控件不可用
        dialog.setWindowModality(Qt.ApplicationModal)
        # 显示对话框
        dialog.exec()

    def Message(self):
        text = self.sender().text()
        if text == '保存':
            if self.file_path == '':
                # QMessageBox.about(self,'关于','这是一个关于对话框')
                # 两个选项，一个YES,一个No,还有一个默认的值，按回车之后会Yes
                QMessageBox.information(self, '消息', '这是一个消息对话框', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                # QMessageBox.warning(self,'警告','这是一个警告对话框',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                # QMessageBox.critical(self, '错误', '这是一个错误对话框', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                # QMessageBox.question(self, '提问', '这是一个提问对话框', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                # 移动button
                # QMessageBox.exec()
                # QMessageBox.Yes.move(50, 50)
                # QMessageBox.setWindowModality(Qt.ApplicationModal)
                # 导入QMessageBox类，前提是你已经从PyQt或PySide导入了所需的模块
                # 例如：from PyQt5.QtWidgets import QMessageBox
        elif text == '关闭':
            # 创建一个QMessageBox实例
            msgBox = QMessageBox(self)
            # 设置消息框的文本信息
            msgBox.setText("确定退出吗？")
            # 设置消息框的图标为“信息”图标
            msgBox.setIcon(QMessageBox.Information)
            # 为消息框添加自定义按钮，并设置其角色为“行动角色”
            yes = msgBox.addButton("确定", QMessageBox.ActionRole)
            no = msgBox.addButton("取消", QMessageBox.ActionRole)

            # 显示消息框，并等待用户做出选择
            msgBox.exec_()
            if msgBox.clickedButton() == yes:
                # 用户点击了“Custom”按钮
                self.close_window()

    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "打开文件", "./images",
                                                         "All Files(*);;Text Files(*.png)")
        # self.lineEdit.setText(filename)
        if filename != '':
            self.file_path = filename
        self.dirPath,self.file_name=os.path.split(self.file_path)
        self.listWidget_file.addItem(self.file_name)

    def save_file(self):
        # 获取文件路径

        pixmap = QPixmap(self.file_path)
        folder_path, filetype = QFileDialog.getSaveFileName(self, "文件保存", r"./save",
                                                          "All Files (*);;Text Files (*.png);;Text Files (*.jpg)")
        if pixmap.isNull():
            return
        pixmap.save(folder_path)

    def up_Image(self):
        # 效率：使用for循环搜索特定图像是否存在可能不是最有效的方法，特别是当图像列表很大时。更好的方法是使用字典，其中文件名 / 路径是键，与其相关的数据是值。

        # 代码清晰度：复杂的if - else结构使代码的意图变得模糊。建议将部分功能划分为单独的函数，使代码更加清晰和模块化。
        if self.listWidget_file.count() == 0:  # 检查是否为空
            return
        current_row = self.listWidget_file.currentRow()

        next_row = (current_row - 1) % self.listWidget_file.count()
        self.listWidget_file.setCurrentRow(next_row)

    def down_Image(self):
        if self.listWidget_file.count() == 0:  # 检查是否为空
            return
        current_row = self.listWidget_file.currentRow()

        next_row = (current_row + 1) % self.listWidget_file.count()
        self.listWidget_file.setCurrentRow(next_row)

    def print(self):
        # 创建对话框
        self.print_window = QWidget()
        self.print_window.resize(600, 400)
        self.print_window.setWindowTitle('图片打印')

        # 创建一个 QPixmap 对象并从文件中加载图像
        pixmap = QPixmap(self.file_path)

        # 使用 QLabel 显示 QPixmap
        label_image = QLabel(self.print_window)

        # 使用scaled方法来缩放图片到所需的大小
        label_image.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

        # 创建垂直布局,将标签添加到其中
        layout = QVBoxLayout()
        layout.addWidget(label_image)

        # 设置按钮
        self.print_window.settingsButton = QPushButton('打印设置', self.print_window)
        self.print_window.settingsButton.move(500, 50)
        self.print_window.settingsButton.clicked.connect(self.showSettingDialog)

        self.print_window.printButton = QPushButton('打印', self.print_window)
        self.print_window.printButton.move(500, 70)
        self.print_window.printButton.clicked.connect(self.showPrintDialog)

        # 显示对话框
        self.print_window.show()

    def showSettingDialog(self):
        printDialog = QPageSetupDialog(self.printer, self)
        printDialog.exec()

    def showPrintDialog(self):
        printdialog = QPrintDialog(self.printer, self)
        if QDialog.Accepted == printdialog.exec():
            self.editor.print(self.printer)

    def top_left(self):
        # 获取Pixmap在QLabel中的左上角坐标
        x = (self.label_pic.width() - self.scaled_pixmap.width()) // 2
        y = (self.label_pic.height() - self.scaled_pixmap.height()) // 2
        # 将QPixmap在QLabel中的坐标转换为在主窗口中的坐标
        new_point = self.label_pic.mapToParent(QtCore.QPoint(x, y))
        return new_point

    def resetImagePosition(self):
        size = self.geometry()
        # self.label_pic.move(0,0)
        # self.label_pic.resize(self.pixmap.size())
        # Pixmap的改变不会导致位置的变化：setPixmap方法改变的是label_pic的内容（即显示的图像），而不是它的位置
        # 当调整内容大小时，QLabel的左上角位置保持不变,
        # 这意味着如果图片缩小，QLabel周围可能会有额外的空间；如果图片放大，它可能会溢出其当前位置，但QLabel的左上角仍然保持在原地。
        scaled_pixmap = self.pixmap.scaled(int(0.618 * size.width()), int(0.618 * size.height()), Qt.KeepAspectRatio,
                                           Qt.SmoothTransformation)
        self.label_pic.setPixmap(scaled_pixmap)

        # 计算偏差,倍率,相对位置
        ratio = self.label_pic.scale_factor

        # 计算矩形框,文本框
        for i in range(len(self.label_pic.label_rect_List)):
            self.label_pic.label_rect_List[i][0] = self.label_pic.label_rect_List[i][0] / ratio
            self.label_pic.label_rect_List[i][1] = self.label_pic.label_rect_List[i][1] / ratio
            self.label_pic.label_rect_List[i][2] = self.label_pic.label_rect_List[i][2] / ratio
            self.label_pic.label_rect_List[i][3] = self.label_pic.label_rect_List[i][3] / ratio

        self.label_pic.update()
        self.label_pic.scale_factor = 1

    def clearRectanges(self):
        self.label_pic.label_rect_List.clear()
        self.label_pic.update()

    def loadImageNames(self):
        import os
        self.dirPath = QFileDialog.getExistingDirectory(self, "选择文件",directory='./images',options = QFileDialog.ShowDirsOnly)
        if self.dirPath:
            self.clearRectanges()
            self.listWidget_file.clear()  # currentItemChanged同时也会触发，current就会为空
            self.listWidget_label.clear()
            for file_name in os.listdir(self.dirPath):
                if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif')):
                    self.listWidget_file.addItem(file_name)

    def displayImage(self, current,precious):
        import os
        if current==None:
            return
        self.listWidget_label.clear()
        self.label_pic.selected_rect_fillColor=QRect()
        self.label_pic.scale_factor = 1
        self.file_name=current.text()
        self.file_path = os.path.join(self.dirPath, self.file_name)
        self.pixmap = QPixmap(self.file_path)
        size = self.geometry()
        self.label_pic.setPixmap(
            self.pixmap.scaled(int(0.618 * size.width()), int(0.618 * size.height()), Qt.KeepAspectRatio))

        if self.file_name in self.label_pic.imagedict:
            self.label_pic.label_rect_List = self.label_pic.imagedict[self.file_name]

            for text in self.label_pic.label_rect_List:
                item = QListWidgetItem(text[4])
                item.setCheckState(Qt.Checked)  # 设置为选中状态
                self.listWidget_label.addItem(item)
        else:
            self.label_pic.label_rect_List=[]
            self.read_xml()

        self.label_pic.update()

    def displayRect(self, item):
        self.label_pic.hovered = True
        if item.checkState() == Qt.Checked:
            data=self.label_pic.label_rect_List[self.listWidget_label.row(item)]
            self.label_pic.selected_rect_fillColor=QRectF(QPointF(data[0], data[1]), QPointF(data[2], data[3]))
            self.label_pic.update()

    def showContextMenu(self, position):
        item = self.listWidget_label.itemAt(position)
        if item:
            menu = QMenu(self.listWidget_label)

            # 添加删除操作
            delete_action = menu.addAction("Delete")
            delete_action.setShortcut('Ctrl+D')
            delete_action.triggered.connect(lambda: self.deleteItem(item))

            # 添加修改操作
            modify_action = menu.addAction("Modify")
            modify_action.setShortcut('Alt+M')
            modify_action.triggered.connect(lambda: self.modifyItem(item))

            # 显示上下文菜单
            menu.exec_(self.listWidget_label.mapToGlobal(position))

            self.label_pic.update()

    def deleteItem(self, item):
        delete_row=self.listWidget_label.row(item)
        self.listWidget_label.takeItem(delete_row)
        self.label_pic.label_rect_List.pop(delete_row)

    def modifyItem(self, item):

        # 弹出一个对话框以获得新的文本
        modify_row = self.listWidget_label.row(item)
        text, ok = QInputDialog.getText(self, 'Modify item', '修改标签:',
                                        text=item.text())
        if ok:
            item.setText(text)
        print(self.label_pic.label_rect_List)
        self.label_pic.label_rect_List[modify_row][4]=text

    def handleItemChanged(self, item):
        index=self.listWidget_label.row(item)

        data = self.label_pic.imagedict[self.file_name][index]

        if item.checkState() == Qt.Checked:  # 选中状态
            self.label_pic.label_rect_List.insert(index,data)
        if item.checkState() == Qt.Unchecked:
            self.label_pic.hovered = False
            if data in self.label_pic.label_rect_List:
                self.label_pic.label_rect_List.remove(data)

        self.label_pic.update()
    # def save_label(self):
    #     file_path, filetype = QFileDialog.getSaveFileName(self, "保存标注文件格式", r"./path_to_label_data",
    #                                                       "Text Format (*.txt);;Json Format(*.json);;XML Format(*.XML)")
    #     if file_path != '':
    #
    #         # os.path.basename(file_name 函数用于获取文件路径中的文件名部分。
    #         # os.path.splitext(file_name)函数用于将文件名拆分成文件名和文件扩展名两部分，并返回一个包含文件名和扩展名的元组。
    #         fileName, suffixName = os.path.splitext(os.path.basename(file_path))
    #         if suffixName == ".txt":
    #             self.savetoText(file_path)
    #         elif suffixName == ".csv":
    #             self.savetoCSV(file_path)
    #         elif suffixName == ".json":
    #             self.savetoJson(file_path)
    #         elif suffixName == ".XML":
    #             self.savetoXML(file_path)
    #         else:
    #             pass
    #     else:
    #         return

    def save_xml(self,image_name,path_to_label_data):
        import xml.dom.minidom

        self.resetImagePosition()

        folder=os.path.basename(self.dirPath)
        fileName, suffixName = os.path.splitext(image_name)

        xml_path = os.path.join(path_to_label_data, fileName + '.xml')  # 提取其中一部分可以给xml文件命名

        doc = xml.dom.minidom.Document()  # 在内存中创建一个空的文档
        root_node = doc.createElement('annotation')  # 创建一个根节点annotation对象
        root_node.setAttribute('object', '对象')  # 设置根节点的属性
        root_node.setAttribute('coordinate', '坐标')
        doc.appendChild(root_node)  # 将根节点添加到文档对象中

        branch_node = doc.createElement('folder')  # 创建一个分支:文件名
        branch_value = doc.createTextNode(folder)
        branch_node.appendChild(branch_value)
        root_node.appendChild(branch_node)  # 将分支添加到根节点

        branch_node = doc.createElement('filename')  # 创建一个分支:图片名
        branch_value = doc.createTextNode(self.file_name)
        branch_node.appendChild(branch_value)
        root_node.appendChild(branch_node)  # 将分支添加到根节点

        branch_node = doc.createElement('path')  # 创建一个分支:图片路径名
        branch_value = doc.createTextNode(self.file_path)
        branch_node.appendChild(branch_value)
        root_node.appendChild(branch_node)  # 将分支添加到根节点

        for node in self.label_pic.label_rect_List:
            print(node)
            branch_node = doc.createElement('object')  # 创建一个分支:矩形框
            root_node.appendChild(branch_node)  # 将分支添加到根节点

            leaf_node = doc.createElement('name')  # 创建一个叶子节点
            leaf_value = doc.createTextNode(node[4])  # 给叶子节点name设置一个文本节点，用于显示文本内容
            leaf_node.appendChild(leaf_value)
            branch_node.appendChild(leaf_node)  # 将叶子节点添加到object分支

            leaf_node_total = doc.createElement('bndbox')
            branch_node.appendChild(leaf_node_total)
            current_number = 0
            coordinate = ['xmin', 'ymin', 'xmax', 'ymax']
            while current_number < 4:
                leaf_node = doc.createElement(coordinate[current_number])
                leaf_value = doc.createTextNode(str(node[current_number]))
                leaf_node.appendChild(leaf_value)
                leaf_node_total.appendChild(leaf_node)
                current_number = current_number + 1
            with open(xml_path, "w", encoding="utf-8") as f:
                doc.writexml(f, indent='', addindent='\t', newl='\n', encoding="utf-8")
        # doc.writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式,第三个参数是其他子节点的缩进格式， 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
        # fp = open(xml_path, 'w',encoding="utf-8")
        # doc.writexml(fp, indent='', addindent='\t', newl='\n', encoding="utf-8")

    def saveXml_in_bulk(self):
        path_to_label_data=QFileDialog.getExistingDirectory(self, "选择保存路径",directory= "./path_to_label_data",options = QFileDialog.ShowDirsOnly)
        for image_name in self.label_pic.imagedict.keys():
            self.file_path=os.path.join(self.dirPath,image_name)
            self.label_pic.label_rect_List=self.label_pic.imagedict[image_name]
            self.save_xml(image_name,path_to_label_data)

    def read_xml(self):
        from xml.etree.ElementTree import Element, ElementTree

        self.listWidget_label.clear()
        path,folder=os.path.split(self.dirPath)
        fileName, suffixName = os.path.splitext(self.file_name)
        path_to_label_data=os.path.join(path,'./path_to_label_data')
        if not os.path.exists(path_to_label_data):
            return
        all_xml_file = os.listdir(path_to_label_data)
        match_xml=fileName+'.xml'
        if match_xml in all_xml_file:
            xml_path=os.path.join(path_to_label_data,match_xml)
            tree = ElementTree()
            tree.parse(xml_path)
            root_node = tree.getroot()
            branch_node = root_node.findall('object')

            for index,branch in enumerate(branch_node):
                leaf_node = branch.find('name')  # 找到打错标签的'name'

                label_name=leaf_node.text
                item = QListWidgetItem(label_name)
                item.setCheckState(Qt.Checked)  # 设置为选中状态
                self.listWidget_label.addItem(item)

                bndbox_node = branch.findall('bndbox')
                for bndbox in bndbox_node:
                    xmin=bndbox.find("xmin")
                    start_x=float(xmin.text)
                    ymin=bndbox.find("ymin")
                    start_y=float(ymin.text)
                    xmax=bndbox.find("xmax")
                    end_x=float(xmax.text)
                    ymax=bndbox.find("ymax")
                    end_y=float(ymax.text)
                    data= [start_x, start_y, end_x, end_y, label_name, index]
                    self.label_pic.label_rect_List.append(data)
            self.label_pic.imagedict[self.file_name]=self.label_pic.label_rect_List



# 防止别的脚本调用，只有自己单独运行，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app = QApplication(sys.argv)

    # 设置图标
    app.setWindowIcon(QIcon(r'./images/photo.png'))

    # 创建对象
    main = Mainwindow()

    # 创建窗口
    main.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())
