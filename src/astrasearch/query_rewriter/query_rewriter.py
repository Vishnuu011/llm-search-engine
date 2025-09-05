import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_core.runnables import RunnableSequence

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.pydantic_v1 import BaseModel, Field

from typing import Optional, List, Literal
from src.astrasearch.exception import SearchEngineException
import sys

load_dotenv()


class StructuredQuery(BaseModel):

    query: str = Field(
        ...,
        description="Cleaned user query. Grammar fixed. If stock-related, use yfinance symbol."
    )



def query_rewriter_agent(model_name: str, temperature: float | int ) -> Optional[RunnableSequence]:

    try:
        system_prompt = system_prompt = """You are a query refiner and normalizer.

        Your tasks:
        1. Take the user's raw query and rewrite it into a clean, well-structured query.
           - Fix grammar mistakes.
           - Remove unnecessary words.
           - Make it concise and clear.                

        2. If the query is related to the stock market:
           - Identify the company name or ticker symbol.
           - If the company is Indian (NSE), append `.NS` to the symbol.
             Example: "TCS stock market analysis" → "TCS.NS"
                      "Reliance stock price today" → "RELIANCE.NS"
           - Otherwise, use the correct Yahoo Finance symbol (e.g., Apple → AAPL).        

        3. Return only the cleaned query as structured JSON.
        """

        llm = ChatGroq(
            model=model_name,
            temperature=temperature
        )

        structuredllm = llm.with_structured_output(
            StructuredQuery
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{user_input}")
        ])

        chain = (
            prompt
            | structuredllm
        )

        return chain
    except Exception as e:
        raise SearchEngineException(e, sys)
