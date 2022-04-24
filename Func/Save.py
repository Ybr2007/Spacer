from Structure.DataTree import DataTree
import pickle

def Save(dataTree : DataTree,path : str) -> bool:
    '''
    保存数据
    '''
    try:
        with open(path,'wb') as f:
            pickle.dump(dataTree,f)
        return True
    except Exception as e:
        return False