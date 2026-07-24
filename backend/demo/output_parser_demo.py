from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings
from app.schemas.ai_output import AIResponseSchema


parser = PydanticOutputParser(
    pydantic_object=AIResponseSchema
)

llm = ChatGoogleGenerativeAI(
    model=settings.GEMINI_MODEL,
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0,
)

prompt = PromptTemplate(
    template="""
Answer the question below.

{format_instructions}

Question:
{question}
""",
    input_variables=["question"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    },
)

chain = prompt | llm

if __name__ == "__main__":
    response = chain.invoke(
        {
            "question": "What is FastAPI?"
        }
    )

    print("========== RAW ==========")
    print(response.content)

    parsed = parser.parse(response.text())

    print("\n========== PARSED ==========")
    print(parsed)

    print("\nAnswer:", parsed.answer)
    print("Category:", parsed.category)
    print("Confidence:", parsed.confidence)