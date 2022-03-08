import numpy as np
import pandas as pd
import glob
import os

from pandas import DataFrame

if __name__ == '__main__':
    # df = pd.read_excel(io='/Users/jinghui.zhang/coder/mine/2281/data/RESSET_STKSH2020_600495_600718_5_2.xls', engine='openpyxl',
    #                    dtype={'观测序号_Nobs': np.int32, '代码_Code': np.int32, '证券名称_Secunm': str, '行情日期_Qdate': str, '标准时间_StdTime':
    #                           str, '期间累计成交量(股)_TVolume_accu1': str, '期间收益率_Ret_Min': float})
    # print(df.head(10))

    df: DataFrame = pd.DataFrame()
    for path in glob.glob("/Users/jinghui.zhang/coder/mine/2281/data/*.csv"):
        print(f'{path}')

        csv_df = pd.read_csv(path, dtype={'观测序号_Nobs': np.int32, '代码_Code': np.int32, '证券名称_Secunm': str, '行情日期_Qdate': str,
                                          '标准时间_StdTime':
                                              str, '期间累计成交量(股)_TVolume_accu1': str, '期间收益率_Ret_Min': float})
        df = df.append(csv_df, ignore_index=True)

    print(df.head(5))
    # 观测序号_Nobs	代码_Code	证券名称_Secunm	行情日期_Qdate	标准时间_StdTime	期间累计成交量(股)_TVolume_accu1	期间收益率_Ret_Min
    liutong_df = pd.read_excel('/Users/jinghui.zhang/coder/mine/2281/流通股数.xlsx',
                               dtype={'日期': str, '股票代码': np.int32, '股票简称': str, '成交量': np.int32, '换手率': float, '流通股数': float})
    print(liutong_df.head(5))

    pd.merge(df, liutong_df, how='left', on=None, left_on=['行情日期_Qdate', '代码_Code'], right_on=['日期', '股票代码'],
             left_index=False, right_index=False, sort=True)
    df.rename()