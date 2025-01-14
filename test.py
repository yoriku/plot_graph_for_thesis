import numpy as np
from plot import PLOT
import pandas as pd

if __name__ == "__main__":
    from sklearn.datasets import make_classification
    X, y= make_classification(n_samples=100, n_features=4, n_redundant=1, n_informative=3, n_classes=4, random_state=0)
    df = pd.DataFrame(X)
    df["target"] = y

    plot = PLOT(save_mode=["png"], figsize=(12,8), font_size=30)

    df = plot.convert(df, hue="target", x="features", y="number")
    color = plot.get_color("pastel")

    plot.box(df, "pic/adjust", x="features", y="number", hue="target", yticks=[-5,0,5], color=color)

    # iris dataset
    df = pd.read_csv("https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv")

    plot = PLOT(save_mode=["png"], figsize=(12,8))

    df = plot.convert(df, hue="variety")
    color = plot.get_color("C3")

    plot.bar(df, "pic/bar", hue="variety", color=color)
    plot.box(df, "pic/box", hue="variety", color=color, stats={"stat_name": "welch", "stat_mark": None}, figsize=(20,8))
    plot.box(df, "pic/box-", hue="variety", color=color, kind="-", figsize=(12,8))


    ave =np.array([[100,4],[10,200]])
    std =np.array([[0.3,1.2],[0.8,1.2]])
    classes = np.array([0,1])
    plot.confusion_matrix(ave, "pic/cm", std=std, classes=classes)

