import numpy as np
from plot import PLOT
import pandas as pd

if __name__ == "__main__":
    # iris dataset
    df = pd.read_csv("https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv")

    plot = PLOT(save_mode=["png"])

    df = plot.convert(df, hue="variety")
    color = plot.get_color("C3")

    plot.bar(df, "pic/bar", hue="variety", color=color)
    plot.box(df, "pic/box", hue="variety", color=color)
    plot.box(df, "pic/box-", hue="variety", color=color, kind="-")


    ave =np.array([[100,4],[10,200]])
    std =np.array([[0.3,1.2],[0.8,1.2]])
    classes = np.array([0,1])
    plot.confusion_matrix(ave, "pic/cm", std=std, classes=classes)

