import __init__
#
from taxi_common.geo_functions import get_SG_polygon, get_SG_roads
from taxi_common.file_handling_functions import check_path_exist, load_pickle_file, save_pickle_file
#
import wx
#
app = wx.App(False)
#


class MainFrame(wx.Frame):
    def __init__(self, title="DriverTrajectory", pos=(30, 30), size=(1600, 1100)):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        #
        self.InitUI()
        self.Centre()
        self.Maximize()
        #
        self.Show(True)
        for p in self.basePanel.GetChildren():
            if type(p) == TrajectoryView:
                p.InitUI()

    def InitUI(self):
        self.basePanel = wx.Panel(self)
        self.basePanel.SetBackgroundColour('#4f5049')
        #
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(TrajectoryView(self.basePanel), 9, wx.EXPAND | wx.ALL)
        vbox.Add(wx.Panel(self.basePanel), 1, wx.EXPAND | wx.ALL)
        self.basePanel.SetSizer(vbox)
        #
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.basePanel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(vbox)

def convert_drawing_coords(lon, lat, min_max_info, scale):
    min_lon, max_lon, min_lat, max_lat = min_max_info
    x = (lon - min_lon) * scale
    y = (max_lat - (lat - min_lat)) * scale
    return x, y

class TrajectoryView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)

    def InitUI(self):
        self.SetDoubleBuffered(True)
        print 'size', self.GetSize()
        sg_border = get_SG_polygon()
        self.scale = 2500
        self.sg_border_fd = []
        min_lon, max_lon = 1e400, -1e400
        min_lat, max_lat = 1e400, -1e400
        for lon, lat in sg_border:
            if lon < min_lon:
                min_lon = lon
            if lon > max_lon:
                max_lon = lon
            if lat < min_lat:
                min_lat = lat
            if lat > max_lat:
                max_lat = lat
        min_max_info = (min_lon, max_lon, min_lat, max_lat)
        min_x, min_y = 1e400, 1e400
        for lon, lat in sg_border:
            x, y = convert_drawing_coords(lon, lat, min_max_info, self.scale)
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            self.sg_border_fd += [(x, y)]

        self.translate_x, self.translate_y = -min_x, -min_y

        self.roads_fd = None
        ofpath = 'roads_fd.pkl'
        if check_path_exist(ofpath):
            self.roads_fd = load_pickle_file(ofpath)
        else:
            self.roads_fd = []
            for _, coords in get_SG_roads():
                road_fd = []
                for lon, lat in coords:
                    road_fd += [convert_drawing_coords(lon, lat, min_max_info, self.scale)]
                self.roads_fd += [road_fd]
            save_pickle_file(ofpath, self.roads_fd)
        #
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # prepare stock objects.
        self.default_pen = self.create_pen(wx.BLACK, 1)
        self.default_font = self.create_font(8, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.gpath = None

    def create_pen(self, color, width):
        return wx.Pen(color, width)

    def create_font(self, size, family, style, weight):
        return wx.Font(size, family, style, weight)

    def OnPaint(self, _):
        # prepare.
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen(self.default_pen)
        gc.SetFont(self.default_font, wx.BLACK)
        # draw on logical space.
        oldTransform = gc.GetTransform()
        gc.Translate(self.translate_x, self.translate_y)
        # gc.Scale(self.scale, self.scale)
        self.OnDraw(gc)
        gc.SetTransform(oldTransform)

    def create_gpath(self, gc):
        gpath = gc.CreatePath()
        for r_coords in self.roads_fd:
            gpath.MoveToPoint(r_coords[0])
            for i in range(1, len(r_coords)):
                gpath.AddLineToPoint(r_coords[i])
        return gpath


    def OnDraw(self, gc):
        gc.DrawLines(self.sg_border_fd)
        # if not self.gpath:
        #     self.gpath = self.create_gpath(gc)
        # gc.DrawPath(self.gpath)





if __name__ == '__main__':
    MainFrame()
    app.MainLoop()