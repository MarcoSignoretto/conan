from __future__ import annotations

import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy
from tabulate import tabulate


def dataframe(csv_path: str) -> DataFrame:
    """
    Load a dataframe from a CSV file and print the head of the file

    :param csv_path: the path of the CSV file
    :return: the pandas dataframe
    """

    df = pd.read_csv(csv_path)
    print(df.head().to_markdown())
    return df


def remove_outliers(df: DataFrame, labels: [str]) -> DataFrame:
    """
    Remove outliers from the dataframe based on quantiles

    :param df: original dataframe
    :param labels: columns used as groups
    :return: a new dataframe without outliers
    """
    df_low = df.quantile(0.01, numeric_only=True)
    df_high = df.quantile(0.99, numeric_only=True)
    df_filter = (df < df_high) & (df > df_low)

    cols = list(df.columns)
    for col in cols:
        if col in labels:
            df_filter[col] = True
    return df[df_filter]


def less_ttest_99(df: DataFrameGroupBy, metric: str, variantA: str, variantB: str):
    """
    T-test to verify that variant B reduces the metric respect to variant A

    :param df: the dataframe grouped by the variants
    :param metric: The metric under test
    :param variantA: The variant that is supposed to improve the metric
    :param variantB: The current metric
    :return:
    """
    from scipy.stats import ttest_ind

    agg_df = df.agg(list)

    # Verify that the mean of variantA is less than variantB
    t_stat, pvalue = ttest_ind(agg_df[metric][variantA], agg_df[metric][variantB], nan_policy='omit',
                               alternative='less', equal_var=False)

    print('H0: The new variant does not improve the metric respect to the current variant')
    print('H1: The new variant does IMPROVE the metric respect to the current variant')
    print('t-statistics:', t_stat,
          f'Inp-value: result = {pvalue:.6f}')
    if pvalue < 0.01:
        print(
            f'(Confidence 99%): Reject Null Hypothesis HO, the new variant "{variantA}" IMPROVES the metric {metric} respect to the current variant "{variantB}", ROLLING IT OUT!')
    elif pvalue >= 0.01:
        print(
            f'(Confidence 99%): Fail to reject Null Hypothesis H0, the new variant "{variantA}" does NOT improve the metric {metric} respect to the current variant "{variantB}"')


def study(df: DataFrame, group_by: [str], groups: [str], values: [str], hist_range: ([int] | None) = None):
    df = df.groupby(group_by)

    # block 1 - simple stats
    index = 0
    fig, axs = plt.subplots(2, 1, figsize=(15, 10))
    keys = values
    for key in keys:
        mean1 = df[key].mean()
        sum1 = df[key].sum()
        max1 = df[key].max()
        min1 = df[key].min()
        count1 = df[key].count()
        median1 = df[key].median()
        std1 = df[key].std()
        var1 = df[key].var()

        group_report = []
        for group in groups:

            #plot
            axs[index].hist(df.get_group(group)[key], color='blue', edgecolor='black', bins=100, range=hist_range)

            axs[index].set_xlabel(f'{key}')
            axs[index].set_ylabel('Occurences')
            axs[index].set_title(f'{group}')
            index = index + 1

            #report
            group_report.append(
                [group, mean1[group], median1[group], std1[group], str(var1[group]), max1[group], min1[group],
                 count1[group]], )

        print(f"=============={key}====================")
        print(
            tabulate(group_report,
                     headers=['data type', 'mean', 'median', 'std', 'var', 'max', 'min', 'count'],
                     tablefmt='pipe')
        )
        print()

    plt.show()
