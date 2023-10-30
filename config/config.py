from psycopg2 import Error
import streamlit as st

from config.code import *


def explore_database(sql_query):
    results = []
    if len(sql_query) == 0:
        return []
    connection = None
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        # Create a cursor object using the connection
        with connection.cursor() as cursor:
            # Execute your SQL query
            cursor.execute(sql_query)
            # Fetch all results if there are any
            results = cursor.fetchall()

    except Error as e:
        st.sidebar.error(e)

    finally:
        # Close the cursor and connection
        if connection is not None:
            connection.commit()
            cursor.close()
            connection.close()

    return results


def read_and_display_csv_file(uploaded_file):
    st.caption('---')
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    # Display the uploaded data
    st.caption("### CSV FILE CONTENT:")
    st.write(df)
    return df


# Function to configure Streamlit page
def configure_page():
    st.set_page_config(
        page_title='🛺 DE 1.2',
        layout="wide",
        initial_sidebar_state="expanded")

    # Project title and description
    st.title('🛺 DE 1.2')
    st.caption('CAR TRADING DATA WAREHOUSE by Vytautas Pliadis')
    st.caption(
        'Turing College. Module 1: Introduction to Data Engineering. '
        'Sprint:2 Introduction to Relational Databases Practical Project')


def execute_query_ui():
    sql_query = st.sidebar.text_area('Write your SQL query:')
    if st.sidebar.button('EXECUTE QUERY', type='primary'):
        result = explore_database(sql_query)
        st.caption("### QUERY RESULT:")
        if len(result) > 0:
            st.dataframe(result)


def sidebar_cheatsheet():
    with st.sidebar:
        with st.expander('Frequently used queries'):
            st.write('SELECT * FROM car;')
            st.write('SELECT * FROM manufacturer;')
            st.write("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")


def file_uploader():
    # File uploader widget
    uploaded_file = st.file_uploader("Choose a CSV file:", type="csv")

    # Check if a file is uploaded
    if uploaded_file is not None:
        df = read_and_display_csv_file(uploaded_file)
        st.info('You can upload CSV file to a warehouse now')
        if st.button('UPLOAD', type='primary'):
            upload_data_to_table(df)
