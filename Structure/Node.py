class Node:
    '''
    保存占用空间和路径的树节点
    '''
    def __init__(self,name,value,parent = None):
        '''
        初始化
        '''
        self.name = name
        self.value = value
        self.parent = parent
        self.children = []

    def __eq__(self, __o: object) -> bool:
        '''
        比较两个节点是否相等
        '''
        if isinstance(__o,Node):
            return self.name == __o.name
        else:
            return False