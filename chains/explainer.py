from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config.config import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-120b",
    temperature=0.3,
)

SYSTEM = (
    "You explain why an itinerary was constructed. "
    "You do NOT plan, suggest alternatives, or change the itinerary."
)

USER = """
City: {city}

Itinerary summary:
- Number of activities: {num_activities}
- Average interest match: {avg_interest}
- Total time used: {total_time} hours
- Total cost: {total_cost}

User constraints:
{constraints}

Explain why this itinerary was selected in 2–3 sentences.
"""

PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("user", USER),
])

def explain_itinerary(
    city: str,
    num_activities: int,
    avg_interest: float,
    total_time: float,
    total_cost: float,
    constraints: list[str],
) -> str:
    response = llm.invoke(
        PROMPT.format_messages(
            city=city,
            num_activities=num_activities,
            avg_interest=round(avg_interest, 2),
            total_time=round(total_time, 1),
            total_cost=total_cost,
            constraints="\n".join(constraints),
        )
    )
    return response.content
