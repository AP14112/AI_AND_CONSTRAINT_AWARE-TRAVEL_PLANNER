import streamlit as st

from core.planner import plan_activity
from chains.narrator import narrate_itinerary
from chains.explainer import explain_itinerary

st.set_page_config(
    page_title="AI Travel Planner",
    layout="centered",
)

st.title(" AI Travel Planner")
st.caption("Constraint-aware & Explainable")


# Activity Metadata Resolver (SYSTEM-OWNED)

ACTIVITY_PROFILES = {
    "museum": {
        "duration": 2.0,
        "cost": 300,
        "tags": ["culture", "history"],
    },
    "food": {
        "duration": 2.0,
        "cost": 400,
        "tags": ["food", "local"],
    },
    "nature": {
        "duration": 2.5,
        "cost": 0,
        "tags": ["nature", "relaxing"],
    },
    "shopping": {
        "duration": 2.0,
        "cost": 600,
        "tags": ["shopping"],
    },
    "culture": {
        "duration": 1.5,
        "cost": 200,
        "tags": ["culture"],
    },
}

def build_activity(name: str, category: str) -> dict:
    profile = ACTIVITY_PROFILES[category]
    return {
        "name": name,
        "duration": profile["duration"],
        "cost": profile["cost"],
        "distance_km": 3.0, #proxy value
        "tags": profile["tags"],
    }


st.sidebar.header("Constraints")

city = st.sidebar.text_input("City", value="Delhi")

max_time = st.sidebar.slider("Max time per day (hours)", 1, 12, 8)
max_budget = st.sidebar.number_input("Max budget per day", min_value=0, value=3000)
max_distance = st.sidebar.slider("Max walking distance (km)", 1, 20, 7)

constraints = {
    "max_time": float(max_time),
    "max_budget": float(max_budget),
    "max_distance": float(max_distance),
}

user_interests = st.sidebar.multiselect(
    "Your interests",
    ["culture", "history", "food", "nature", "shopping"],
    default=["culture", "history"],
)
# User-added Activities
st.subheader("➕ Add Activities")

if "activities" not in st.session_state:
    st.session_state.activities = []

with st.form("add_activity_form", clear_on_submit=True):
    activity_name = st.text_input("Activity name")
    category = st.selectbox(
        "Category",
        list(ACTIVITY_PROFILES.keys()),
    )
    submitted = st.form_submit_button("Add activity")

    if submitted and activity_name:
        st.session_state.activities.append(
            build_activity(activity_name, category)
        )

# Display added activities
if st.session_state.activities:
    st.markdown("### 📋 Activities Added")
    for i, act in enumerate(st.session_state.activities, start=1):
        st.write(
            f"{i}. **{act['name']}** "
            f"({', '.join(act['tags'])}, {act['duration']} hrs)"
        )
# Run Planner
st.divider()

if st.button("Create Constraint-Aware Itinerary"):
    result = plan_activity(
        city=city,
        activities=st.session_state.activities,
        user_interests=user_interests,
        constraints=constraints,
    )

    st.divider()

    itinerary = result["itinerary"]

    if not itinerary:
        st.error(result["reason"])
    else:

        # Planned Itinerary

        st.subheader("🧭 Planned Itinerary")

        for idx, item in enumerate(itinerary, start=1):
            act = item["activity"]
            st.write(
                f"**{idx}. {act['name']}** "
                f"({act['duration']} hrs · ₹{act['cost']})"
            )


        # Aggregate metrics for explanation

        avg_interest = sum(
            item["scores"]["interest_score"] for item in itinerary
        ) / len(itinerary)

        total_time = sum(
            item["activity"]["duration"] for item in itinerary
        )

        total_cost = sum(
            item["activity"]["cost"] for item in itinerary
        )


        # Itinerary-level Explanation

        explanation = explain_itinerary(
            city=city,
            num_activities=len(itinerary),
            avg_interest=avg_interest,
            total_time=total_time,
            total_cost=total_cost,
            constraints=[
                f"Daily time limit: {constraints['max_time']} hours",
                f"Budget limit: ₹{constraints['max_budget']}",
                f"Walking distance limit: {constraints['max_distance']} km",
            ],
        )

        st.subheader(" Why this itinerary?")
        st.write(explanation)


        # Narration 

        narration = narrate_itinerary(city, itinerary)

        st.subheader("✨ Your Day, Planned Out")
        st.write(narration)
