import pandas as pd
import psycopg2
import streamlit as st
from sqlalchemy import create_engine

dbname = st.secrets["dbname"]
user = st.secrets["user"]
password = st.secrets["password"]
host = st.secrets["host"]
port =st.secrets["port"]


def insert_data_into_table(df, connection, engine, table_name, column_name):
    # Insert data into the specified table, checking for existing values first
    for value in df[column_name].unique():
        existing_data = pd.read_sql(f"SELECT {column_name}_id FROM {table_name} WHERE {column_name} = '{value}'",
                                    connection)
        if existing_data.empty:
            pd.DataFrame({column_name: [value]}).to_sql(table_name, engine, if_exists='append', index=False)
    # Get the id values for the specified table
    data_ids = pd.read_sql(f'SELECT {column_name}_id, {column_name} FROM {table_name}', connection)
    return data_ids


def upload_data_to_table(df):
    # Establish a connection to the database
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Create a cursor object using the connection
    engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(user, password, host, port, dbname))

    # Convert all header names to lowercase, fix postgres compatibility issues
    df.columns = df.columns.str.lower()
    # Remove commas and convert the 'mileage_run' column to integers
    df['mileage_run'] = df['mileage_run'].str.replace(',', '').astype(int)
    df['price'] = df['price'].str.replace(',', '').astype(int)
    df.rename(columns={'fuel_tank_capacity(l)': 'fuel_tank_capacity_l'}, inplace=True)
    df.rename(columns={'mileage(kmpl)': 'mileage_kmpl'}, inplace=True)
    df['mileage_kmpl'] = pd.to_numeric(df['mileage_kmpl'], errors='coerce')  # Convert to numeric, coerce errors to NaN

    df.rename(columns={'power(bhp)': 'power_bhp'}, inplace=True)
    df.rename(columns={'torque(nm)': 'torque_nm'}, inplace=True)
    df.rename(columns={'mileage(kmpl)': 'mileage_kmpl'}, inplace=True)
    df.rename(columns={'fuel_tank_capacity(l)': 'fuel_tank_capacity_l'}, inplace=True)
    df.rename(columns={'fuel_tank_capacity(l)': 'fuel_tank_capacity_l'}, inplace=True)

    # Insert data into table and return IDs
    make_ids = insert_data_into_table(df, connection, engine, 'manufacturer', 'make')
    body_type_ids = insert_data_into_table(df, connection, engine, 'body_type', 'body_type')
    fuel_type_ids = insert_data_into_table(df, connection, engine, 'fuel_type', 'fuel_type')
    transmission_type_ids = insert_data_into_table(df, connection, engine, 'transmission_type', 'transmission_type')
    transmission_ids = insert_data_into_table(df, connection, engine, 'transmission', 'transmission')
    emission_ids = insert_data_into_table(df, connection, engine, 'emission', 'emission')
    color_ids = insert_data_into_table(df, connection, engine, 'color', 'color')

    # Merge manufacturer DataFrame
    merged_data = pd.merge(df, make_ids, how='inner', left_on='make', right_on='make')
    merged_data.drop(columns=['make'], inplace=True)

    # Merge body_type DataFrame
    merged_data = pd.merge(merged_data, body_type_ids, how='inner', left_on='body_type', right_on='body_type')
    merged_data.drop(columns=['body_type'], inplace=True)

    # Merge fuel_type DataFrame
    merged_data = pd.merge(merged_data, fuel_type_ids, how='inner', left_on='fuel_type', right_on='fuel_type')
    merged_data.drop(columns=['fuel_type'], inplace=True)

    # Merge transmission_type DataFrame
    merged_data = pd.merge(merged_data, transmission_type_ids, how='inner', left_on='transmission_type',
                           right_on='transmission_type')
    merged_data.drop(columns=['transmission_type'], inplace=True)

    # Merge transmission DataFrame
    merged_data = pd.merge(merged_data, transmission_ids, how='inner', left_on='transmission', right_on='transmission')
    merged_data.drop(columns=['transmission'], inplace=True)

    # Merge emission DataFrame
    merged_data = pd.merge(merged_data, emission_ids, how='inner', left_on='emission', right_on='emission')
    merged_data.drop(columns=['emission'], inplace=True)

    # Merge color DataFrame
    merged_data = pd.merge(merged_data, color_ids, how='inner', left_on='color', right_on='color')
    merged_data.drop(columns=['color'], inplace=True)

    # Insert data into car table
    merged_data.to_sql('car', engine, if_exists='append', index=False)

    # Commit the transaction and close the connection
    connection.commit()
    connection.close()
