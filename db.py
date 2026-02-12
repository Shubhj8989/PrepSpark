import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

import streamlit as st

def get_connection():
    # Try getting config from Streamlit secrets first (Cloud)
    if st.secrets:
        # Check if user pasted [secrets] section (nested dict)
        if "secrets" in st.secrets:
             config = st.secrets["secrets"]
        else:
             config = st.secrets
    # Fallback to environment variables (Local)
    else:
        config = os.environ

    try:
        return mysql.connector.connect(
            host=config.get("DB_HOST", "localhost"),
            user=config.get("DB_USER", "root"),
            password=config.get("DB_PASSWORD", ""),
            database=config.get("DB_NAME", "smart_study_analyzer"),
            port=int(config.get("DB_PORT", 3306))
        )
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            st.error("🚨 Deployment Error: Access denied. Please check your database username and password in Streamlit Secrets.")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            st.error("🚨 Deployment Error: Database does not exist. Please check your DB_NAME in Streamlit Secrets.")
        else:
            st.error(f"🚨 Connection Error: {err}. \n\n**Note for Deployment:** 'localhost' will NOT work on Streamlit Cloud. You must connect to a remote MySQL database (e.g., TiDB, AWS RDS, DigitalOcean).")
        st.stop()
