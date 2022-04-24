from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Structure.Node import Node
from Structure.DataTree import DataTree

from Func.Scan import ScanThread
from Func.Cmp import CmpThread,GetLinearTree
from Func.Format import BitFormat
from Func.Save import Save
from Func.Load import Load

import threading
from Info import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化窗口
        self.initWin()

        # 初始化UI
        self.initUI()

        # 数据
        self.dataTree = None
        self.showMode = 'Auto'

        self.ScanThread = ScanThread()
        self.ScanThread.setRangeSignal.connect(self.SetPropgressBarRange)
        self.ScanThread.setValueSignal.connect(self.SetProgressBarValue)
        self.CmpThread = CmpThread()
        self.CmpThread.setRangeSignal.connect(self.SetPropgressBarRange)
        self.CmpThread.setValueSignal.connect(self.SetProgressBarValue)

    def initWin(self):  
        # 设置窗口标题
        title = 'Spacer' + ' ' + verision + ' By: ' + author
        self.setWindowTitle(title)

        # 设置窗口大小
        self.resize(1600,1200)

        # 设置窗口图标
        self.setWindowIcon(QIcon('./Asset/Icon.png'))

    def initUI(self):
        # 储存扫描按钮
        self.scanButton = QPushButton('储存扫描',self)
        self.scanButton.setGeometry(QRect(100,100,100,30))
        self.scanButton.clicked.connect(self.Scan)

        # 保存扫描结果
        self.saveButton = QPushButton('保存结果',self)
        self.saveButton.setGeometry(QRect(300,100,100,30))
        self.saveButton.clicked.connect(self.Save)

        # 加载扫描数据
        self.loadButton = QPushButton('加载数据',self)
        self.loadButton.setGeometry(QRect(500,100,100,30))
        self.loadButton.clicked.connect(self.Load)

        # 对比按钮
        self.compareButton = QPushButton('对比',self)
        self.compareButton.setGeometry(QRect(700,100,100,30))
        self.compareButton.clicked.connect(self.Cmp)

        # 获取信息
        self.infoButton = QPushButton('信息',self)  
        self.infoButton.setGeometry(QRect(900,100,100,30))
        self.infoButton.clicked.connect(self.Info)

        # 按钮组
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.scanButton)
        self.buttonGroup.addButton(self.saveButton)
        self.buttonGroup.addButton(self.loadButton)
        self.buttonGroup.addButton(self.compareButton)
        self.buttonGroup.addButton(self.infoButton)
        
        # 储存树
        self.tree = QTreeWidget(self)
        self.tree.setGeometry(QRect(100,200,1400,800))
        self.tree.setHeaderLabels(['文件名','大小'])
        self.tree.setColumnWidth(0,1000)
        self.tree.setColumnWidth(1,100)

        #进度条
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(QRect(100,150,1400,30))
        #self.progressBar.setRange(0,0)
        self.progressBar.setValue(0)

    def __BuildScanTree(self,node : Node,parent):
        item = QTreeWidgetItem(parent,[node.name,BitFormat(node.value)])

        for child in node.children:
            self.__BuildScanTree(child,item)

    def SetScanTree(self,_,root):
        self.dataTree = DataTree(root)

        self.tree.clear()

        # 将所有按钮设置为可用
        for button in self.buttonGroup.buttons():
            button.setEnabled(True)

        self.__BuildScanTree(self.dataTree.rootNode,self.tree)

    def SetCmpTree(self,newNodes,root):
        self.tree.clear()

        self.__BuildCmpTree(root,self.tree)

        for node in newNodes:
            item = QTreeWidgetItem(self.tree,[node.name,'New:' + BitFormat(node.value)])
            item.setForeground(1,QBrush(QColor(255,0,0)))

        for button in self.buttonGroup.buttons():
            button.setEnabled(True)

    def __BuildCmpTree(self,node : Node,parent):
        if node.value[1] != -1:
            item = QTreeWidgetItem(parent,[node.name,BitFormat(node.value[0]) + '->' 
            + BitFormat(node.value[1])])
            if node.value[0] < node.value[1]:
                item.setForeground(1,QBrush(QColor(255,0,0)))
            elif node.value[0] > node.value[1]:
                item.setForeground(1,QBrush(QColor(0,255,0)))
        else:
            item = QTreeWidgetItem(parent,[node.name,BitFormat(node.value[0]) + '->'
            'Not Found'])
            item.setForeground(1,QBrush(QColor(0,255,0)))

        for child in node.children:
            self.__BuildCmpTree(child,item)

    def SetPropgressBarRange(self,min,max):
        self.progressBar.setRange(min,max)

    def SetProgressBarValue(self,value):
        self.progressBar.setValue(value)

    def Scan(self):
        path = QFileDialog.getExistingDirectory(self,'选择文件夹')

        if not path:
            return

        # 将所有按钮设置为不可用
        for button in self.buttonGroup.buttons():
            button.setEnabled(False)

        t = threading.Thread(target=self.ScanThread.Scan,args=(path,None,self.SetScanTree))
        t.setName('Scaning the path:' + path)
        t.start()

    def Save(self):
        path = QFileDialog.getSaveFileName(self,'保存文件','','*.ysd')[0]

        if not path:
            return

        if not path.endswith('.ysd'):
            path += '.ysd'

        if not Save(self.dataTree,path):
            QMessageBox.warning(self,'错误','保存失败')

    def Load(self):
        path = QFileDialog.getOpenFileName(self,'打开文件','','*.ysd')[0]

        if not path:
            return

        if not path.endswith('.ysd'):
            path += '.ysd'

        tree = Load(path)

        if not tree:
            QMessageBox.warning(self,'错误','加载失败')
            return

        self.dataTree = tree

        self.tree.clear()

        self.__BuildScanTree(self.dataTree.rootNode,self.tree)

    def Cmp(self):
        path = QFileDialog.getOpenFileName(self,'打开文件','','*.ysd')[0]

        if not path:
            return

        if not path.endswith('.ysd'):
            path += '.ysd'

        tree = Load(path)

        if not tree:
            QMessageBox.warning(self,'错误','加载失败')
            return

        for button in self.buttonGroup.buttons():
            button.setEnabled(False)

        t = threading.Thread(target=self.CmpThread.Cmp,args=(self.dataTree.rootNode,tree,'',self.SetCmpTree))
        t.setName('Cmp the path:' + path)
        t.start()

    def Info(self):
        if self.dataTree:
            QMessageBox.information(self,'信息','扫描时间:' + self.dataTree.scanTime + '\n'
            + '文件数量:' + str(len(GetLinearTree(self.dataTree.rootNode))) + '\n'
            + '占用空间:' + BitFormat(self.dataTree.rootSize) + '\n'
            + '根目录' + self.dataTree.rootPath + '\n'
            + '扫描版本:' + self.dataTree.verision)
