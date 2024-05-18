基本的に各列のデータがあるときは，`pd.melt()`関数を使用して，データの変換を行う必要がある  
（__name__内の例を参照）

## APIs

### 箱ひげ図
``` Python
plot_box(df, filename, title="", figsize=(10, 8), x="x", y="y", 
             hue=None, y_const=None, color=["#0066CC", "#FF0000"], 
             yticks=None, is_fitter=False, is_legend=False)
```
箱ひげ図を表示  

変数の意味（一部）  
- df (Required)：プロットするデータ
- filename (Required)：保存するファイル名（ex. test.png）
- x (option)：x軸の要素
- y (option)：y軸の要素
- hue (option)：群間を比較するときに，その指標となるもの（target={1,0}の列があるときは，targetを指定．例を参照）
- color (option)：BOXの色．hueがNoneの時は1つの色のコードを指定したリストを，それ以外はhueが持つ変数の数分の色のコードを指定したリスト指定する．デフォルトではhueの変数が2つの時の場合に使えるようになっている
- y_const (option)：基準となる横線を引くときに基準値の数値を指定
- yticks (option)：y軸のメモリのリストを指定（ex. [0,1,2]）
- is_fitter (option)：実際のメモリの点を描画する時はTrueを指定

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
