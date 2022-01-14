import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy


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


def get_field_column_definition(series) -> str:
    field_name: str = str(series["source_column_name"]).strip()
    if is_empty(field_name):
        return ''

    # generate data type
    column_type = str(series["column_type"]).strip()
    column_length = series["column_length"]
    dig_length = series["小数位数（sql server）"]
    data_type = column_type
    if column_type == 'nvarchar':
        if not is_empty(column_length):
            data_type = '{}({})'.format(column_type, column_length)
    elif column_type == 'bigint' or \
            column_type == 'decimal' or \
            column_type == 'float' or \
            column_type == 'int' or \
            column_type == 'numeric':
        if not is_empty(dig_length):
            data_type = '{}({})'.format(column_type, dig_length)

    # generate data constraints
    is_nullable = str(series["is_nullable"]).strip()
    constraint = "NOT NULL" if is_nullable == '1' else ""

    is_PK = str(series["is_PK"]).strip()
    if float(is_PK) == 1.0:
        constraint += " PRIMARY KEY"

    return '{field_name} {data_type} {constraint}'.format(field_name=field_name, data_type=data_type, constraint=constraint)


if __name__ == '__main__':
    # pd.read_excel('tmp.xlsx', index_col=0)
    xlsx = "../Melco_Opera.xlsx"
    df: DataFrame = pd.read_excel(xlsx, sheet_name="ODS", index_col=0)

    create_sql_df = pd.DataFrame(df,
                                 columns=['source_table_name', 'source_column_name', 'column_type', 'column_length',
                                          '小数位数（sql server）',
                                          'is_PK', 'is_nullable'])

    sql_df_groupby: DataFrameGroupBy = create_sql_df.groupby('source_table_name')

    for db_name, sub_df in sql_df_groupby:
        pd_column = sub_df.apply(get_field_column_definition, axis=1)
        print(create_table_ddl_fs("melco_opera", db_name, np.array(pd_column)))
