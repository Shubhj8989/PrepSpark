import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import mysql.connector
import time

from db import get_connection
from analytics import calculate_productivity, calculate_streak, check_burnout, detect_weak_subject
from prediction import predict_score
from auth import authenticate_user, create_user

st.set_page_config(
    page_title="PrepSpark", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)


if 'user' not in st.session_state:
    st.session_state['user'] = None

if not st.session_state['user']:
    st.title("🔐 PrepSpark Login")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Login")
            
            if submit_login:
                user = authenticate_user(username, password)
                if user:
                    st.session_state['user'] = user
                    st.success(f"Welcome back, {user['name']}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    with tab2:
        with st.form("signup_form"):
            new_user = st.text_input("Username")
            new_name = st.text_input("Full Name")
            new_pass = st.text_input("Password", type="password")
            submit_signup = st.form_submit_button("Sign Up")
            
            if submit_signup:
                if create_user(new_user, new_pass, new_name):
                    st.success("Account created! Please login.")
                else:
                    st.error("Username already exists or error creating account.")
    
    st.stop()

user_id = st.session_state['user']['id']
user_name = st.session_state['user']['name']

with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #2c3e50; font-size: 3rem;'>🎓 PrepSpark</h1>", unsafe_allow_html=True)
    st.title(f"Hi, {user_name}! 👋")
    st.markdown("---")

    st.markdown("### 📌 Navigation")
    page = st.radio("Go to", ["Dashboard", "Log Session", "Predictions"])
    
    st.markdown("---")
    if st.button("Logout"):
        st.session_state['user'] = None
        st.rerun()
    
    st.caption("Developed by Shubh.dev")


if page == "Log Session":
    st.header("📝 Log Your Study Session")
    st.markdown("Keep track of your progress daily to build consistency.")

    with st.container():
        with st.form("study_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                study_date = st.date_input("📅 Date", date.today())
                subject = st.text_input("📚 Subject", placeholder="e.g. Mathematics")
                hours = st.number_input("⏳ Duration (Hours)", min_value=0.5, step=0.5)

            with col2:
                difficulty = st.selectbox("😰 Difficulty", ["Easy", "Medium", "Hard"])
                mood = st.selectbox("😊 Mood", ["Fresh", "Normal", "Tired"])
                notes = st.text_area("📝 Notes", placeholder="What did you cover today?")

            submitted = st.form_submit_button("Save Session")

            if submitted:
                if not subject:
                    st.warning("⚠️ Please enter a subject.")
                else:
                    try:
                        prod_score = calculate_productivity(hours, difficulty, mood)
                        conn = get_connection()
                        cursor = conn.cursor()
                        query = """
                            INSERT INTO study_sessions 
                            (study_date, subject, hours, difficulty, mood, notes, productivity, user_id) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        values = (study_date, subject, hours, difficulty, mood, notes, prod_score, user_id)
                        cursor.execute(query, values)
                        conn.commit()
                        conn.close()
                        st.success(f"✅ Session Saved! Productivity Score: {prod_score:.2f}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error saving session: {e}")

    st.divider()
    st.subheader("📋 Recent Sessions")

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM study_sessions WHERE user_id = %s ORDER BY id DESC LIMIT 5", (user_id,))
        sessions = cursor.fetchall()
        conn.close()

        if sessions:
            for session in sessions:
                with st.container():
                    
                    c1, c2, c3, c4 = st.columns([2, 4, 2, 1])
                    
                    with c1:
                        st.markdown(f"**📅 {session['study_date']}**")
                        st.caption(f"{session['mood']}")
                    
                    with c2:
                        st.markdown(f"**{session['subject']}**")
                        st.caption(f"{session['difficulty']} • {session['hours']} hrs")
                        if session['notes']:
                            st.text(session['notes'])
                            
                    with c3:
                        st.metric("Productivity", f"{session['productivity']:.1f}")

                    with c4:
                        if st.button("🗑️", key=f"del_{session['id']}", help="Delete this session"):
                            try:
                                conn = get_connection()
                                cursor = conn.cursor()
                                cursor.execute("DELETE FROM study_sessions WHERE id = %s AND user_id = %s", (session['id'], user_id))
                                conn.commit()
                                conn.close()
                                st.success("Deleted!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
                    
                    st.divider()
        else:
            st.info("No recent sessions found.")
            
    except Exception as e:
        st.error(f"Could not load history: {e}")

elif page == "Dashboard":
    st.header("📊 Analytics Dashboard")
    
    try:
        conn = get_connection()
        query = "SELECT * FROM study_sessions WHERE user_id = %s"
        df = pd.read_sql(query, conn, params=(user_id,))
        conn.close()

        if not df.empty:
            df['study_date'] = pd.to_datetime(df['study_date'])

            total_hours = df['hours'].sum()
            avg_productivity = df['productivity'].mean()
            current_streak = calculate_streak(df['study_date'].dt.date.tolist())
            is_burnout = check_burnout(df)
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Hours", f"{total_hours:.1f} hrs", "Cumulative")
            m2.metric("Avg Productivity", f"{avg_productivity:.1f}", "Score")
            m3.metric("Current Streak", f"{current_streak} days", "Keep it up!" if current_streak > 2 else "Start now")
            m4.metric("Burnout Risk", "High" if is_burnout else "Low", delta_color="inverse" if is_burnout else "normal")

            st.markdown("---")

            tab1, tab2 = st.tabs(["📈 Trends", "🧠 Subject Analysis"])
            
            with tab1:
                st.subheader("Daily Study Habits")
                daily_trend = df.groupby(df['study_date'].dt.date)['hours'].sum()
                
                fig, ax = plt.subplots(figsize=(10, 4))
                daily_trend.plot(kind='area', alpha=0.4, color='#4CAF50', ax=ax)
                daily_trend.plot(kind='line', marker='o', color='#2E7D32', ax=ax)
                ax.set_title("Hours Studied per Day")
                ax.set_ylabel("Hours")
                ax.grid(True, linestyle='--', alpha=0.3)
                st.pyplot(fig)

            with tab2:
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.subheader("Time Allocation")
                    subject_hours = df.groupby('subject')['hours'].sum()
                    st.bar_chart(subject_hours)
                
                with c2:
                    st.subheader("Weak Areas")
                    weak_subjects = detect_weak_subject(df)
                    if not weak_subjects.empty:
                        st.error(f"Need Focus: {', '.join(weak_subjects.index.tolist())}")
                        st.markdown("*These subjects have significantly lower study time than your average.*")
                    else:
                        st.success("🎉 You are maintaining a balanced study schedule!")

        else:
            st.info("👋 Welcome! Go to the 'Log Session' page to add your first study entry.")

    except Exception as e:
        st.error(f"Could not load analytics. Ensure database is running. Error: {e}")

elif page == "Predictions":
    st.header("🔮 Subject-wise Performance Forecaster")
    st.markdown("Estimate your potential exam score for each subject based on your study habits.")
    
    try:
        conn = get_connection()
        query = "SELECT * FROM study_sessions WHERE user_id = %s"
        df = pd.read_sql(query, conn, params=(user_id,))
        conn.close()
        
        if not df.empty:
            # Group by subject
            subjects = df['subject'].unique()
            
            # Create a grid layout
            cols = st.columns(2)
            
            for i, subject in enumerate(subjects):
                subject_data = df[df['subject'] == subject]
                
                total_hours = subject_data['hours'].sum()
                avg_productivity = subject_data['productivity'].mean()
                
                prediction = predict_score(total_hours, avg_productivity)
                score = prediction['score']
                
                # Use columns to create a card-like effect
                with cols[i % 2]:
                    
                    st.subheader(f"📘 {subject}")
                    st.metric("Predicted Score", f"{score:.1f} / 100", help=f"Base: {prediction['base']} + Hours: {prediction['from_hours']:.1f} + Eff: {prediction['from_productivity']:.1f}")
                    st.progress(int(score))
                    
                    if score < 60:
                        st.caption("⚠️ Needs more time/focus.")
                    elif score < 80:
                        st.caption("📈 Good, keep pushing!")
                    else:
                        st.caption("🌟 Excellent mastery!")
                    
                    st.divider()

            st.info("💡 Tip: hover over the score to see the breakdown.")

        else:
            st.warning("Not enough data to generate predictions. Log at least one session!")
    except Exception as e:
        st.error(f"Prediction Error: {e}")
