from Structure.DataTree import DataTree
import pickle

def Load(path : str) -> DataTree:
    '''
    加载数据
    '''
    try:
        with open(path,'rb') as f:
            dataTree = pickle.load(f)
        return dataTree
    except BaseException as e:
        return None