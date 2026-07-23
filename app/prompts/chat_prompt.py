from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from app.parsers.output_parser import AI_OUTPUT_PARSER

format_instructions = AI_OUTPUT_PARSER.get_format_instructions()

CHAT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an experienced AI Backend Developer with over 10 years of experience.

            Be helpful, accurate, and professional.
            Provide clear, concise, and easy-to-understand answers.
            Return your response using the following format.

            {format_instructions}
            """,
        ),
        MessagesPlaceholder(
        variable_name="chat_history"
        ),
        ("human", "{question}")
    ]
)


