def predict_score(total_hours, avg_productivity):
    base = 40
    hours_factor = 0.5
    productivity_factor = 0.3

    hours_contribution = total_hours * hours_factor
    productivity_contribution = avg_productivity * productivity_factor
    
    final_score = base + hours_contribution + productivity_contribution
    final_score = min(100, final_score) 

    return {
        "score": final_score,
        "base": base,
        "from_hours": hours_contribution,
        "from_productivity": productivity_contribution
    }
