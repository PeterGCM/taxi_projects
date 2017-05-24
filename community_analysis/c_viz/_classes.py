from __init__ import *
#
from log_xyCoords import get_driver_trajectory

import wx
#
VEHICLE_STATE_COLARS = [
            wx.Brush(wx.Colour(200, 200, 200)),
            wx.Brush(wx.Colour(225, 225, 225)),
            wx.Brush(wx.Colour(0, 0, 255)),
            wx.Brush(wx.Colour(255, 193, 193)),
            wx.Brush(wx.Colour(0, 255, 0)),
            wx.Brush(wx.Colour(255, 255, 0))]

ST_FREE, ST_POB = 0, 5
COL_FREE = wx.Brush(wx.Colour(0, 255, 0))
COL_POB = wx.Brush(wx.Colour(255, 0, 0))
COL_ETC = wx.Brush(wx.Colour(0, 0, 255))
VEH_SIZE = 5


class driver(object):
    def __init__(self, did):
        self.did = did
        self.dt_xy_state = get_driver_trajectory(did)
        #
        self.prev_update_time = None
        self.prev_x, self.prev_y = None, None
        self.state = None
        #
        self.next_update_time = None
        self.next_x, self.next_y = None, None
        #
        self.time_interval = None
        #
        self.size = VEH_SIZE

    def __repr__(self):
        return 'did %d' % self.did

    def update_processing_log(self):
        dt, x, y, state = self.dt_xy_state.pop(0)
        self.prev_update_time = dt
        self.prev_x, self.prev_y = self.x, self.y = x, y
        self.state = state
        #
        self.next_update_time = self.dt_xy_state[0][0]
        self.next_x, self.next_y = self.dt_xy_state[0][1:3]
        #
        self.time_interval = (self.next_update_time - self.prev_update_time).seconds
        if self.time_interval == 0:
            self.update_processing_log()


    def update_trajectory(self, cur_dt):
        if self.next_update_time <= cur_dt:
            self.update_processing_log()
        else:
            td = cur_dt - self.prev_update_time
            time_passed = td.seconds + td.microseconds / float(1e6)
            ratio = time_passed / float(self.time_interval)
            self.x = self.prev_x + (self.next_x - self.prev_x) * ratio
            self.y = self.prev_y + (self.next_y - self.prev_y) * ratio

    def update_dt_xy_state(self, given_dt):
        if self.prev_update_time == None:
            self.update_processing_log()
        while True:
            if self.prev_update_time <= given_dt and given_dt < self.next_update_time:
                break
            self.update_processing_log()
        if self.prev_update_time != given_dt:
            self.update_processing_log()

    def draw(self, gc):
        old_tr = gc.GetTransform()
        gc.Translate(self.x, self.y)
        #
        gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
        state, col = None, None
        if self.state == ST_FREE:
            col = COL_FREE
            state = 'FREE'
        elif self.state == ST_POB:
            col = COL_POB
            state = 'POB'
        else:
            col = COL_ETC
            state = 'ETC'
        gc.SetBrush(col)
        gc.DrawEllipse(-self.size / 2.0, -self.size / 2.0,
                       self.size, self.size)
        #
        gc.DrawLines([(0, 0), (self.size / 2.0, self.size * 1.5)])
        gc.SetFont(DEFAULT_FONT)
        gc.DrawText('%s(%s)' % (self.did, state), self.size / 2.0, self.size * 1.5)


        gc.SetTransform(old_tr)


if __name__ == '__main__':
    print driver(32768).dt_xy_state





