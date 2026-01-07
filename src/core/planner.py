from core.constraint_engine import check_constraints
from core.scoring import (
    compute_interest_score,
    compute_time_score,
    compute_distance_penalty,
    compute_final_score,
)


def plan_activity(
        city:str,
        activities:list[dict],
        user_interests:list[str],
        constraints:dict,
)->dict:
    allowed_activities=[]
    for activity in activities:
        allowed,_=check_constraints(
            activity_duration=activity['duration'],
            activity_cost=activity['cost'],
            activity_distance_km=activity['distance_km'],
            max_time=constraints['max_time'],
            max_budget=constraints['max_budget'],
            max_distance=constraints['max_distance'],
        )
        if allowed:
            interest_score=compute_interest_score(
                activity_tags=activity['tags'],
                user_interests=user_interests,
            )
            time_score=compute_time_score(
                activity_duration=activity['duration'],
                available_time=constraints['max_time'],
            )
            distance_penalty=compute_distance_penalty(
                distance_km=activity['distance_km'],
                max_distance=constraints['max_distance'],
            )
            final_score=compute_final_score(
                interest_score=interest_score,
                time_score=time_score,
                distance_penalty=distance_penalty,
            )
            score_data={
                'interest_score':interest_score,
                'time_score':time_score,
                'distance_penalty':distance_penalty,
            }
            allowed_activities.append({
                'activity':activity,
                'scores':score_data,
                'final_score':final_score,
            })
    allowed_activities.sort(
         key=lambda x: x["final_score"],
        reverse=True
        )
    if len(allowed_activities)==0:
        return {
        "city": city,
        "itinerary": [],
        "reason": "No activities satisfied the constraints.",
        }

    
    return {
        'city':city,
        'itinerary':allowed_activities 
    }

