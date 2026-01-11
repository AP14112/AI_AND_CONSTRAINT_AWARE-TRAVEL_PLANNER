def compute_interest_score(activity_tags:list[str],user_interests:list[str])->float:
    if not activity_tags or not user_interests:
        return 0.0
    matched_tags = set(activity_tags).intersection(set(user_interests))
    return len(matched_tags) / len(activity_tags)

def compute_distance_penalty(distance_km:float,max_distance:float)->float:
    if distance_km<=0 or max_distance<=0:
        return 0.0
    penalty=min(distance_km / max_distance,1.0)
    return penalty

def compute_time_score(
    activity_duration: float,
    available_time: float,
) -> float:
    if activity_duration <= 0 or available_time <= 0:
        return 0.0

    ratio = activity_duration / available_time
    score=1-ratio
    if score<0:
        return 0.0
    if score>1:
        return 1.0
    return score



def compute_final_score(
    interest_score: float,
    time_score: float,
    distance_penalty: float,
    w_interest: float = 0.5,
    w_time: float = 0.3,
    w_distance: float = 0.2,
) -> float:
    return (
        w_interest * interest_score
        + w_time * time_score
        - w_distance * distance_penalty
    )
