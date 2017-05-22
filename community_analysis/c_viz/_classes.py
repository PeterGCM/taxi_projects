import __init__
#
from log_xyCoords import get_driver_trajectory

import wx
#
# VEHICLE_STATE_COLARS = [wx.Brush(wx.Colour(200, 200, 200)),
#                 wx.Brush(wx.Colour(225, 225, 225)),
#                 wx.Brush(wx.Colour(0, 0, 255)),
#                 wx.Brush(wx.Colour(255, 193, 193)),
#                 wx.Brush(wx.Colour(0, 255, 0)),
#                 wx.Brush(wx.Colour(255, 255, 0))]

class driver(object):
    def __init__(self, did):
        self.did = did
        self.dt_xy_state = get_driver_trajectory(did)
        dt, x, y, state = self.dt_xy_state.pop(0)
        self.prev_update_time = dt
        self.prev_x, self.prev_y = self.x, self.y = x, y
        self.state = state
        #
        self.next_update_time = self.dt_xy_state[0][0]
        self.next_x, self.next_y = self.dt_xy_state[0][1:3]
        #
        self.time_interval = (self.next_update_time - self.prev_update_time).seconds

    def update_trajectory(self, cur_dt):
        if self.next_update_time <= cur_dt:
            dt, x, y, state = self.dt_xy_state.pop(0)
            self.prev_update_time = dt
            self.prev_x, self.prev_y = self.x, self.y = x, y
            self.state = state
            #
            self.next_update_time = self.dt_xy_state[0][0]
            self.next_x, self.next_y = self.dt_xy_state[0][1:3]
            #
            self.time_interval = (self.next_update_time - self.prev_update_time).seconds
        else:
            td = cur_dt - self.prev_update_time
            time_passed = td.seconds + td.microseconds / float(1e6)
            ratio = time_passed / float(self.time_interval)
            self.x = self.prev_x + (self.next_x - self.prev_x) * ratio
            self.y = self.prev_y + (self.next_y - self.prev_y) * ratio

    def draw(self, gc):
        old_tr = gc.GetTransform()
        gc.Translate(self.x, self.y)
        #
        gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
        gc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))

        gc.DrawEllipse(-3, -3, 6, 6)

        gc.SetTransform(old_tr)

    def update_dt_xy_state(self, given_dt):
        while True:
            dt, x, y, state = self.dt_xy_state[0]
            if given_dt < dt:
                break
            else:
                dt, x, y, state = self.dt_xy_state.pop(0)
                self.prev_update_time = dt
                self.prev_x, self.prev_y = self.x, self.y = x, y
                self.state = state
                #
                self.next_update_time = self.dt_xy_state[0][0]
                self.next_x, self.next_y = self.dt_xy_state[0][1:3]
                #
                self.time_interval = (self.next_update_time - self.prev_update_time).seconds


if __name__ == '__main__':
    # v1 = subVec((3, 4), (0,0))
    # print v1
    # print norm(v1)
    # print calc_unitVec(v1)
    # po = (0, 0)
    # print calc_point(po, v1, 5)
    from datetime import timedelta
    d = timedelta(microseconds=1e6 - 1)
    print d.seconds
    print d.microseconds
    d = timedelta(microseconds=1e6 + 1)
    print d.seconds
    print d.microseconds
    # x0, y0 = 858.383357837, 3203.03291399
    # x1, y1 = 858.373909804, 3203.03791589
    # x2, y2 = 858.364465312, 3203.04291592
    # v0 = subVec((x1, y1), (x0, y0))
    # v1 = subVec((x2, y2), (x1, y1))
    # print v0
    # print v1





