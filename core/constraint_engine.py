def check_constraints(
    activity_duration: float,
    activity_cost: float,
    activity_distance_km: float,
    max_time: float,
    max_budget: float,
    max_distance: float,
) -> tuple[bool, list[str]]:
    violations=[]
    if activity_duration > max_time:
        violations.append("time limit exceeded.")
    if activity_cost > max_budget:
        violations.append(f"budget limit exceeded.")
    if activity_distance_km > max_distance:
        violations.append("Too much walking distance.")
    is_allowed = (len(violations) == 0)
    return is_allowed, violations

