from Structure.Node import Node
from Structure.DataTree import *
from PyQt5.QtCore import *

class CmpThread(QObject):
    
    setRangeSignal : pyqtSignal = pyqtSignal(int,int)
    setValueSignal = pyqtSignal(int)

    def Cmp(self,root : Node,other : DataTree or list,parent : str = '',
           callback = None
        ) -> DataTree:
        '''
        比较两个文件夹的大小
        返回
        '''
        if isinstance(other,DataTree):
            tree2 = GetLinearTree(other.rootNode)
        elif isinstance(other,list):
            tree2 = other

        cmpNode = None

        for node in tree2:
            assert isinstance(node,Node)
            if node == root:
                tree2.remove(node)

                cmpNode = Node(root.name,(root.value,node.value),parent)

                break
        
        if cmpNode is None:
            cmpNode = Node(root.name,(root.value,-1),parent)

        assert isinstance(cmpNode,Node)

        if parent == '':
            self.setRangeSignal.emit(0,len(tree2))
            l = len(tree2)
            i = 0

        for child in root.children:
            node = self.Cmp(child,tree2,cmpNode.name)
            cmpNode.children.append(node)

            if parent == '':
                i += 1
                self.setValueSignal.emit(l - len(tree2))

                if l == len(tree2):
                    self.setRangeSignal.emit(0,0)
                    self.setValueSignal.emit(0)

        if callback is not None:
            callback(tree2,cmpNode)

        return cmpNode

def GetLinearTree(root : Node) -> list:
    '''
    获取树的线性表
    '''
    tree = []

    def Get(node : Node):
        tree.append(node)

        for child in node.children:
            Get(child)

    Get(root)

    return tree