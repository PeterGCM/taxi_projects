from __init__ import *
import timeKeeper as tk
#
from datetime import datetime


class TimeFlowView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)
        self.slider_index = tk.datehours.index(datetime(tk.now.year, tk.now.month, tk.now.day, tk.now.hour))
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        #
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st_fdt = wx.StaticText(self,
                               label='%d/%02d/%02d' % (
                                   tk.min_dt.year, tk.min_dt.month, tk.min_dt.day),
                               style=wx.ALIGN_CENTER)
        st_fdt.SetFont(DEFAULT_FONT)
        hbox.Add(st_fdt, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=10)
        self.sld = wx.Slider(self,
                             value=self.slider_index,
                             minValue=0,
                             maxValue=len(tk.datehours),
                             style=wx.SL_HORIZONTAL)
        hbox.Add(self.sld, 10, wx.EXPAND, border=10)
        st_ldt = wx.StaticText(self,
                               label='%d/%02d/%02d' % (
                                   tk.max_dt.year, tk.max_dt.month, tk.max_dt.day),
                               style=wx.ALIGN_CENTER)
        st_ldt.SetFont(DEFAULT_FONT)
        hbox.Add(st_ldt, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=10)
        vbox.Add(hbox, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP)
        self.st_cur_datehour = wx.StaticText(self,
                                             label='%d/%02d/%02d:H%02d' % tk.get_datehour(),
                                             style=wx.ALIGN_CENTER)
        self.st_cur_datehour.SetFont(BIG_BOLD_FONT)
        vbox.Add(self.st_cur_datehour, 1, wx.ALIGN_CENTRE_HORIZONTAL)
        self.SetSizer(vbox)
        #
        self.sld.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

    def OnSliderScroll(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()
        chosen_dt = tk.datehours[val]
        self.st_cur_datehour.SetLabel('%d/%02d/%02d:H%02d' % (
            chosen_dt.year, chosen_dt.month, chosen_dt.day, chosen_dt.hour))

    def update_datehour(self):
        new_index = tk.datehours.index(datetime(tk.now.year, tk.now.month, tk.now.day, tk.now.hour))
        if 0 < new_index < len(tk.datehours):
            chosen_dt = tk.datehours[new_index]
            self.st_cur_datehour.SetLabel('%d/%02d/%02d:H%02d' % (
                chosen_dt.year, chosen_dt.month, chosen_dt.day, chosen_dt.hour))
            self.sld.SetValue(new_index)
            self.slider_index = new_index








