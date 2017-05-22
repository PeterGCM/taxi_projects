from __init__ import *
#
import GPS_xyCoords_converter as GPS_xyDrawing
import timeKeeper as tk
#
from taxi_common.file_handling_functions import check_path_exist
#
import wx

bg_img_fpath = 'bg_img.png'



class TrajectoryView(wx.Panel):
    def __init__(self, parent, drivers):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        #
        self.main_frame = self.Parent.Parent.Parent
        self.drivers = drivers
        self.InitUI()

    def InitUI(self):
        self.SetDoubleBuffered(True)
        #
        self.sgBorder_xy = GPS_xyDrawing.get_sgBoarder_xy()
        min_x, min_y = 1e400, 1e400
        for x, y in self.sgBorder_xy:
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
        self.translate_x, self.translate_y = -min_x + 10, -min_y + 10
        #
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # prepare stock objects.
        self.default_pen = self.create_pen(wx.BLACK, 1)
        self.default_font = self.create_font(8, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        if check_path_exist(bg_img_fpath):
            bmp = wx.BitmapFromImage(wx.Image(bg_img_fpath).AdjustChannels(1.0, 1.0, 1.0, 0.5))
            self.bg_bmp = (bmp, bmp.GetWidth(), bmp.GetHeight())
        else:
            self.bg_bmp = None

    def create_pen(self, color, width):
        return wx.Pen(color, width)

    def create_font(self, size, family, style, weight):
        return wx.Font(size, family, style, weight)

    def update_trjectory(self):
        for d in self.drivers.itervalues():
            d.update_trajectory(tk.now)

    def update(self, ani_update=True):
        if ani_update:
            self.update_trjectory()
        self.Refresh()

    def OnPaint(self, _):
        # prepare.
        self.dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(self.dc)
        gc.SetPen(self.default_pen)
        gc.SetFont(self.default_font, wx.BLACK)
        # draw on logical space.
        oldTransform = gc.GetTransform()
        gc.Translate(self.translate_x, self.translate_y)
        self.OnDraw(gc)
        gc.SetTransform(oldTransform)
        self.OnDrawDevice(gc)

    def gen_bg_img(self):
        w, h = self.GetSize()
        bmp = wx.EmptyBitmap(w, h)
        # Create a memory DC that will be used for actually taking the screenshot
        dc = wx.MemoryDC(bmp)
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen(self.default_pen)
        gc.SetFont(self.default_font, wx.BLACK)
        # draw on logical space.
        oldTransform = gc.GetTransform()
        gc.Translate(self.translate_x, self.translate_y)
        #
        gpath = gc.CreatePath()
        gpath.MoveToPoint(self.sgBorder_xy[0])
        for i in range(1, len(self.sgBorder_xy)):
            gpath.AddLineToPoint(self.sgBorder_xy[i])
        for r_coords in GPS_xyDrawing.get_sgRoards_xy():
            gpath.MoveToPoint(r_coords[0])
            for i in range(1, len(r_coords)):
                gpath.AddLineToPoint(r_coords[i])
        gc.DrawPath(gpath)
        #
        gc.SetTransform(oldTransform)
        #
        img = bmp.ConvertToImage()
        img.SaveFile(bg_img_fpath, wx.BITMAP_TYPE_PNG)
        return bmp, w, h

    def OnDrawDevice(self, gc):
        gc.SetFont(DEVICE_DRAW_FONT)
        tx = self.main_frame.tx
        txs = ('%.1f' if tx < 1e5 else '%.1e') % tx
        gc.DrawText('%d/%02d/%02d %02d:%02d:%02d (speed X%s)' %
                    (tk.now.year, tk.now.month, tk.now.day,
                     tk.now.hour, tk.now.minute, tk.now.second, txs), 5, 3)

    def OnDraw(self, gc):
        if not self.bg_bmp:
            self.bg_bmp = self.gen_bg_img()
        bmp, w, h = self.bg_bmp
        gc.DrawBitmap(bmp, -self.translate_x, -self.translate_y, w, h)
        #
        for d in self.drivers.itervalues():
            d.draw(gc)
        # gc.SetPen(wx.Pen(wx.Colour(100, 100, 100), 0.9))
        # gc.DrawLines([(10, 10), (20, 20)])
