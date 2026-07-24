from langchain_core.prompts import PromptTemplate


RAG_PROMPT = PromptTemplate(
    input_variables=[
        "context",
        "question",
    ],
    template="""
You are an AI Knowledge Assistant.

You must answer ONLY using the information provided in the context below.

Instructions:
- Use only the provided context to answer the question.
- Do not make up or assume information.
- If the answer is not present in the context, reply:
  "The requested information is not available in the uploaded documents."
- Keep your answer clear, accurate, and concise.

Context:
{context}

Question:
{question}

Answer:
""",
)