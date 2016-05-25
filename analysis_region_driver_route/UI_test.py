from __future__ import division
import wx, time
from polygon_reader import singapore_poly_points, vertical_lines, horizontal_lines

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'test', size=(300, 300))
        MyPanel(self)
        self.Show(True)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # size and mouse events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        
        self.translate_mode = False
        self.translate_x, self.translate_y = 0, 0
        self.scale = 1.0
        
        self.gpath = None
        
        
        
#         self.timer = wx.Timer(self)
#         self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
#         self.timer.Start(1000)
#         self.n = Node(0);
        
    def OnSize(self, evt):
        self.InitBuffer()
        evt.Skip()
        
    def OnLeftDown(self, evt):
        self.translate_mode = True
        print evt.GetX(), evt.GetY()
        self.prev_x, self.prev_y = evt.GetX(), evt.GetY()
        self.CaptureMouse()
        
    def OnMotion(self, evt):
        if self.translate_mode:
            dx, dy = evt.GetX() - self.prev_x, evt.GetY() - self.prev_y
            self.translate_x += dx
            self.translate_y += dy
            self.prev_x, self.prev_y = evt.GetX(), evt.GetY()
            self.RefreshGC()
    
    def OnLeftUp(self, evt):
        self.translate_mode = False
        self.ReleaseMouse()
    
#     def OnTimer(self, evt):
#         self.RefreshGC()
            
    def OnPaint(self, evt):
        _ = wx.BufferedPaintDC(self, self._buffer)
        
    def OnMouseWheel(self, evt):
        zoom_scale = 1.2
        old_scale = self.scale 
        if evt.GetWheelRotation() > 0:
            self.scale *= zoom_scale
            self.translate_x = evt.GetX() - self.scale / old_scale * (evt.GetX() - self.translate_x)
            self.translate_y = evt.GetY() - self.scale / old_scale * (evt.GetY() - self.translate_y) 
        else:
            self.scale /= zoom_scale
            self.translate_x = evt.GetX() - self.scale / old_scale * (evt.GetX() - self.translate_x)
            self.translate_y = evt.GetY() - self.scale / old_scale * (evt.GetY() - self.translate_y)
        self.RefreshGC()
        
    def InitBuffer(self):
        sz = self.GetClientSize()
        sz.width = max(1, sz.width)
        sz.height = max(1, sz.height)
        self._buffer = wx.EmptyBitmap(sz.width, sz.height, 32)
        dc = wx.MemoryDC(self._buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        self.Draw(gc)
        
    def RefreshGC(self):
        dc = wx.MemoryDC(self._buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        self.Draw(gc)
        self.Refresh(False)
    def set_scale(self, s, cx, cy):
        '''
        set scale based on (cx, cy) as center.
        '''
        old_scale, self.scale = self.scale, s
        self.translate_x = cx - self.scale / old_scale * (cx - self.translate_x)
        self.translate_y = cy - self.scale / old_scale * (cy - self.translate_y)
    def fit_viewport(self, x0, y0, x1, y1):
        assert x0 <= x1 and y0 <= y1
        EPSILON = 0.001
        dx, dy = max(x1 - x0, EPSILON), max(y1 - y0, EPSILON)
        cx, cy = x0 + dx / 2, y0 + dy / 2
        w, h = self.GetClientSize()
        self.translate_x, self.translate_y = -(cx - w / 2), -(cy - h / 2)
        self.set_scale(min(w / dx, h / dy) * 0.8, w / 2, h / 2)
    def Draw(self, gc):
        if not self.gpath:
            self.gpath = gc.CreatePath()
            # draw Singapore polygon
            reversed_points = [(x, -y)for x, y in singapore_poly_points]
            x_min = x_max = reversed_points[0][0]
            y_min = y_max = reversed_points[0][1]
            self.gpath.MoveToPoint(*reversed_points[0])
            for i in xrange(len(reversed_points) - 1):
                x, y = reversed_points[i + 1]
                self.gpath.AddLineToPoint(x, y)
                #
                x_min, x_max = min(x_min, x), max(x_max, x)
                y_min, y_max = min(y_min, y), max(y_max, y)
            self.gpath.AddLineToPoint(*reversed_points[0])
            #
            for sx, sy, ex, ey in vertical_lines + horizontal_lines:
                self.gpath.MoveToPoint(sx, -sy)
                self.gpath.AddLineToPoint(ex, -ey)
            self.fit_viewport(x_min, y_min, x_max, y_max)
        gc.Translate(self.translate_x, self.translate_y)
        gc.Scale(self.scale, self.scale)
        gc.SetPen(wx.Pen("black", 1000))
        gc.DrawPath(self.gpath)
        
#         t = time.localtime(time.time())
#         st = time.strftime("%I:%M:%S", t)
#         gc.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
#         gc.DrawText(st, 10, 150)

if __name__ == '__main__':
    app = wx.App()
    app.frame = MainFrame()
    app.MainLoop()
