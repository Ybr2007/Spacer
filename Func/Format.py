def BitFormat(bit : int,mode = 'Auto') -> str:  
    if mode == 'Auto':
        if abs(bit) < 1024:
            return str(bit) + ' B'
        elif abs(bit) < 1024 ** 2:
            return str(bit / 1024) + ' KB'
        elif abs(bit) < 1024 ** 3:
            return str(bit / 1024 ** 2) + ' MB'
        else:
            return str(bit / 1024 ** 3) + ' GB'
    elif mode == 'B':
        return str(bit) + ' B'
    elif mode == 'KB':
        return str(bit / 1024) + ' KB'
    elif mode == 'MB':
        return str(bit / 1024 ** 2) + ' MB'
    elif mode == 'GB':
        return str(bit / 1024 ** 3) + ' GB'
    
    return str(bit) + ' B'