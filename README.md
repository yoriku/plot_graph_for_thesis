# 概要 Overview
直接論文やスライドに貼れるレベルの図を簡単に作成できるツール群  
A suite of tools that make it easy to create diagrams at a level that can be put directly on papers and slides.  


# APIs

## 基本的な使い方 Basic usage
``` Python
# インスタンス化 Instantiate
plot = PLOT(figsize=(10, 8), font_size=20, is_times_new_roman=False, save_mode=["png", "pdf"])

# 必要に応じてデータフレームを変形 Transform data frames as required.
df = plot.convert(df, hue="target")
# 必要に応じてカラーパレットを取得 Get a colour palette if necessary.
color = plot.get_color("KW")

# 図の作成 Create figure.
plot.box(df, "test", hue="target", color=color)
```

## サポートされる図一覧 Supported figures

### 箱ひげ図 Box plot
``` Python
box(df, filename, figsize=None, kind="|", 
    x="x", y="y", hue=None, y_const=None, zero_start=False, 
    color=["#0066CC", "#FF0000"], yticks=None, rotation=0)
```
箱ひげ図を表示  

変数の意味（一部）  
| 引数       | 必須/任意 | 説明                                                                                                                                                                                                                                                                                                                                                      |
| ---------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `df`       | 必須      | プロットするデータ<br>Data to be plotted                                                                                                                                                                                                                                                                                                                  |
| `filename` | 必須      | 保存するファイル名（例: `test`）<br>Filename for saving the plot (e.g., `test`)                                                                                                                                                                                                                                                                           |
| `kind`     | 任意      | `"                                                                                                                                                                                                                                                                                                                                                        | "` の時に縦向き，`"-"` の時に横向きの図を表示<br>Display vertical plot with `" | "`, horizontal plot with `"-"` |
| `x`        | 任意      | x軸の要素<br>Elements for the x-axis                                                                                                                                                                                                                                                                                                                      |
| `y`        | 任意      | y軸の要素<br>Elements for the y-axis                                                                                                                                                                                                                                                                                                                      |
| `hue`      | 任意      | 群間を比較するときにその指標となるもの（`target={1,0}` の列がある場合、`target` を指定。例を参照）<br>Indicator for group comparison (e.g., `target` with values `{1,0}`)                                                                                                                                                                                 |
| `color`    | 任意      | BOXの色。`hue=None` の時は1つの色コードを指定したリストを、`hue` が持つ変数の数分の色コードを指定したリストを渡す。デフォルトでは `hue=2` の場合に使用可能<br>Color of the box. If `hue=None`, provide a list of one color code. Otherwise, provide a list of color codes corresponding to the number of hue variables. By default, it works for `hue=2`. |
| `y_const`  | 任意      | 基準となる横線を引くときに基準値の数値を指定<br>Specify a numeric value for drawing a reference horizontal line                                                                                                                                                                                                                                           |
| `yticks`   | 任意      | y軸のメモリのリストを指定（例: `[0,1,2]`）<br>List of y-axis ticks (e.g., `[0,1,2]`)                                                                                                                                                                                                                                                                      |
| `rotation` | 任意      | X軸のメモリラベルの角度<br>Rotation angle for x-axis tick labels                                                                                                                                                                                                                                                                                          |


### 線グラフ
``` Python
plot_line(df, filename, title="", figsize=(10, 8), x="x", y="y", 
              hue=None, color=["#0066CC", "#FF0000"], 
              xticks=None, yticks=None, zero_start=False, is_legend=False)
```
線グラフを表示  

変数の意味（一部）  
- df (Required)：プロットするデータ
- filename (Required)：保存するファイル名（ex. test.png）
- x (option)：x軸の要素
- y (option)：y軸の要素
- hue (option)：群間を比較するときに，その指標となるもの（target={1,0}の列があるときは，targetを指定．例を参照）
- color (option)：Lineの色．hueがNoneの時は1つの色のコードを指定したリストを，それ以外はhueが持つ変数の数分の色のコードを指定したリスト指定する．デフォルトではhueの変数が2つの時の場合に使えるようになっている
- y_const (option)：基準となる横線を引くときに基準値の数値を指定
- xticks (option)：x軸のメモリのリストを指定（ex. [0,1,2]）
- yticks (option)：y軸のメモリのリストを指定（ex. [0,1,2]）
- zero_start (option)：y軸を0から始めたい時はTrueを指定

### 棒グラフ
``` Python
plot_bar(df, filename, title="", figsize=(10, 8), x="x", y="y", 
             hue=None, y_const=0, color=["#0066CC", "#FF0000"], 
             yticks=None, is_legend=False, zero_start=False):
```
棒グラフを表示  

変数の意味（一部）  
- df (Required)：プロットするデータ
- filename (Required)：保存するファイル名（ex. test.png）
- x (option)：x軸の要素
- y (option)：y軸の要素
- hue (option)：群間を比較するときに，その指標となるもの（target={1,0}の列があるときは，targetを指定．例を参照）
- color (option)：BARの色．hueがNoneの時は1つの色のコードを指定したリストを，それ以外はhueが持つ変数の数分の色のコードを指定したリスト指定する．デフォルトではhueの変数が2つの時の場合に使えるようになっている
- y_const (option)：基準となる横線を引くときに基準値の数値を指定
- yticks (option)：y軸のメモリのリストを指定（ex. [0,1,2]）
- zero_start (option)：y軸を0から始めたい時はTrueを指定
