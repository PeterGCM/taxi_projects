#
from datetime import timedelta, datetime
from time import time

import pandas as pd
import timeKeeper as tk
from timeFlowView import TimeFlowView
from trajectoryView import TrajectoryView

from __init__ import *
from _classes import driver
#
from community_analysis import AM10, PM8
from community_analysis import dpaths, prefixs
#
from taxi_common.sg_grid_zone import get_sg_zones
from viz_cmd import ID_CONTROL_S_UP
from viz_cmd import set_command_interface
#
# followers = [1]
# leaders = [32768]


# followers = [18485]
# negLeaders = [35005]
# posLeaders = [34512]


# followers = [21340]
# negLeaders = []
# posLeaders = [17742]

followers = []
a = set([20318, 15078, 35650, 3413, 13851, 37446, 35685, 33796])
b = set([40970, 35716, 30309, 22412, 17695, 17637, 16606, 14969, 12887, 3413])
leaders = list(a.union(b))

target_drivers = followers + leaders
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
        self.InitEncounterMoments()
        self.InitUI()
        self.Show(True)
        self.Centre()
        self.Maximize()
        #
        # create timer.
        self.timer, self.timer_tick = wx.Timer(self), 0
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

    def InitTimeDrivers(self):
        self.drivers = {}
        latest_fist_dt, earliest_last_dt = None, None
        for did in target_drivers:
            d = driver(did)
            first_dt, last_dt = d.dt_xy_state[0][0], d.dt_xy_state[-1][0]
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
        #
        self.zones = get_sg_zones()

    def InitEncounterMoments(self):
        if_dpath = dpaths['roamingTime', 'priorPresence']
        if_prefix = prefixs['roamingTime', 'priorPresence']
        year = 2009
        self.ecounterMoments = []
        ecounterMoments = set()
        loc = {}
        for did1 in target_drivers:
            fpath = '%s/%s%d-%d.csv' % (if_dpath, if_prefix, year, did1)
            df = pd.read_csv(fpath)
            for did0 in target_drivers:
                if did1 == did0:
                    continue
                _did0 = '%d' % did0
                if _did0 not in df.columns:
                    continue
                for m, d, h, zi, zj in df[(df[_did0] == 1)][['month', 'day', 'hour', 'zi', 'zj']].values:
                    dt = datetime(year, m, d, h)
                    ecounterMoments.add(datetime(year, m, d, h))
                    loc[dt] = (zi, zj)
        for dt in ecounterMoments:
            self.ecounterMoments += [(dt, loc[dt])]


        for did1 in followers:
            fpath = '%s/%s%d-%d.csv' % (if_dpath, if_prefix, year, did1)
            df = pd.read_csv(fpath)
            for did0 in leaders:
                _did0 = '%d' % did0
                for m, d, h, zi, zj in df[(df[_did0] == 1)][['month', 'day', 'hour', 'zi', 'zj']].values:
                    self.ecounterMoments += [(datetime(year, m, d, h), (zi, zj))]
        self.ecounterMoments.sort()

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
        self.timer_tick += 1
        #
        tk.now += timedelta(seconds=SPEED_BASE ** self.speed_factor / float(MAX_FRAME_RATE))
        if datetime(*tk.get_datehour()) not in tk.datehours:
            tk.now = tk.datehours[self.tf_view.slider_index + 1]
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
        i = 0
        while True:
            dt, (zi, zj) = self.ecounterMoments[i]
            dt_before30 = dt - timedelta(minutes=30)
            if tk.now < dt_before30:
                if dt_before30.hour < AM10 or PM8 <= dt_before30.hour:
                    tk.now = dt
                else:
                    tk.now = dt_before30
                self.tj_view.mark_zone(zi, zj)
                for d in self.drivers.itervalues():
                    d.update_dt_xy_state(tk.now)
                break
            i += 1

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