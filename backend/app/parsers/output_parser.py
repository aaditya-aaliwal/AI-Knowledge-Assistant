from langchain_core.output_parsers import PydanticOutputParser

from app.schemas.ai_output import AIResponseSchema


AI_OUTPUT_PARSER = PydanticOutputParser(
    pydantic_object=AIResponseSchema
)