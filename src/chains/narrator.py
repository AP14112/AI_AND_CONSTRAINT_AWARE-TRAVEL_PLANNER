from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config.config import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-120b",
    temperature=0.3,
)

SYSTEM_MESSAGE = (
    "You are an assistant that narrates a travel itinerary. "
    "You MUST follow the given order exactly. "
    "You MUST NOT add, remove, or reorder activities. "
    "You MUST NOT suggest alternatives."
)

USER_TEMPLATE = """
City: {city}

Fixed itinerary (DO NOT CHANGE ORDER):
{itinerary}

Write a friendly, concise day plan using bullet points.
Use natural transitions like 'Morning', 'Midday', 'Afternoon'.
Do not invent new places.
"""

PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE),
    ("user", USER_TEMPLATE),
])


def narrate_itinerary(city: str, itinerary: list[dict]) -> str:
    if not itinerary:
        return "No itinerary available to narrate."

    itinerary_text = "\n".join(
        f"- {item['activity']['name']} ({item['activity']['duration']} hrs)"
        for item in itinerary
    )

    response = llm.invoke(
        PROMPT.format_messages(
            city=city,
            itinerary=itinerary_text,
        )
    )

    return response.content
