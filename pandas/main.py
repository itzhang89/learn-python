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


def table_name_fm(sys_name: str, table_name: str, pre_ods: bool = False, db_name: str = None, schema_name: str = None):
    items = []
    items.append("pre_ods" if pre_ods else "ods")
    items.append(sys_name)
    if db_name:
        items.append(db_name)
    if schema_name:
        items.append(schema_name)
    items.append(table_name)
    full_table_name = "__".join(items)

    if full_table_name.find('$') != -1:
        full_table_name = '`' + full_table_name + '`'
    return full_table_name


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


isNullable = {'Y': True, 'N': False}

# oracle_to_hive = {
#     "varchar2": "varchar",
#     "number":
# }


def get_field_column_definition(series) -> str:
    column_name: str = str(series[COLUMN_NAME]).strip()
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

    is_nullable = "NOT NULL" if series[NULLABLE] else ""

    return '{column_name} {column_type} {constraint}'.format(column_name=column_name, column_type=column_type,
                                                             constraint=is_nullable)


if __name__ == '__main__':
    # pd.read_excel('tmp.xlsx', index_col=0)
    xlsx = "../ALL_TAB_COLS_202201171108.csv"
    # TABLE_NAME,COLUMN_NAME,DATA_TYPE,DATA_LENGTH,DATA_PRECISION,NULLABLE,CHARACTER_SET_NAME
    df: DataFrame = pd.read_csv(xlsx, header=0).drop(['CHARACTER_SET_NAME'], axis=1)
    df[NULLABLE] = df[NULLABLE].map(isNullable).astype(bool)

    #  select 21 table name
    selected_tables = ['FORECAST_SUMMARY', 'allotment$detail', 'Memberships', 'name_view', 'reservation_items',
                       'RESERVATION_DAILY_ELEMENT_NAME', 'RESERVATION_NAME', 'reservation_products', 'trx_routing_instructions',
                       'RESERVATION_SUMMARY', 'EXTERNAL_REFERENCES', 'RESERVATION_SUMMARY', 'FORECAST_SUMMARY',
                       'allotment$header', 'NAME', 'RESERVATION_DAILY_ELEMENTS', 'RESERVATION_DAILY_ELEMENT_NAME',
                       'RESERVATION_NAME', 'NAME_PHONE', 'RESERVATION_COMMENT', 'name_address', 'postal_codes_chain',
                       'name_address', 'postal_codes_chain']

    selected_tables = list(map(str.upper, selected_tables))
    print(selected_tables)

    df = df[df[TABLE_NAME].isin(selected_tables)]
    sql_df_groupby: DataFrameGroupBy = df.groupby(TABLE_NAME)

    for db_name, sub_df in sql_df_groupby:
        pd_column = sub_df.apply(get_field_column_definition, axis=1)
        ddl_string = create_table_ddl_fs("melco_opera",
                                         table_name_fm(sys_name='opera', db_name='operastaging', table_name=db_name),
                                         np.array(pd_column))
        with open("../target/{}.ddl.sql".format(str(db_name).lower()), 'w') as file:
            file.write(ddl_string)
