import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy

NULLABLE = 'NULLABLE'

DATA_PRECISION = 'DATA_PRECISION'

DATA_LENGTH = 'DATA_LENGTH'

DATA_TYPE = 'DATA_TYPE'

COLUMN_NAME = 'COLUMN_NAME'

TABLE_NAME = 'TABLE_NAME'


def create_table_ddl_fs(db_name: str, table_name, fileds: list):
    fileds_str = ",".join(map(str.lower, fileds))
    return 'CREATE TABLE IF NOT EXISTS {}.{} ( {} ) PARTITIONED BY ( year string, month string, day string)'.format(
        db_name.lower(),
        table_name.lower(),
        fileds_str)


def is_empty(field) -> bool:
    if field is None:
        return True
    field = str(field).strip()
    if len(field) == 0:
        return True
    if field == 'null':
        return True
    return False


isNullable = {'Y': True, 'N': False}


def get_field_column_definition(series) -> str:
    column_name: str = str(series[COLUMN_NAME]).strip()
    if is_empty(column_name):
        return ''

    # generate data type
    column_type = str(series[DATA_TYPE]).strip()
    column_length = str(series[DATA_LENGTH]).strip()
    precision = str(series[DATA_PRECISION]).strip()
    if is_empty(precision):
        column_type = "{}({},{})".format(column_type, column_length, precision)
    else:
        column_type = "{}({})".format(column_type, column_length)

    is_nullable = "NOT NULL" if series[NULLABLE] else ""

    return '{column_name} {column_type} {constraint}'.format(column_name=column_name, column_type=column_type,
                                                             constraint=is_nullable)


if __name__ == '__main__':
    # pd.read_excel('tmp.xlsx', index_col=0)
    xlsx = "../ALL_TAB_COLS_202201171108.csv"
    # TABLE_NAME,COLUMN_NAME,DATA_TYPE,DATA_LENGTH,DATA_PRECISION,NULLABLE,CHARACTER_SET_NAME
    df: DataFrame = pd.read_csv(xlsx, header=0).drop(['CHARACTER_SET_NAME'], axis=1)
    df[NULLABLE] = df[NULLABLE].map(isNullable).astype(bool)

    print(df.info())
    sql_df_groupby: DataFrameGroupBy = df.groupby(TABLE_NAME)

    for db_name, sub_df in sql_df_groupby:
        pd_column = sub_df.apply(get_field_column_definition, axis=1)
        print(create_table_ddl_fs("melco_opera", db_name, np.array(pd_column)))
