from __init__ import *
#
from viz_cmd import set_command_interface
from viz_cmd import ID_CONTROL_S_UP
from _classes import driver
import timeKeeper as tk
from trajectoryView import TrajectoryView
from timeFlowView import TimeFlowView
#
from time import time
from datetime import timedelta, datetime
#
target_drivers = [
                    1,
                  32768
                  ]
#


class MainFrame(wx.Frame):
    def __init__(self, title="DriverTrajectory", pos=(30, 30), size=(1600, 1100)):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        # simulation speed and refresh setting
        self.is_paused = True
        self.speed_factor, self.scene_refresh_factor = 14, 30
        self.tx = SPEED_BASE ** self.speed_factor
        #
        self.InitTimeDrivers()
        self.InitUI()
        self.Show(True)
        self.Centre()
        self.Maximize()
        #
        # self.tj_view.InitUI()
        # self.tf_view.InitUI()
        # create timer.
        self.timer, self.timer_tick = wx.Timer(self), 0
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

    def InitTimeDrivers(self):
        self.drivers = {}
        latest_fist_dt, earliest_last_dt = None, None
        for did in target_drivers:
            d = driver(did)
            first_dt, last_dt = d.prev_update_time, d.dt_xy_state[-1][0]
            if latest_fist_dt == None or latest_fist_dt < first_dt:
                latest_fist_dt = first_dt
            if earliest_last_dt == None or earliest_last_dt > last_dt:
                earliest_last_dt = last_dt
            self.drivers[did] = d
        tk.min_dt, tk.max_dt = latest_fist_dt, earliest_last_dt
        tk.now = tk.min_dt
        tk.datehours = set()
        for d in self.drivers.itervalues():
            d.update_dt_xy_state(tk.now)
            for dt, _, _, _ in d.dt_xy_state:
                tk.datehours.add(datetime(dt.year, dt.month, dt.day, dt.hour))
        tk.datehours = list(tk.datehours)
        tk.datehours.sort()


    def InitUI(self):
        # set menu & tool bar, and bind events.
        set_command_interface(self)
        #
        basePanel = wx.Panel(self)
        #
        vbox = wx.BoxSizer(wx.VERTICAL)
        #
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        h1 = wx.Panel(basePanel)
        self.tj_view = TrajectoryView(h1, self.drivers)
        hbox.Add(self.tj_view, 9, wx.EXPAND | wx.ALL)
        p = wx.Panel(h1)
        p.SetBackgroundColour('#4f5049')
        hbox.Add(p, 3, wx.EXPAND | wx.ALL)
        h1.SetSizer(hbox)
        #
        vbox.Add(h1, 9, wx.EXPAND | wx.ALL)
        self.tf_view = TimeFlowView(basePanel)
        vbox.Add(self.tf_view, 1, wx.EXPAND | wx.ALL)
        basePanel.SetSizer(vbox)
        #
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(basePanel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(vbox)

    def OnClose(self, _e):
        self.timer.Stop()
        self.DestroyChildren()
        self.Destroy()

    def OnExit(self, _e):
        self.Close()

    def OnTimer(self, _e):
        # if self.timer_tick == 0:
        #     self.tj_view.gen_bg_img()
        self.timer_tick += 1
        #
        tk.now += timedelta(seconds=SPEED_BASE ** self.speed_factor / float(MAX_FRAME_RATE))
        #
        self.refresh_scene()

    def OnPlay(self, _e=None):
        if self.is_paused:
            self.timer.Start(TIMER_INTERVAL)
            self.is_paused = False
            # timing related
            self.last_clock_on_refresh, self.last_time_on_refresh = tk.now, time()
        else:
            self.timer.Stop()
            self.is_paused = True

    def OnSpeed(self, e, up=None):
        self.speed_factor += (1 if (e != None and e.GetId() == ID_CONTROL_S_UP) or up else -1)
        self.tx = SPEED_BASE ** self.speed_factor
        #
        self.refresh_scene(False)

    def OnSkip(self, _e=None):
        pass

    def OnFrameRate(self, _e=None):
        pass

    def OnFrameRate(self, _e=None):
        pass

    def refresh_scene(self, update_animate_state=True):
        self.tj_view.update(update_animate_state)
        self.tf_view.update_datehour()


if __name__ == '__main__':
    MainFrame()
    app.MainLoop()