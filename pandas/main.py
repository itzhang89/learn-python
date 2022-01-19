import re

import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy

PK = "PK"

NULLABLE = 'NULLABLE'

DATA_PRECISION = 'DATA_PRECISION'

DATA_LENGTH = 'DATA_LENGTH'

DATA_TYPE = 'DATA_TYPE'

COLUMN_NAME = 'COLUMN_NAME'

TABLE_NAME = 'TABLE_NAME'


def format_name(name: str):
    return name.join(['`', '`']) if name.find('$') != -1 else name


def create_table_ddl_fs(db_name: str, table_name, fileds: list):
    fileds_str = ",".join(map(str.lower, fileds))
    return 'CREATE TABLE IF NOT EXISTS {}.{} ( {} ) PARTITIONED BY ( year string, month string, day string)'.format(
        db_name.lower(),
        table_name.lower(),
        fileds_str)


def table_name_fm(sys_name: str, table_name: str, pre_ods: bool = False, db_name: str = None, schema_name: str = None):
    items = []
    items.append("pre_ods" if pre_ods else "ods")
    items.append(sys_name)
    if db_name:
        items.append(db_name)
    if schema_name:
        items.append(schema_name)
    items.append(table_name)
    return format_name("__".join(items))


def is_empty(field) -> bool:
    if field is None:
        return True
    field = str(field).strip()
    if len(field) == 0:
        return True
    if field == 'null':
        return True
    if field == 'nan':
        return True
    return False


isNullable = {'Y': True, 'N': False,
              '1': True, '0': False}

# re.sub(r"(\d.*?)\s(\d.*?)", r"\1 \2", string1)
oracle_to_hive: dict = {
    r"varchar2": r"varchar",
    r"date\(\d+\)": r"date",
    r"number\((\d+),(\d+)\)": r"decimal(\1,\2)",
    r"number\(22\)": r"int"
}


def get_field_column_definition(series) -> str:
    column_name: str = format_name(str(series[COLUMN_NAME]).strip())
    if is_empty(column_name):
        return ''

    # generate data type
    column_type = series[DATA_TYPE]
    column_length = series[DATA_LENGTH]
    precision = series[DATA_PRECISION]
    if is_empty(column_length):
        column_type = column_type
    elif is_empty(precision):
        column_type = "{}({})".format(column_type, round(column_length))
    else:
        column_type = "{}({},{})".format(column_type, round(column_length), round(precision))

    # 替换数据类型
    for r_key, r_val in oracle_to_hive.items():
        column_type = re.sub(r_key, r_val, column_type, flags=re.IGNORECASE)

    is_nullable = "" if series[NULLABLE] else "NOT NULL"

    return '{column_name} {column_type} {constraint}'.format(column_name=column_name, column_type=column_type,
                                                             constraint=is_nullable)


def read_yb_df() -> DataFrame:
    yb_xlsx = "../Melco_Opera.xlsx"
    yb_df: DataFrame = pd.read_excel(yb_xlsx, sheet_name="ODS", header=0, index_col=0)
    yb_df[NULLABLE] = yb_df["is_nullable"].map(lambda x: isNullable.get(x, False)).astype(bool)
    yb_df[PK] = yb_df["is_PK"].map(lambda x: isNullable.get(x, False)).astype(bool)
    yb_df[DATA_PRECISION] = yb_df["小数位数（sql server）"].map(lambda x: round(x) if str(x).isdigit() else x)
    yb_df[DATA_LENGTH] = yb_df["column_length"].map(lambda x: round(x) if str(x).isdigit() else x)
    return yb_df.rename(
        columns={"source_table_name": TABLE_NAME, "source_column_name": COLUMN_NAME, "column_type": DATA_TYPE},
        errors="raise")[[TABLE_NAME, COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, NULLABLE, PK]]


def read_hive_df() -> DataFrame:
    hive_csv = "../ALL_TAB_COLS_202201171108.csv"
    # TABLE_NAME,COLUMN_NAME,DATA_TYPE,DATA_LENGTH,DATA_PRECISION,NULLABLE,CHARACTER_SET_NAME
    df: DataFrame = pd.read_csv(hive_csv, header=0).drop(['CHARACTER_SET_NAME'], axis=1)
    df[NULLABLE] = df[NULLABLE].map(isNullable).astype(bool)
    return df


def create_ddl(df: DataFrame, *selected_columns):
    df = df[df[TABLE_NAME].isin(selected_columns)]
    sql_df_groupby: DataFrameGroupBy = df.groupby(TABLE_NAME)
    for tb_name, sub_df in sql_df_groupby:
        pd_column = sub_df.apply(get_field_column_definition, axis=1)
        ddl_string = create_table_ddl_fs("melco_opera",
                                         table_name_fm(sys_name='opera', db_name='operastaging', table_name=tb_name),
                                         np.array(pd_column))
        # with open("../target/{}.ddl.sql".format(str(tb_name).lower()), 'w') as file:
        #     file.write(ddl_string)


if __name__ == '__main__':
    yb_selected_tb = ['E_PMS_HIST_FORECAST_SUMMARY']
    yb_df = read_yb_df()
    yb_df = yb_df[yb_df[TABLE_NAME].isin(yb_selected_tb)]

    print(yb_df[[TABLE_NAME, COLUMN_NAME]])

    #  select 21 table name
    # hive_selected_tb = ['FORECAST_SUMMARY', 'allotment$detail', 'Memberships', 'name_view', 'reservation_items',
    #                    'RESERVATION_DAILY_ELEMENT_NAME', 'RESERVATION_NAME', 'reservation_products', 'trx_routing_instructions',
    #                    'RESERVATION_SUMMARY', 'EXTERNAL_REFERENCES', 'RESERVATION_SUMMARY', 'FORECAST_SUMMARY',
    #                    'allotment$header', 'NAME', 'RESERVATION_DAILY_ELEMENTS', 'RESERVATION_DAILY_ELEMENT_NAME',
    #                    'RESERVATION_NAME', 'NAME_PHONE', 'RESERVATION_COMMENT', 'name_address', 'postal_codes_chain',
    #                    'name_address', 'postal_codes_chain']

    hive_selected_tb = ['FORECAST_SUMMARY']
    hive_df: DataFrame = read_hive_df()

    hive_selected_tb = list(map(str.upper, hive_selected_tb))
    print(hive_selected_tb)

    create_ddl()
