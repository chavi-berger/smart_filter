def analyze_candidate_decision(initial_score, chat_score, response_time):
    """
    מנוע קבלת החלטות חכם עבור גיוס לחברת ביטוח.
    קלט: ציון סינון (בת 1), ציון צ'אט (בת 2), זמן תגובה בדקות.
    """

    # 1. חישוב ציון משוקלל (צ'אט שווה יותר כי זו אינטראקציה אקטיבית)
    weighted_score = (initial_score * 0.4) + (chat_score * 0.6)

    # 2. ניתוח חריגות (Anomaly Detection)
    # אם יש פער ענק בין הסינון לצ'אט - זה דגל צהוב (מצריך בדיקה אנושית)
    score_gap = abs(initial_score - chat_score)
    needs_manual_review = score_gap > 40

    # 3. פקטור זמן תגובה (Critical for Service)
    # בשירות לקוחות, מהירות היא הכל.
    time_penalty = 0
    if response_time > 1440:  # מעל יום (24 שעות)
        time_penalty = 15
    elif response_time > 480:  # מעל 8 שעות
        time_penalty = 5

    final_score = weighted_score - time_penalty

    # 4. קבלת החלטה סופית (Logic Gate)
    if final_score >= 80 and not needs_manual_review:
        status = "✅ High Priority"
        action = "Send Calendar Link"
    elif final_score >= 65 or needs_manual_review:
        status = "🟡 Manual Review"
        action = "HR Specialist Review"
    else:
        status = "❌ Rejected"
        action = "Send Rejection Email"

    # 5. פלט מובנה ל-Dashboard
    return {
        "final_score": round(final_score, 2),
        "status": status,
        "next_step": action,
        "insights": {
            "score_gap": score_gap,
            "speed_penalty": time_penalty,
            "was_fast_responder": response_time < 60
        }
    }
