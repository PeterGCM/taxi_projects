from __future__ import division
import os, shutil
import datetime
import pickle
#
def write_text_file(path, msg, is_first=False):
    if is_first:
        with open(path, 'w') as f:
            f.write(msg + '\n')
    else:
        with open(path, 'a') as f:
            f.write(msg + '\n')
#
def save_pickle_file(path, _objects):
    with open(path, 'wb') as fp:
        pickle.dump(_objects, fp)
        
def load_picle_file(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)
    
def check_dir_create(path):
    if not os.path.exists(path):
        os.makedirs(path)
    
def remove_creat_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    
def get_all_files(_path, filtering_prefix, filtering_postfix):
    return [fn for fn in os.listdir(_path) if fn.startswith(filtering_prefix) and fn.endswith(filtering_postfix)]

def get_all_directories(_path):
    return [dn for dn in os.listdir(_path) if os.path.isdir('%s/%s' % (_path, dn))]

def get_date(_timestamp):
    return datetime.datetime.fromtimestamp(_timestamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    print get_date(1231119063)
                                  
                                  
                                  
    
