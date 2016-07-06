from __future__ import division
import os, shutil
import pickle
import threading


def check_path_exist(path):
    return True if os.path.exists(path) else False


def write_text_file(path, msg, is_first=False):
    if is_first:
        with open(path, 'w') as f:
            f.write(msg + '\n')
    else:
        with open(path, 'a') as f:
            f.write(msg + '\n')


def save_pickle_file(path, _objects):
    with open(path, 'wb') as fp:
        pickle.dump(_objects, fp)


def load_pickle_file(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)


thread_writing = None
def save_pkl_threading(path, _objects):
    global thread_writing
    if thread_writing is None:
        print 'start writing'
        thread_writing = threading.Thread(target=save_pickle_file, args=(path, _objects))
        thread_writing.daemon = True
        thread_writing.start()
    else:
        print 'waiting'
        thread_writing.join()
        print 'finish joining'
        thread_writing = None
        save_pkl_threading(path, _objects)


def get_fn_only(path):
    _, tail = os.path.split(path)
    return tail


def check_dir_create(path):
    if not os.path.exists(path):
        os.makedirs(path)


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


def remove_creat_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def get_all_files(_path, filtering_prefix, filtering_postfix):
    return [fn for fn in os.listdir(_path) if fn.startswith(filtering_prefix) and fn.endswith(filtering_postfix)]


def get_all_directories(_path):
    return [dn for dn in os.listdir(_path) if os.path.isdir('%s/%s' % (_path, dn))]

if __name__ == '__main__':
    pass
                                  
                                  
                                  
    
