from Structure.Node import Node
import Info
import time

class DataTree:
    '''
    用于保存储存扫描的数据
    '''
    rootNode : Node # 树的根节点

    rootPath : str # 根目录路径

    rootSize : int # 根目录大小

    scanTime : str # 扫描时间

    verision : str # 扫描时的版本

    def __init__(self,rootNode : Node):
        '''
        初始化
        '''
        self.rootNode = rootNode
        self.rootPath = rootNode.name
        self.rootSize = rootNode.value
        self.scanTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.verision = Info.verision

    @staticmethod
    def Load(data):
        '''
        加载数据
        '''
        result = DataTree(
            data['rootNode']
        )
        result.scanTime = data['scanTime']
        result.verision = data['verision']
        
        return result
