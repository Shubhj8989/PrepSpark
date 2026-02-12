import pandas as pd

def calculate_productivity(hours, difficulty, mood):
    difficulty_weight = {
        "Easy": 1,
        "Medium": 1.5,
        "Hard": 2
    }

    mood_weight = {
        "Fresh": 1.2,
        "Normal": 1,
        "Tired": 0.7
    }

    d_w = difficulty_weight.get(difficulty, 1)
    m_w = mood_weight.get(mood, 1)

    return hours * d_w * m_w

def calculate_streak(dates):
    if not dates:
        return 0
        
    dates = sorted(set(dates))
    streak = 1
    max_streak = 1

    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1

    return max_streak

def check_burnout(df):
    if df.empty or len(df) < 5:
        return False

    df = df.sort_values('study_date')
    last_5 = df.tail(5)

    if len(last_5) < 5:
        return False

    avg_hours = last_5['hours'].mean()
    
    mood_map = {
        "Fresh": 3,
        "Normal": 2,
        "Tired": 1
    }
    
    mood_scores = last_5['mood'].map(mood_map)
    mood_score = mood_scores.mean()

    if avg_hours > 6 and mood_score < 2:
        return True

    return False

def detect_weak_subject(df):
    if df.empty:
        return pd.Series(dtype=float)
        
    subject_hours = df.groupby('subject')['hours'].sum()
    avg = subject_hours.mean()

    weak = subject_hours[subject_hours < avg * 0.6]

    return weak
