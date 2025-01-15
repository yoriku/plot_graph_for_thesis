import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from typing import Literal
from scipy.stats import ttest_ind, brunnermunzel
from statsmodels.stats.multitest import multipletests

class Annot:
    def __init__(self, df, y="y", fs=20):
        self.max_h = np.max(df[y].values)
        self.fs = fs
        self.fspx = fs * 4 / 3
        self.origin_ax_min_y, self.origin_ax_max_y = plt.gca().get_ylim()
        dpp = plt.rcParams["figure.dpi"] / 96
        p_miny, p_maxy = plt.gca().get_window_extent().get_points()[:, 1]
        self.p_miny, self.p_maxy = p_miny / dpp, p_maxy / dpp

    def get(self, level):
        level -= 0.5
        font_height = self.fspx * (self.origin_ax_max_y - self.origin_ax_min_y) / (self.p_maxy - self.p_miny)
        return font_height * level
    
    def plot(self, ax, points):
        for s,e,l,text in points:
            if text != "":
                h = self.max_h + self.get(l)
                ax.plot([s,e], [h, h], color="black", clip_on=False)
                ax.text((s+e)/2, h + self.get(1), text, color="black", horizontalalignment='center', fontsize=self.fs)
        return ax


class Stat:
    def __init__(self, stat_name="brunnermunzel", adjust_name=None, stat_mark="*"):
        self.stat_name = stat_name
        self.adjust_name = adjust_name
        self.stat_mark = stat_mark
        
    def sort(self, l_hues):
        combinations = list(itertools.combinations(l_hues, 2))
        sorted_combinations = sorted(combinations, key=lambda pair: abs(pair[0] - pair[1]))
        return sorted_combinations
    
    def exe_stat(self, x1 ,x2):
        if self.stat_name == "welch":
            p = ttest_ind(x1, x2, equal_var=False, nan_policy="omit")[1]
        elif self.stat_name == "brunnermunzel":
            p = brunnermunzel(x1, x2, nan_policy="omit", distribution="normal")[1]
        else:
            raise ValueError("stat mode only welch or brunnermunzel")
        return p
    
    def exe_adjust(self, l_p):
        if self.adjust_name is None:
            l_p_mark = []
            if self.stat_mark is None:
                l_p_mark = [f"p={p:.3f}" if p >= 0.001 else f"p<0.001" for p in l_p]
            else:
                for p in l_p:
                    l_p_mark.append(lookup_p(p, self.stat_mark))
            return l_p, l_p_mark
        else:
            l_p = multipletests(l_p, method=self.adjust_name)[1]
            if self.stat_mark is None:
                l_p_mark = [f"p={p:.3f}" if p >= 0.001 else f"p<0.001" for p in l_p]
            else:
                l_p_mark = []
                for p in l_p:
                    l_p_mark.append(lookup_p(p, self.stat_mark))
            return l_p, l_p_mark
    
    def adjust_level(self, points):
        col_level = 0
        th = 0
        prev_level, prev_end_point = -100, -100
        adjusted_points = []
        for s,e,l,text in points:
            if th+0.5 < s:
                col_level = 0
                prev_level, prev_end_point = -100, -100
                th += 1

            if text != "" and l>2:

                if prev_level == l and prev_end_point > s:
                    col_level += 2
                prev_end_point = e
                prev_level = l
                l += col_level

            adjusted_points.append((s,e,l,text))
        return adjusted_points

    def calc(self, df, x, y, hue, width=0.8):
        xs = get_unigue(df, x, sort=True)
        hues = get_unigue(df, hue, sort=True)
        n_hue = len(hues)
        l_hues = np.arange(n_hue)
        c_hues = self.sort(l_hues)

        l_p = []
        for i, name_x in enumerate(xs):
            for i1, i2 in c_hues:
                df_tmp = df[df[x] == name_x].copy()
                x1, x2 = df_tmp[df_tmp[hue] == hues[i1]][y].values, df_tmp[df_tmp[hue] == hues[i2]][y].values
                p = self.exe_stat(x1,x2)
                l_p.append(p)

        l_p, l_p_mark = self.exe_adjust(l_p)

        annot_stat = []
        i_mark = 0
        for i, name_x in enumerate(xs):
            for i1, i2 in c_hues:
                gap = width / n_hue
                start = 0
                if n_hue%2 == 0:
                    start = width/(n_hue*2)
                start -= gap*(n_hue//2)
                s,e = (start+i) + gap*i1, (start+i) + gap*i2  
                l = i2-i1
                annot_stat.append((s+0.01, e-0.01, l*2, l_p_mark[i_mark]))
                i_mark +=1
        
        return self.adjust_level(annot_stat)

def get_unigue(df, i, sort=True):
    i, indexes = np.unique(df[i].values, return_index=True)
    i = np.array([str(s_i) for s_i in i])
    indexes = np.argsort(indexes)
    if sort:
        return i[indexes]
    else:
        return i


def lookup_p(p, mark):
    if p < 0.001:
        return mark+mark+mark
    if p < 0.01:
        return mark+mark
    if p < 0.05:
        return mark
    return ""

class PLOT:
    def __init__(self, figsize=(10, 8), font_size=20, is_times_new_roman=False, save_mode=["png", "pdf"]):
        self.font_size = font_size
        for _ in range(2):
            self.fig, self.ax = self.update_fig(figsize)
            self.figsize = figsize
            self.save_mode = save_mode

            plt.rcParams["mathtext.fontset"] = "stix"  # stixフォントにする
            if is_times_new_roman:
                plt.rcParams['font.family'] = 'Times New Roman'
            plt.rcParams['font.size'] = font_size
            plt.rcParams['xtick.direction'] = 'in'  # in or out
            plt.rcParams['ytick.direction'] = 'in'
            plt.rcParams['xtick.major.width'] = 2  # x軸主目盛り線の線幅
            plt.rcParams["ytick.major.size"] = 4.0
            plt.rcParams['ytick.major.width'] = 2  # y軸主目盛り線の線幅
            plt.rcParams['axes.linewidth'] = 3
            plt.rcParams["ytick.major.size"] = 4.0
            plt.rcParams['axes.xmargin'] = 0.01
            plt.rcParams['axes.ymargin'] = 0.01
            plt.rcParams["legend.fancybox"] = False  # 丸角OFF
            plt.rcParams["legend.framealpha"] = 1  # 透明度の指定、0で塗りつぶしなし
            plt.rcParams["legend.edgecolor"] = 'black'  # edgeの色を変更

    def update_fig(self, figsize):
        self.figsize = figsize
        fig = plt.figure(figsize=figsize, dpi=100)
        ax = fig.add_subplot(111)
        return fig, ax
    
    def delete_fig(self):
        self.fig.clear()
        plt.close(self.fig)
        return self
    
    def range(self, ax, xticks=None, yticks=None, zero_start=False):
        if xticks is not None:
            ax.set_xticks(xticks)
            ax.set_xlim(xticks[0], xticks[-1])
        if yticks is not None:
            ax.set_yticks(yticks)
            ax.set_ylim(yticks[0], yticks[-1])
        else:
            y_min, y_max = ax.get_ylim()
            if zero_start:
                y_min = 0
                ax.set_ylim(y_min, y_max)
        return ax
    
    def save(self, fig, filename):
        for mode in self.save_mode:
            if mode =="pdf":
                fig.savefig(f"{filename}.{mode}", transparent=True)
            else:
                fig.savefig(f"{filename}.{mode}")
        return fig

    
    def box(self, df, filename, figsize=None, kind="|", 
            x="x", y="y", hue=None, y_const=None, zero_start=False, 
            color=["#0066CC", "#FF0000"], yticks=None, rotation=0,
            stats={"stat_name": "brunnermunzel", "adjust_name": None, "stat_mark": "*"}):
        if figsize is not None and self.figsize != figsize:
            self.fig, self.ax = self.delete_fig().update_fig(figsize)
        fig, ax = self.fig, self.ax
        
        PROPS = {
        'boxprops': {'edgecolor': 'black'},
        'medianprops': {'color': 'black'},
        'whiskerprops': {'color': 'black'},
        'capprops': {'color': 'black'}
        }

        if y_const is not None:
            ax.axhline(y=y_const, c="b", linewidth=3)
        
        xs = get_unigue(df, x, sort=True)

        hue_order = None
        if hue is not None:
            hue_order = get_unigue(df, hue, sort=True)
            df[hue] = df[hue].astype(str)
        df[x] = df[x].astype(str)
        
        if kind !="|":
            x, y = y, x
            xs = None

        sns.set_palette(color)
        sns.boxplot(x=x, y=y, data=df, hue=hue, order=xs, hue_order=hue_order, ax=ax, linewidth=2, width=0.8, 
                        showmeans=True,
                        flierprops=dict(marker='o',
                                        markersize=10,
                                        markerfacecolor='black',
                                        markeredgewidth=0),
                        meanprops={"marker": "x",
                                "markeredgewidth": 2,
                                "markerfacecolor": "black",
                                "markeredgecolor": "black",
                                "markersize": "20"}, **PROPS)
        
        ax = self.range(ax, yticks=yticks, zero_start=zero_start)

        if hue is not None:
            ax.get_legend().remove()

        for tick in ax.get_xticklabels():
            tick.set_rotation(rotation)
        sns.despine()

        if stats is not None and hue is not None and kind=="|":
            stat = Stat(**stats)
            annot_text = stat.calc(df, x, y, hue)

            annot = Annot(df, y=y, fs=min(self.font_size,20))
            ax = annot.plot(ax, annot_text)

        plt.tight_layout(pad=1.1)

        fig = self.save(fig, filename)

        plt.cla()
    
    def line(self, df, filename, figsize=None, 
            x="x", y="y", hue=None, y_const=None, zero_start=False, 
            errorbar="sd", color=["#0066CC", "#FF0000"], xticks=None, yticks=None, rotation=0):
        if figsize is not None and self.figsize != figsize:
            self.fig, self.ax = self.delete_fig().update_fig(figsize)
        fig, ax = self.fig, self.ax

        if y_const is not None:
            ax.axhline(y=y_const, c="b", linewidth=3)

        sns.set_palette(color)
        sns.lineplot(x=x, y=y, data=df, hue=hue, ax=ax, linewidth=3, errorbar=errorbar)

        ax = self.range(ax,xticks=xticks, yticks=yticks, zero_start=zero_start)

        if hue is not None:
            ax.get_legend().remove()

        for tick in ax.get_xticklabels():
            tick.set_rotation(rotation)
        sns.despine()
        plt.tight_layout(pad=1.1)

        fig = self.save(fig, filename)

        plt.cla()
    
    
    def bar(self, df, filename, figsize=None, 
            x="x", y="y", hue=None, y_const=None, zero_start=False, 
            errorbar="sd", kind="|", stacked=False, 
            color=["#0066CC", "#FF0000"], xticks=None, yticks=None, rotation=0,
            stats={"stat_name": "brunnermunzel", "adjust_name": None, "stat_mark": "*"}):

        if figsize is not None and self.figsize != figsize:
            self.fig, self.ax = self.delete_fig().update_fig(figsize)
        
        fig, ax = self.fig, self.ax

        if y_const is not None:
            ax.axhline(y=y_const, c="b", linewidth=3)

        xs = get_unigue(df, x, sort=True)

        hue_order = None
        if hue is not None:
            hue_order = get_unigue(df, hue, sort=True)
            df[hue] = df[hue].astype(str)
        df[x] = df[x].astype(str)
        
        if kind !="|":
            x, y = y, x
            xs = None
        
        sns.set_palette(color)
        if stacked:
            df.plot(kind="bar", stacked=stacked, ax=ax, color=color)
        else:
            sns.barplot(x=x, y=y, data=df, hue=hue, ax=ax, order=xs, hue_order=hue_order, errorbar=errorbar, capsize=0.05)

        ax = self.range(ax,xticks=xticks, yticks=yticks, zero_start=zero_start)

        if hue is not None:
            ax.get_legend().remove()

        
        for tick in ax.get_xticklabels():
            tick.set_rotation(rotation)
        sns.despine()

        if stats is not None and hue is not None and kind=="|":
            stat = Stat(**stats)
            annot_text = stat.calc(df, x, y, hue)

            annot = Annot(df, y=y, fs=min(self.font_size,20))
            ax = annot.plot(ax, annot_text)

        plt.tight_layout(pad=1.1)

        fig = self.save(fig, filename)

        plt.cla()
    
    def confusion_matrix(self, ave, filename, figsize=None, 
                         std=None, classes=None, cmap="Blues", fontsize=25):
        if figsize is not None and self.figsize != figsize:
            self.fig, self.ax = self.delete_fig().update_fig(figsize)
        fig, ax = self.fig, self.ax

        cm, cms = ave, std

        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.colorbar()
        if classes is not None:
            tick_marks = np.arange(len(classes))
            plt.xticks(tick_marks, classes)
            plt.yticks(tick_marks, classes)

        thresh = cm.max() / 2.

        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                if cms is None:
                    _text = '{0:.2f}'.format(cm[i, j])
                else:
                    _text = '{0:.2f}'.format(cm[i, j]) + '\n$\pm$' + '{0:.2f}'.format(cms[i, j])
                plt.text(j, i, _text,
                        horizontalalignment="center",
                        verticalalignment="center", fontsize=fontsize,
                        color="white" if cm[i, j] > thresh else "black")

        sns.despine(left=True, bottom=True)
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')

        plt.tight_layout(pad=1.1)

        fig = self.save(fig, filename)

        plt.cla()
        self.fig, self.ax = self.delete_fig().update_fig(self.figsize)
    
    def spectrogram(self, df, filename, figsize=None, 
                    cmap="jet", xticks=None, yticks=None, rotation=0):

        if figsize is not None and self.figsize != figsize:
            self.fig, self.ax = self.delete_fig().update_fig(figsize)
        
        fig, ax = self.fig, self.ax

        t = df.columns
        f = df.index
        X = df.values

        ax.pcolormesh(t, f, X, cmap=cmap)
        sns.despine(left=True, bottom=True)
        
        ax = self.range(ax,xticks=xticks, yticks=yticks, zero_start=False)
        
        for tick in ax.get_xticklabels():
            tick.set_rotation(rotation)
        plt.tight_layout(pad=1.1)

        fig = self.save(fig, filename)

        plt.cla()
        self.fig, self.ax = self.delete_fig().update_fig(self.figsize)

    def movie2frame(video_path, frame_num=0, result_path="cut.png"):
        import cv2
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return

        os.makedirs(os.path.dirname(result_path), exist_ok=True)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(result_path, frame)
    
    def convert(self, df, x="x", y="y", hue=None, index2x=False):
        if index2x:
            df[x] = df.index
            if hue is not None:
                df = pd.melt(df, id_vars=x, var_name="hue", value_name=y)
        else:
            if hue is not None:
                df = pd.melt(df, id_vars=hue, var_name=x, value_name=y)
            else:
                df = pd.melt(df, var_name=x, value_name=y)
        return df
    
    def get_color(self, name: Literal["BR", "BG", "KW", "C3", "C5", "pastel", "vivid"] = "BR"):
        BR = ["#0066CC", "#FF0000"]
        BG = ["#1a198a", "#19B900"]
        KW = ["#333333", "#AAAAAA"]
        C3 = ["#ff7f00", "#19B900", "#0066CC"]
        C5 = ["#1a198a", "#19B900", "#333333", "#ff7f00", "#e41a1c"]
        pastel = ["#ff7f7f", "#ff7fff", "#7f7fff", "#7fffff", "#7fff7f", "#ffff7f"]
        vivid = ["#ff2d2d", "#ff2dff", "#2d2dff", "#2dffff", "#2dff2d", "#ffff2d"]

        return eval(name)

if __name__ == "__main__":
    df = pd.read_csv("https://raw.githubusercontent.com/yoriku/tmp_csv/main/kadai.csv")

    plot = PLOT()

    df = plot.convert(df, hue="target")
    color = plot.get_color("C3")

    plot.bar(df, "test", hue="target", color=color)
