from __future__ import division
#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.ticker as tkr
from file_handling_functions import check_dir_create, write_text_file

_rgb = lambda r, g, b: (r / float(255), g / float(255), b / float(255))

clists = (
    'blue', 'green', 'red', 'cyan', 'magenta', 'black',
    _rgb(255, 165, 0),  # orange
    _rgb(238, 130, 238),  # violet
    _rgb(255, 228, 225),  # misty rose
    _rgb(127, 255, 212),  # aqua-marine
    'yellow',
    _rgb(220, 220, 220),  # gray
    _rgb(255, 165, 0),  # orange
    'black'
)

mlists = (
    'o',  #    circle
    'v',  #    triangle_down
    '^',  #    triangle_up
    '<',  #    triangle_left
    '>',  #    triangle_right
    's',  #    square
    'p',  #    pentagon
    '*',  #    star
    '+',  #    plus
    'x',  #    x
    'D',  #    diamond
    'h',  #    hexagon1
    '1',  #    tri_down
    '2',  #    tri_up
    '3',  #    tri_left
    '4',  #    tri_right
    '8',  #    octagon
    'H',  #    hexagon2
    'd',  #    thin_diamond
    '|',  #    vline
    '_',  #    hline
    '.',  #    point
    ',',  #    pixel

    'D',  #    diamond
    '8',  #    octagon
          )
#
FONT_SIZE = 18
#


class simple_barchart(object):
    def __init__(self, x_ticks, y_label, _data, save_fn=None) :
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ind = np.arange(len(_data))
        width = 0.5  # the width of the bars
        ax.bar(ind, _data, width, color='blue')
        ax.set_xlim(-width, len(ind))
        ax.set_ylabel(y_label)
        plt.xticks(ind + width / float(2), x_ticks)
        for item in ([ax.yaxis.label] + ax.get_xticklabels()):
            item.set_fontsize(FONT_SIZE)
        if save_fn:
            plt.savefig(save_fn + '.pdf')
            #
            txt_path_fn = save_fn + '.txt'
            write_text_file(txt_path_fn, 'Init', True)
            for i in xrange(len(x_ticks)):
                write_text_file(txt_path_fn,'%s: %f' %(str(x_ticks[i]), _data[i]))
        plt.show()


class one_histogram(object):
    def __init__(self, _figsize, _title, x_label, y_label, num_bin, x_data, save_fn=None):
        plt.figure(figsize=_figsize)
        _, bins, _ = plt.hist(x_data, num_bin, normed=1, facecolor='green', alpha=0.75)
        x_mean, x_std = np.mean(x_data), np.std(x_data)
        # add a 'best fit' line
        plt.plot(bins, mlab.normpdf(bins, x_mean, x_std), 'r--', linewidth=1)
        #
        plt.xlabel(x_label); plt.ylabel(y_label)
        plt.title(r'$\mathrm{%s}\ \mu=%.2f,\ \sigma=%.2f$' % (_title, x_mean, x_std))
        if save_fn:
            plt.savefig(save_fn + '.pdf')
            #
            self.saving_histo_data(save_fn + '.txt', num_bin, x_data)

    def saving_histo_data(self, txt_path_fn, num_bin, x_data):
        num_data = len(x_data)
        sorted_data = sorted(x_data)
        min_v, max_v = sorted_data[0], sorted_data[-1]
        intervals = []
        interval = (max_v - min_v) / float(num_bin)
        bins = [[] for _ in xrange(num_bin)]
        for v in sorted_data[:-1]:
            i = int((v - min_v) / float(interval))
            lower_bound, upper_bound = min_v + i * interval, min_v + (i + 1) * interval
            bins[i].append(v)
            if (not intervals) or (intervals[-1] != [lower_bound, upper_bound]):
                intervals.append([lower_bound, upper_bound])
        bins[-1].append(max_v)
        #
        write_text_file(txt_path_fn, 'lower-bound,upper-bound,proportion')
        proportion = [len(_bin) / float(num_data) for _bin in bins]
        for i, (lower_bound, upper_bound) in enumerate(intervals):
            write_text_file(txt_path_fn,
                            '%f, %f, %s' % (lower_bound, upper_bound, str(proportion[i])))
        plt.show()


class histo_cumulative(object):
    def __init__(self, _title, x_label, y_label, num_bin, xs_data, _legend, save_fn=None):
        assert len(xs_data) == len(_legend)
        plt.figure(figsize=(6, 6))
        x_means, x_stds = [], []
        _xmax = -1e400
        for i, x_data in enumerate(xs_data):
            _xmax = max(_xmax, max(x_data))
            _, bins, _ = plt.hist(x_data, num_bin, normed=1,
                                    histtype='step', cumulative=True, color=clists[i])
            x_mean, x_std = np.mean(x_data), np.std(x_data)
            x_means.append(x_mean); x_stds.append(x_std)
            #
            y = mlab.normpdf(bins, x_mean, x_std).cumsum()
            y /= float(y[-1])
        plt.legend(_legend, ncol=1, loc='upper left', fontsize=10)
        #
        plt.xlabel(x_label); plt.ylabel(y_label)
        plt.xlim(xmax = _xmax)
        plt.ylim(ymax = 1.0)
        
        s = r'  '.join(['$\mathrm{%s}\ \mu=%.2f,\ \sigma=%.2f$' % (_legend[i], x_means[i], x_stds[i]) for i in xrange(len(_legend))])
        plt.title(s)
        
        if save_fn:
            plt.savefig(save_fn + '.pdf')
            #
            txt_path_fn = save_fn + '.txt'
            self.saving_histo_cumulative_data(txt_path_fn, num_bin, x_data)
        plt.show()

    def saving_histo_cumulative_data(self, txt_path_fn, num_bin, x_data):
        num_data = len(x_data)
        sorted_data = sorted(x_data)
        min_v, max_v = sorted_data[0], sorted_data[-1]
        intervals = []
        interval = (max_v - min_v) / float(num_bin)
        bins = [[] for _ in xrange(num_bin)]
        for v in sorted_data[:-1]:
            if v == max_v:
                i = len(bins) - 1
            else:
                i = int((v - min_v) / float(interval))
            lower_bound, upper_bound = min_v + i * interval, min_v + (i + 1) * interval
            try:
                bins[i].append(v)
            except IndexError:
                bins[-1].append(v)
            if (not intervals) or (intervals[-1] != [lower_bound, upper_bound]):
                intervals.append([lower_bound, upper_bound])
        #

        write_text_file(txt_path_fn, 'lower-bound,upper-bound,cum-proportion')
        proportion = [len(_bin) / float(num_data) for _bin in bins]
        cum_prob = [sum(proportion[:i+1]) for i in xrange(len(proportion))]
        for i, (lower_bound, upper_bound) in enumerate(intervals):
            write_text_file(txt_path_fn,
                            '%f, %f, %s' % (lower_bound, upper_bound, str(cum_prob[i])))
        plt.show()


class multiple_line_chart(object):
    def __init__(self, _figsize, _title, _xlabel, _ylabel, xticks_info, multi_y_data, y_legend_labels, legend_pos, save_fn=None):
        assert len(multi_y_data) == len(y_legend_labels), multi_y_data
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        ax.set_title(_title)
        ax.set_xlabel(_xlabel)
        ax.set_ylabel(_ylabel)
        ymax = 0
        for i, y_data in enumerate(multi_y_data):
            plt.plot(range(len(y_data)), y_data, linewidth=1, color=clists[i], marker=mlists[i])
            ymax1 = max(y_data)
            if ymax < ymax1:
                ymax = ymax1
        plt.legend(y_legend_labels, ncol=1, loc=legend_pos, fontsize=FONT_SIZE * 0.6)
        #
        _xticks, _rotation = xticks_info 
        plt.xticks(range(len(_xticks)), _xticks, rotation=_rotation)
        ax.set_xbound(lower=0, upper=range(len(_xticks))[-1])
        #
        ax.set_ybound(upper=ymax * 1.05)
        ax.yaxis.set_major_formatter(tkr.FuncFormatter(comma_formating))  # set formatter to needed axis
        for item in ([ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(FONT_SIZE)
        if save_fn:
            plt.savefig(save_fn + '.pdf')
            #
            txt_path_fn = save_fn + '.txt'
            write_text_file(txt_path_fn, 'Init', True)
            write_text_file(txt_path_fn, 'x-asix: %s' % str(_xticks))
            for i, ys in enumerate(multi_y_data):
                write_text_file(txt_path_fn, '%s: %s' %(y_legend_labels[i], str(ys)))
            write_text_file(txt_path_fn, '')
        plt.show()  

class x_twin_chart(object):
    def __init__(self, _figsize, _title, x_info, y_info1, y_info2, save_fn=None):
        _xlabel, _xticks, _rotation = x_info
        _ylabel1, multi_y_data1, bounds1, y_legend_labels1, legend_pos1 = y_info1
        _ylabel2, multi_y_data2, bounds2, y_legend_labels2, legend_pos2 = y_info2
        assert len(multi_y_data1) == len(y_legend_labels1)
        assert len(multi_y_data2) == len(y_legend_labels2)
        assert len(multi_y_data1[0]) == len(multi_y_data2[0])
        #
        fig = plt.figure(figsize=_figsize)
        #
        ax1 = fig.add_subplot(111)
        #
        ymax = 0
        for i, y_data in enumerate(multi_y_data1):
            plt.plot(range(len(y_data)), y_data, linewidth=1, color=clists[i], marker=mlists[i])
            ymax1 = max(y_data)
            if ymax < ymax1:
                ymax = ymax1
        plt.legend(y_legend_labels1, ncol=1, loc=legend_pos1, fontsize=FONT_SIZE * 0.8)
        if bounds1:
            ax1.set_ybound(lower=bounds1[0], upper=bounds1[1])
        else:
            ax1.set_ybound(upper=ymax * 1.05)
        ax1.yaxis.set_major_formatter(tkr.FuncFormatter(comma_formating))  # set formatter to needed axis
        plt.xticks(range(len(_xticks)), _xticks, rotation=_rotation)
        #
        ax2 = ax1.twinx()
        ymax = 0
        for i, y_data in enumerate(multi_y_data2):
            plt.plot(range(len(y_data)), y_data, '--', linewidth=1, color=clists[-(i + 1)], marker=mlists[-(i + 1)])
            ymax1 = max(y_data)
            if ymax < ymax1:
                ymax = ymax1
        plt.legend(y_legend_labels2, ncol=1, loc=legend_pos2, fontsize=FONT_SIZE * 0.8)
        if bounds2:
            ax2.set_ybound(lower=bounds2[0], upper=bounds2[1])
        else:
            ax2.set_ybound(upper=ymax * 1.05) 
        ax2.yaxis.set_major_formatter(tkr.FuncFormatter(comma_formating))  # set formatter to needed axis
        #
        
        ax1.set_xbound(lower=0, upper=range(len(_xticks))[-1])
        #
        ax1.set_title(_title)
        ax1.set_xlabel(_xlabel)
        ax1.set_ylabel(_ylabel1)
        ax2.set_ylabel(_ylabel2)
        #
        for item in ([ax1.xaxis.label, ax1.yaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
            item.set_fontsize(FONT_SIZE)
        if save_fn:
            plt.savefig(save_fn + '.pdf')
            #
            txt_path_fn = save_fn + '.txt'
            write_text_file(txt_path_fn, 'Init', True)
            write_text_file(txt_path_fn, 'x-asix: %s' % str(_xticks))
            write_text_file(txt_path_fn, '-----------------------y1-asix')
            for i, ys in enumerate(multi_y_data1):
                write_text_file(txt_path_fn, '%s: %s' %(y_legend_labels1[i], str(ys)))
            write_text_file(txt_path_fn, '-----------------------y2-asix')
            for i, ys in enumerate(multi_y_data2):
                write_text_file(txt_path_fn, '%s: %s' %(y_legend_labels2[i], str(ys)))    
            write_text_file(txt_path_fn, '')
            
        plt.show()

class line_3D(object):
    def __init__(self, _figsize, _title, _xlabel, _ylabel, _zlabel, _data):
        fig = plt.figure(figsize=_figsize)
        ax = fig.gca(projection='3d')
        ax.set_title(_title); ax.set_xlabel(_xlabel); ax.set_ylabel(_ylabel); ax.set_zlabel(_zlabel)
        for xyz in _data:
            x, y, z = zip(*xyz)
            ax.plot(x, y, z)
            ax.legend()
        plt.show()

class bar_table(object):
    def __init__(self, _figsize, _title, _ylabel, row_labels, col_labels, table_data, save_fn=None):
        assert len(table_data) == len(row_labels)
        assert len(table_data[0]) == len(col_labels)
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        #
        bar_width = 0.5
        ind = [bar_width / float(2) + i for i in xrange(len(col_labels))]
        #
        bar_data = table_data[:]
        bar_data.reverse()
        y_offset = np.array([0.0] * len(col_labels))
        for i, row_data in enumerate(bar_data):
            plt.bar(ind, row_data, bar_width, bottom=y_offset, color=clists[i])
            y_offset = y_offset + row_data
        ax.set_xlim(0, len(ind))
        #
        formatted_table_data = []
        for r in table_data:
            formatted_table_data.append(['{:,}'.format(x) for x in r])
        table = plt.table(cellText=formatted_table_data, colLabels=col_labels, rowLabels=row_labels, loc='bottom')
        table.scale(1, 2)
        #
        plt.subplots_adjust(left=0.2, bottom=0.2)
        plt.ylabel(_ylabel)
        ax.yaxis.set_major_formatter(tkr.FuncFormatter(comma_formating))  # set formatter to needed axis
        plt.xticks([])
        plt.title(_title)
        if save_fn:
            plt.savefig(save_fn + '.pdf')
        plt.show()

class one_pie_chart(object):
    def __init__(self, _title, per_data, _labels, save_fn=None):
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        labels = []
        for i, l in enumerate(_labels):
            labels.append('%s (%.2f)' % (l, per_data[i]))
        ax.pie(per_data, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.legend(labels, fontsize='x-small')
        ax.set_title(_title)
        if save_fn:
            plt.savefig(save_fn + '.pdf')
        plt.show()

class two_pie_chart(object):
    def __init__(self, _labels, title1, per_data1, title2, per_data2, save_fn=None):
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(121)
        labels = []
        for i, l in enumerate(_labels):
            labels.append('%s (%.2f)' % (l, per_data1[i]))
        ax.pie(per_data1, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.legend(labels, fontsize='x-small')
        ax.set_title(title1)
        
        ax = fig.add_subplot(122)
        for i, l in enumerate(_labels):
            labels.append('%s (%.2f)' % (l, per_data2[i]))
        ax.pie(per_data2, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.legend(labels, fontsize='x-small')
        ax.set_title(title2)
        if save_fn:
            plt.savefig(save_fn + '.pdf')
        plt.show()

class histograms(object):
    def __init__(self, _figsize, chart_info):
        # chart_info is two dimensional array (list)
        # The first dimension means rows
        # ex. 2X2 charts
        # [
        # [(_title, x_label, y_label, num_bin, x_data), (_title, x_label, y_label, num_bin, x_data)],
        # [(_title, x_label, y_label, num_bin, x_data), (_title, x_label, y_label, num_bin, x_data)]
        # ] 
        plt.figure(figsize=_figsize)
        _, axarr = plt.subplots(len(chart_info), len(chart_info[0]))
        for i, row in enumerate(chart_info):
            for j, (_title, x_label, y_label, num_bin, x_data) in enumerate(row):
                ax = axarr[i + j]
                _, bins, _ = ax.hist(x_data, num_bin, normed=1, facecolor='green', alpha=0.75)
                x_mean, x_std = np.mean(x_data), np.std(x_data)
                # add a 'best fit' line
                ax.plot(bins, mlab.normpdf(bins, x_mean, x_std), 'r--', linewidth=1)
                #
                ax.set_xlabel(x_label); ax.set_ylabel(y_label)
                ax.set_title(r'$\mathrm{%s}\ \mu=%.2f,\ \sigma=%.2f$' % (_title, x_mean, x_std))
        plt.show()

class bar_chart(object):
    def __init__(self, _title, _ylabel, xTickMarks, _data):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ind = np.arange(len(_data))
        width = 0.4  # the width of the bars
        #
        ax.bar(ind, _data, width, color='blue')
        # axes and labels
        ax.set_xlim(-width, len(ind) + width)
        ax.set_ylabel(_ylabel)
        ax.set_title(_title)
        ax.set_xticks(ind + width)
        xtickNames = ax.set_xticklabels(xTickMarks)
        plt.setp(xtickNames, rotation=25, fontsize=10)
        
        # # add a legend
        plt.show()

class one_bar_chart(object):
    def __init__(self, _title, _ylabel, xTickMarks, data1, data2, legends):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #
        ind = np.arange(len(data1))
        width = 0.4  # the width of the bars
        
        # # the bars
        rects1 = ax.bar(ind, data1, width, color='blue')
        rects2 = ax.bar(ind + width, data2, width, color='red')
        
        # axes and labels
        ax.set_xlim(-width, len(ind) + width)
        ax.set_ylabel(_ylabel)
        ax.set_title(_title)
        ax.set_xticks(ind + width)
        xtickNames = ax.set_xticklabels(xTickMarks)
        plt.setp(xtickNames, rotation=25, fontsize=10)
        
        # # add a legend
        ax.legend((rects1[0], rects2[0]), legends)
        plt.show()

class horizontal_bar_chart(object):
    UNIT = 1.0
    HALF_UNIT = UNIT / float(2)
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    FIG_SIZE_UNIT = 6
    def __init__(self, main_name, sub_name, x_data):
        fig = plt.figure(figsize=(grid_charts.FIG_SIZE_UNIT, grid_charts.FIG_SIZE_UNIT))
        paths = []
        xs, ys = [], []
        for i in xrange(len(x_data)):
            x, y = x_data[i], i
            xs.append(x); ys.append(y)
            if x >= 0 :
                left_bottom = (0, y - grid_charts.HALF_UNIT) 
                left_top = (0, y + grid_charts.HALF_UNIT)
                right_top = (x, y + grid_charts.HALF_UNIT)
                right_bottom = (x, y - grid_charts.HALF_UNIT)
                ignored = left_bottom
                verts = [left_bottom, left_top  , right_top , right_bottom, ignored]
            else:
                left_bottom = (x, y - grid_charts.HALF_UNIT) 
                left_top = (x, y + grid_charts.HALF_UNIT)
                right_top = (0, y + grid_charts.HALF_UNIT)
                right_bottom = (0, y - grid_charts.HALF_UNIT)
                ignored = left_bottom
                verts = [left_bottom, left_top  , right_top , right_bottom, ignored]
            paths.append(Path(verts, grid_charts.codes))
        ax = fig.add_subplot(111)
        for i, path in enumerate(paths):
            patch = patches.PathPatch(path, facecolor=clists[0])
            ax.add_patch(patch)
        ax.set_xlim(min(xs) - grid_charts.HALF_UNIT, max(xs) + grid_charts.HALF_UNIT)
        ax.set_ylim(min(ys) - grid_charts.HALF_UNIT, max(ys) + grid_charts.HALF_UNIT)
        ax.grid()
        plt.yticks([int(len(ys) * 0.00), int(len(ys) * 0.25), int(len(ys) * 0.50), int(len(ys) * 0.75), int(len(ys) * 1.00)], ['0%', '25%', '50%', '75%', '100%'])
        # TODO
        # Modify saving part
        plt.savefig('%s-%s.pdf' % (main_name, sub_name))
#         plt.show()

class grid_charts(object):
    UNIT = 1.0
    HALF_UNIT = UNIT / float(2)
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    FIG_SIZE_UNIT = 6
    def __init__(self, x_axis_info, y_axis_info, _legends, titles, _data, fn=None):
        _xlabel, _xticks = x_axis_info
        _ylabel, _yticks = y_axis_info
        num_charts = len(_data)
        #
        fig = plt.figure(figsize=(grid_charts.FIG_SIZE_UNIT * num_charts, grid_charts.FIG_SIZE_UNIT))
        
        if fn:
            # TODO save it !!
            for i, points_color in enumerate(_data):
                self.draw_a_chart(fig, num_charts, i, _legends, _xlabel, _ylabel, _xticks, _yticks, points_color)
            plt.savefig(fn)
        else:
            for i, points_color in enumerate(_data):
                self.draw_a_chart(fig, num_charts, i, _legends, _xlabel, _ylabel, _xticks, _yticks, points_color, titles[i])
            plt.show()
        
    def draw_a_chart(self, fig, num_charts, _th, _legends, _xlabel, _ylabel, _xticks, _yticks, points_color, title=None):
        paths, color_choices = [], []
        for x, y, c in points_color:
            verts = self.gen_rect_coord_by_center(x, y)
            paths.append(Path(verts, grid_charts.codes))
            color_choices.append(c)
        colors_set = set(color_choices)
        print colors_set
        labeled = [False for _ in xrange(len(colors_set))]
        ax = fig.add_subplot(1, num_charts, _th + 1)
        for i, path in enumerate(paths):
            if not labeled[color_choices[i]]:
                patch = patches.PathPatch(path, facecolor=clists[color_choices[i]], label='%s' % _legends[color_choices[i]])
                labeled[color_choices[i]] = True
            else:
                patch = patches.PathPatch(path, facecolor=clists[color_choices[i]])
            ax.add_patch(patch)
        xs, ys, _ = zip(*points_color)
        ax.set_xlim(min(xs) - grid_charts.HALF_UNIT, max(xs) + grid_charts.HALF_UNIT)
        ax.set_ylim(min(ys) - grid_charts.HALF_UNIT, max(ys) + grid_charts.HALF_UNIT)
        #
        if title: plt.text(0.5, 1.08, title, horizontalalignment='center', transform=ax.transAxes)
        if _xlabel: plt.xlabel(_xlabel)
        if _ylabel: plt.ylabel(_ylabel)
        if _xticks: plt.xticks(_xticks)
        if _yticks: plt.yticks(range(len(_yticks)), _yticks)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0., framealpha=0.0)
        
                
    def gen_rect_coord_by_center(self, x, y):
        left_bottom = (x - grid_charts.HALF_UNIT, y - grid_charts.HALF_UNIT) 
        left_top = (x - grid_charts.HALF_UNIT, y + grid_charts.HALF_UNIT)
        right_top = (x + grid_charts.HALF_UNIT, y + grid_charts.HALF_UNIT)
        right_bottom = (x + grid_charts.HALF_UNIT, y - grid_charts.HALF_UNIT)
        ignored = left_bottom
        return [left_bottom, left_top  , right_top , right_bottom, ignored]



class one_grid_chart(object):
    UNIT = 1.0
    HALF_UNIT = UNIT / float(2)
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    FIG_SIZE_UNIT = 6
    def __init__(self, x_axis_info, y_axis_info, _legends, titles, _data, save_fn=None):
        _xlabel, _xticks = x_axis_info
        _ylabel, _yticks = y_axis_info
        #
        fig = plt.figure(figsize=(grid_charts.FIG_SIZE_UNIT, grid_charts.FIG_SIZE_UNIT))
        
        paths, color_choices = [], []
        for x, y, c in _data:
            verts = self.gen_rect_coord_by_center(x, y)
            paths.append(Path(verts, grid_charts.codes))
            color_choices.append(c)
        colors_set = set([0, 1])

        labeled = [False for _ in xrange(len(colors_set))]
        ax = fig.add_subplot(1, 1, 1)
        for i, path in enumerate(paths):
            try:
                if not labeled[color_choices[i]]:
                    patch = patches.PathPatch(path, facecolor=clists[color_choices[i]], label='%s' % _legends[color_choices[i]])
                    labeled[color_choices[i]] = True
                else:
                    patch = patches.PathPatch(path, facecolor=clists[color_choices[i]])
                ax.add_patch(patch)
            except IndexError:
                pass
        xs, ys, _ = zip(*_data)
        ax.set_xlim(min(xs) - grid_charts.HALF_UNIT, max(xs) + grid_charts.HALF_UNIT)
        ax.set_ylim(min(ys) - grid_charts.HALF_UNIT, max(ys) + grid_charts.HALF_UNIT)
        #
#         if title: plt.text(0.5, 1.08, title, horizontalalignment='center', transform=ax.transAxes)
        if _xlabel: plt.xlabel(_xlabel)
        if _ylabel: plt.ylabel(_ylabel)
        if _xticks: plt.xticks(_xticks)
        if _yticks: plt.yticks(range(len(_yticks)), _yticks)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0., framealpha=0.0)
        if save_fn:
            plt.savefig(save_fn + '.pdf')
        plt.show()
                
    def gen_rect_coord_by_center(self, x, y):
        left_bottom = (x - grid_charts.HALF_UNIT, y - grid_charts.HALF_UNIT) 
        left_top = (x - grid_charts.HALF_UNIT, y + grid_charts.HALF_UNIT)
        right_top = (x + grid_charts.HALF_UNIT, y + grid_charts.HALF_UNIT)
        right_bottom = (x + grid_charts.HALF_UNIT, y - grid_charts.HALF_UNIT)
        ignored = left_bottom
        return [left_bottom, left_top  , right_top , right_bottom, ignored]

def comma_formating(x, pos):  # formatter function takes tick label and tick position
#     return int(x)
    if x == 0:
        return int(x)
    if abs(x) == 5:
        return int(x)
    if x < 10:
        return int(x)
    s = '%d' % x
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))

def test():
#     n_bins = 50
#     mu, sigma = 200, 25
#     x1 = mu + sigma*np.random.randn(10000)
#     mu, sigma = 200, 50
#     x2 = mu + sigma*np.random.randn(10000)
#     
#     histo_cumulative('', 'x_label', 'y_label', n_bins, [x1, x2], ['Y2009', 'Y2010'], save_fn=None)
    
    num_trip = [306117 , 201973 , 53408 , 31251 , 24590 , 66184 , 198111 , 182191 , 150242 , 123608 , 112527 , 128077 , 182481 , 170057 , 195326 , 248171 , 237464 , 242071 , 279671 , 229624 , 325573 , 296758 , 448576 , 352399]
    Y10_hourly_qt = [35.644270303044173, 33.305448869989497, 35.575034632579808, 48.892812311406153, 45.296450886645928, 45.857049134561699, 31.763542493054452, 39.714915922338243, 40.110275205474359, 39.032016512734394, 32.560647065540643, 37.414089385948792, 29.322102361320329, 25.227071068052087, 31.205467697781788, 26.152910906075856, 19.631667520747037, 32.29702635705975, 33.327335019456136, 37.29772387602597, 25.936866618111193, 27.367216483677542, 23.632204569609808, 21.096308120285414]
    Y09_hourly_qt = [41.641760669048146, 42.342235952066034, 42.775465828944533, 52.787501986694821, 47.973749233330409, 49.522126531418785, 33.503306840500692, 42.274819497636983, 45.191994984491522, 45.915898340620288, 40.185395185217821, 42.008305725079921, 36.705277631358513, 33.449317076056928, 34.92462150184469, 27.073668411073189, 26.716538437738496, 38.82035826434916, 37.923223821160285, 40.354963036913325, 29.652411745091413, 33.545230534875238, 25.797125672219924, 25.760345526162997]
    from supports._setting import TIME_SLOTS
    
    diff = [Y09_hourly_qt[i] - Y10_hourly_qt[i] for i in xrange(len(Y10_hourly_qt))]
    x_info = ('Time slot', TIME_SLOTS, 0)
    y_info1 = ('Minute', [Y09_hourly_qt, Y10_hourly_qt, diff], (-5, 60), ['Y2009', 'Y2010', 'Diff.'], 'upper left')
    y_info2 = ('', [num_trip], (0, 350000), ['Number of airport trips'], 'upper right') 
    x_twin_chart((12, 6), '', x_info, y_info1, y_info2, 'time_slot_queue_time')

if __name__ == '__main__':
    test()
