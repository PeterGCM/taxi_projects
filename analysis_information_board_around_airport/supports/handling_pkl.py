from __future__ import division
import pickle

def save_pickle_file(path, _objects):
    with open(path, 'wb') as fp:
        pickle.dump(_objects, fp)
        
def load_picle_file(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)
    
    