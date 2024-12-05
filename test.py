from plot import PLOT
import pandas as pd

if __name__ == "__main__":
    # iris dataset
    df = pd.read_csv("https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv")

    plot = PLOT()

    df = plot.convert(df, hue="variety")
    color = plot.get_color("C3")

    plot.bar(df, "bar", hue="variety", color=color)
    plot.box(df, "box", hue="variety", color=color)
    plot.box(df, "box-", hue="variety", color=color, kind="-")

