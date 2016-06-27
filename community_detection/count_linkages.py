from __init__ import get_relation_fn
from __init__ import MEMORY_MANAGE_INTERVAL, COINCIDENCE_THRESHOLD_VALUE
from __init__ import POB
from __init__ import out_boundary_logs_fn
#
from classes import cd_driver   
#
from taxi_common.file_handling_functions import save_pickle_file #@UnresolvedImport
#
import csv

def run(processed_log_fn, zones):
    out_boundary_logs_num = 0
    with open(out_boundary_logs_fn, 'w') as f:
        f.write('time,did,i,j,state,zone_defined' + '\n')
    #
    drivers = {}
    with open(processed_log_fn, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        # {'i': 1, 'did': 3, 'state': 4, 'j': 2, 'time': 0}
        hid = {h : i for i, h in enumerate(headers)}
        memory_manage_clock = -1e400
        for row in reader:
            t = eval(row[hid['time']])
            did = row[hid['did']]
            i, j = int(row[hid['i']]), int(row[hid['j']])
            #
            # Find a targeted zone
            #
            try:
                z = zones[(i, j)]
                #
                try:
                    assert z.check_validation()
                except AssertionError:
                    out_boundary_logs_num += 1
                    with open(out_boundary_logs_fn, 'a') as f:
                        f.write('%d,%s,%d,%d,%d,O' % (t, did, i, j, state) + '\n')
                    continue
            except KeyError:
                out_boundary_logs_num += 1
                with open(out_boundary_logs_fn, 'a') as f:
                    f.write('%d,%s,%d,%d,%d,X' % (t, did, i, j, state) + '\n')
                continue
            #
            if not drivers.has_key(did): drivers[did] = cd_driver(did)
            d = drivers[did]
            if state == POB:
                d.update_relation(t, z)
            else:
                d.update_position(t, z)
            if t - memory_manage_clock > MEMORY_MANAGE_INTERVAL:
                #
                # Remove low possibility relations
                #
                for d in drivers.itervalues():
                    for d1, num in d.relation.iteritems():
                        if num < COINCIDENCE_THRESHOLD_VALUE:
                            d.relation.pop(d1)
                memory_manage_clock = t
    did_relations = [(did, d.relation) for did, d in drivers.iteritems()]
    save_pickle_file(get_relation_fn(processed_log_fn), did_relations)
    return did_relations
    
    return
    
    