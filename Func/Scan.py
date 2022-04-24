from typing import Tuple
from Structure.Node import Node
import os
from PyQt5.QtCore import *

class ScanThread(QObject):

    setRangeSignal : pyqtSignal = pyqtSignal(int,int)
    setValueSignal = pyqtSignal(int)

    def Scan(self,path : str,parent : str = None,callback = None) -> Tuple[int,Node]:
        '''
        扫描文件(夹)大小
        返回
        '''
        size = 0
        node = Node(path,size,parent)

        isRoot = parent is None

        try:
            if os.path.isfile(path):
                size = os.path.getsize(path)

            elif os.path.isdir(path):

                if isRoot:
                    self.setRangeSignal.emit(0,len(os.listdir(path)))
                    i = 0

                for file in os.listdir(path):
                    s,n = self.Scan(path + '/' + file,path)

                    size += s
                    
                    node.children.append(n)

                    if isRoot:
                        i += 1
                        self.setValueSignal.emit(i)

        except PermissionError as e:
            # TODO: 将权限错误记录到日志
            pass

        node.value = size

        if callback is not None:
            callback(size,node)

        return size,node