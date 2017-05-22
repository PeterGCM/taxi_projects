import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
import community_analysis
#
import wx
app = wx.App(False)
#
MAX_FRAME_RATE = 30  # 30 refreshes per second (SHOULD be integer)
SPEED_BASE = 2**0.5
TIMER_INTERVAL = 1000 // MAX_FRAME_RATE  # milliseconds
SCENE_REFRESH_CYCLES = [1, 2, 3, 5, 6, 10, 15, 30]
DEVICE_DRAW_FONT = wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
DEFAULT_FONT = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
BIG_BOLD_FONT = wx.Font(24, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD)