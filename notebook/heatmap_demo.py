import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

if __name__ == '__main__':
    np.random.seed(20190121)
    nSamples = 1000
    nCut = 10


    def zFunction(X):
        # z = x - y
        return X[:, 0] - X[:, 1]


    print('Generating Data')
    data = np.random.normal(size=(nSamples, 2))
    data = pd.DataFrame(data)
    data['z'] = zFunction(data.values)
    print(data.info())

    cuts = pd.DataFrame({str(feature) + 'Bin': pd.cut(data[feature], nCut) for feature in [0, 1]})
    print('at first cuts are pandas intervalindex.')
    print(cuts.head())
    print(cuts.info())

    means = data.join(cuts).groupby(list(cuts)).mean()
    means = means.unstack(level=0)  # Use level 0 to put 0Bin as columns.

    # Reverse the order of the rows as the heatmap will print from top to bottom.
    means = means.iloc[::-1]
    print(means.head())
    print(means['z'])
    plt.clf()
    sns.heatmap(means['z'])
    plt.title('Means of z vs Features 0 and 1')
    plt.tight_layout()
    plt.savefig('./means1.svg')

    plt.clf()
    sns.heatmap(means['z'], xticklabels=means['z'].columns.map(lambda x: x.left),
                yticklabels=means['z'].index.map(lambda x: x.left))
    plt.title('Means of z vs Features 0 and 1')
    plt.tight_layout()
    plt.savefig('./means2.svg')
