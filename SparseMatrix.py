class SparseMatrix(object):
    """Emulates a sparse matrix. almost verbatim from the work of
       Abd Allah Diab (mpcabd, http://magicpc.wordpress.com)"""
    def __init__(self):
        self.dict = {}
    
    def __getitem__(self, index):
        if index in self.dict.keys():
            return self.dict[index]
        else:
            return 0

    def __setitem__(self, index, value):
        self.dict[index] = value
