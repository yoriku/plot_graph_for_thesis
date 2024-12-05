import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from typing import Literal

class PLOT:
    def __init__(self, figsize=(10, 8), font_size=20, is_times_new_roman=False, save_mode=["png", "pdf"]):
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
            color=["#0066CC", "#FF0000"], yticks=None, rotation=0):
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
        
        if kind !="|":
            x, y = y, x

        sns.set_palette(color)
        sns.boxplot(x=x, y=y, data=df, hue=hue, ax=ax, linewidth=2, width=0.8,
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
        plt.tight_layout(pad=1.1)

        fig = self.save(fig, filename)

        plt.cla()
    
    def line(self, df, filename, figsize=None, 
            x="x", y="y", hue=None, y_const=None, zero_start=False, 
            color=["#0066CC", "#FF0000"], xticks=None, yticks=None, rotation=0):
        if figsize is not None and self.figsize != figsize:
            self.fig, self.ax = self.delete_fig().update_fig(figsize)
        fig, ax = self.fig, self.ax

        if y_const is not None:
            ax.axhline(y=y_const, c="b", linewidth=3)

        sns.set_palette(color)
        sns.lineplot(x=x, y=y, data=df, hue=hue, ax=ax, linewidth=3)

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
            color=["#0066CC", "#FF0000"], xticks=None, yticks=None, rotation=0):

        if figsize is not None and self.figsize != figsize:
            self.fig, self.ax = self.delete_fig().update_fig(figsize)
        
        fig, ax = self.fig, self.ax

        if y_const is not None:
            ax.axhline(y=y_const, c="b", linewidth=3)

        if kind !="|":
            x, y = y, x
        
        sns.set_palette(color)
        if stacked:
            df.plot(kind="bar", stacked=stacked, ax=ax, color=color)
        else:
            sns.barplot(x=x, y=y, data=df, hue=hue, ax=ax, errorbar=errorbar, capsize=0.05)

        ax = self.range(ax,xticks=xticks, yticks=yticks, zero_start=zero_start)

        if hue is not None:
            ax.get_legend().remove()

        
        for tick in ax.get_xticklabels():
            tick.set_rotation(rotation)
        sns.despine()
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
    
    def convert(self, df, hue=None, index2x=False):
        if index2x:
            df["x"] = df.index
            if hue is not None:
                df = pd.melt(df, id_vars="x", var_name="hue", value_name="y")
        else:
            if hue is not None:
                df = pd.melt(df, id_vars=hue, var_name="x", value_name="y")
            else:
                df = pd.melt(df, var_name="x", value_name="y")
        return df
    
    def get_color(self, name: Literal["BR", "BG", "KW", "C3", "C5"] = "BR"):
        BR = ["#0066CC", "#FF0000"]
        BG = ["#010066", "#19B900"]
        KW = ["#333333", "#AAAAAA"]
        C3 = ["#ff7f00", "#19B900", "#0066CC"]
        C5 = ["#010066", "#19B900", "#333333", "#ff7f00", "#e41a1c"]
        return eval(name)





if __name__ == "__main__":
    df = pd.read_csv("https://raw.githubusercontent.com/yoriku/tmp_csv/main/kadai.csv")

    plot = PLOT()

    df = plot.convert(df, hue="target")
    color = plot.get_color("C3")

    plot.bar(df, "test", hue="target", color=color)

