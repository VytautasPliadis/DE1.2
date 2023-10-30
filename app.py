from config.config import *

configure_page()


# Function to define page navigation
def page_navigation():
    pages = ["Home", "Upload CSV", "Explore database"]
    selected_page = st.sidebar.radio("NAVIGATION:", pages)
    return selected_page


# Home page content
def home():
    st.caption("## Project overview")
    st.write(
        "This Streamlit web application designed to set up a data warehouse for a car trading startup. The application"
        " allows users to upload CSV files, execute SQL queries, and explore the database. It is intended to serve as "
        "a tool for data analysts to run ad-hoc queries on the available data, facilitating data-driven decision-making"
        "for the startup's launch in the Indian market.")
    st.write("Infrastructure: Postgres (15.1.0.130) on AWS (eu-central-1)")
    st.caption("## Schema")
    st.image('img/ERD.JPG')


# Upload page content
def upload_csv():
    st.caption("## Upload a CSV file")
    file_uploader()


# Explore page content
def explore():
    st.caption("## Explore a database")
    execute_query_ui()


# Main function to run the app
def main():
    selected_page = page_navigation()
    if selected_page == "Home":
        home()
    elif selected_page == "Upload CSV":
        upload_csv()
    elif selected_page == "Explore database":
        explore()
        sidebar_cheatsheet()


# Run the app
if __name__ == "__main__":
    main()
