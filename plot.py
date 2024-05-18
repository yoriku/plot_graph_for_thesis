import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_box(df, filename, title="", figsize=(10, 8), x="x", y="y", 
             hue=None, y_const=None, color=["#0066CC", "#FF0000"], 
             yticks=None, is_fitter=False, is_legend=False):
    for _ in range(2):
        fig = plt.figure(figsize=figsize, dpi=100)
        ax = fig.add_subplot(111)
        plt.rcParams["mathtext.fontset"] = "stix"  # stixフォントにする
        # plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 20
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
        PROPS = {
        'boxprops': {'edgecolor': 'black'},
        'medianprops': {'color': 'black'},
        'whiskerprops': {'color': 'black'},
        'capprops': {'color': 'black'}
        }
        if y_const is not None:
            ax.axhline(y=y_const, c="b", linewidth=3)

        g = sns.boxplot(x=x, y=y, data=df, hue=hue, ax=ax, linewidth=2, width=0.8,
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
        if is_fitter:
            sns.stripplot(x=x, y=y, data=df, hue=hue, dodge=True, jitter=True, palette='dark:black', ax=ax)
                                
        g.set_title(title)
        if hue is not None and not is_legend:
            ax.get_legend().remove()
        ax.tick_params(bottom=False)
        if yticks is None:
            y_min, y_max = ax.get_ylim()
            ax.set_ylim(y_min, y_max)
        else:
            ax.set_yticks(yticks)
            ax.set_ylim(yticks[0], yticks[-1])

        sns.set_palette(color)
        sns.despine()

        # os.makedirs("pics4slide_ignore_small_data", exist_ok=True)
        plt.savefig(filename)
        plt.savefig(f"{filename}.pdf")
        plt.close()


def plot_line(df, filename, title="", figsize=(10, 8), x="x", y="y", 
              hue=None, color=["#0066CC", "#FF0000"], 
              xticks=None, yticks=None, zero_start=False, is_legend=False):
    for _ in range(2):
        fig = plt.figure(figsize=figsize, dpi=100)
        ax = fig.add_subplot(111)
        plt.rcParams["mathtext.fontset"] = "stix"  # stixフォントにする
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 20
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

        g = sns.lineplot(x=x, y=y, data=df, hue=hue, ax=ax, linewidth=3)
        g.set_title(title)
        if hue is not None and not is_legend:
            ax.get_legend().remove()
        # ax.tick_params(bottom=False)
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
        sns.set_palette(color)
        sns.despine()
        plt.savefig(filename)
        plt.savefig(f"{filename}.pdf")
        plt.close()


def plot_bar(df, filename, title="", figsize=(10, 8), x="x", y="y", 
             hue=None, y_const=0, color=["#0066CC", "#FF0000"], 
             yticks=None, is_legend=False, zero_start=False):
    for _ in range(2):
        fig = plt.figure(figsize=figsize, dpi=100)
        ax = fig.add_subplot(111)
        plt.rcParams["mathtext.fontset"] = "stix"  # stixフォントにする
        # plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 20
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
        PROPS = {
        'err': {'color': 'black'},
        }
        if y_const is not None:
            ax.axhline(y=y_const, c="b", linewidth=3)

        g = sns.barplot(x=x, y=y, data=df, hue=hue, ax=ax, linewidth=2, 
                        width=0.8, err_kws={'color': 'black'}, edgecolor="black")
                                
        g.set_title(title)
        if hue is not None and not is_legend:
            ax.get_legend().remove()
        ax.tick_params(bottom=False)
        if yticks is None:
            y_min, y_max = ax.get_ylim()
            if zero_start:
                y_min = 0
            ax.set_ylim(y_min, y_max)
        else:
            ax.set_yticks(yticks)
            ax.set_ylim(yticks[0], yticks[-1])

        sns.set_palette(color)
        sns.despine()

        # os.makedirs("pics4slide_ignore_small_data", exist_ok=True)
        plt.savefig(filename)
        plt.savefig(f"{filename}.pdf")
        plt.close()

if __name__ == "__main__":
    df = pd.read_csv("https://raw.githubusercontent.com/yoriku/tmp_csv/main/kadai.csv")
    df = pd.melt(df, id_vars="target", var_name="x", value_name="y")
    plot_bar(df, "test_bar.png", hue="target")
    plot_box(df, "test_box.png", hue="target")