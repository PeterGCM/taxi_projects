import __init__


from heapq import heappush, heappop

event_queue = []
now = 0.0
current_event = None


def push_event(t, handler, args=()):
    global now
    e = [now + t, handler, args]
    heappush(event_queue, e)
    return e


def process_events():
    global now, current_event, event_queue
    while event_queue:
        current_event = heappop(event_queue)
        evt_time, hdlr, arg = current_event
        #
        now = evt_time
        hdlr(arg)

def finish_simulation(_):
    global event_queue
    event_queue = []
