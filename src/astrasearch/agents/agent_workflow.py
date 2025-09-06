import os, sys

from dotenv import load_dotenv

from src.astrasearch.exception import SearchEngineException

from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph

from langgraph_supervisor import create_supervisor

from src.astrasearch.tools.tools import get_stock_price, google_search, arxiv_search, youtube_search

from langchain_groq import ChatGroq
from typing import Tuple, List,Optional, Any

load_dotenv()


class CompliedGraphSupervisorWorkflow:

    def __int__(self):

        pass

      

    def finance_react_agent(self) -> Optional[CompiledStateGraph]:

        try:
            model=ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.7
            )

            finance_agent = create_react_agent(
                model=model,
                tools=[get_stock_price],
                name="stock_market_expert",
                prompt=(  
                "You are a **stock market expert**.\n"
                "Your job is provide stock prices and financial info.\n"
                "using the `get_stock_price` tool.\n"
                "Always call the tool instead of guessing."   
                )
            )

            return finance_agent
        
        except Exception as e:

            raise SearchEngineException(e, sys)
        
    def search_engine_react_agent(self) -> Optional[CompiledStateGraph]:

        try:
            model=ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.7
            )

            search_engine_agent = create_react_agent(
                model=model,
                tools=[google_search],
                name="search_engine_expert",
                prompt=(
                "You are acting as a **Google Search engine**.\n\n"

                "### Rules:\n"
                "- Always use the `google_search` tool for every query. Never answer from memory.\n"
                "- Use only **one tool call per query**.\n"
                "- After retrieving results, rewrite them into a clear, factual response in **Markdown format**.\n"
                "- Never add personal opinions or speculation—stick strictly to the retrieved information.\n"
                "- Never expose your internal reasoning or steps.\n\n"

                "### Output Format:\n"
                "1. **Summary (2–4 paragraphs):**\n"
                "   - Provide a concise but informative overview of the search results.\n"
                "   - Highlight the most important points clearly.\n\n"
                "2. **Top Results:**\n"
                "   - Present the retrieved search results as a bullet list with title + link.\n\n"
                "### Example Output:\n"
                "### Summary\n"
                "Paragraph 1 …\n"
                "Paragraph 2 …\n\n"
                "### Top Results\n"
                "- [Title 1](link)\n"
                "- [Title 2](link)\n"
                "- [Title 3](link)\n\n"

                "⚠️ IMPORTANT: Your final output must look like a **Google Search results page** in Markdown. "
                "Do not include anything outside of this format."
                )
            )

            return search_engine_agent
        
        except Exception as e:
            raise SearchEngineException(e, sys)    
        
    def research_arxiv_react_agent(self) -> Optional[CompiledStateGraph]:

        try:
            model=ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.7
            )

            arxiv_search_agent = create_react_agent(
                model=model,
                tools=[arxiv_search],
                name="research_expert",
                prompt=(
                "You are a world-class research assistant with access to arXiv. "
                "Always use the arXiv search tool to gather relevant research papers and insights. "
                "Do not use web search engines. "
                "After retrieving the results, write the final answer in **Markdown format**:\n\n"
                "### Explanation\n"
                "- Provide a detailed explanation in **3–7 paragraphs**.\n"
                "- Use Markdown headings, bullet points, or bold text when appropriate.\n\n"
                "### Sources\n"
                "- List all source links clearly as bullet points.\n\n"
                "Do not include anything outside of Markdown formatting."
                )
            )

            return arxiv_search_agent
        
        except Exception as e:
            raise SearchEngineException(e, sys)    
        

    def supervisor_worflow(self) -> Optional[CompiledStateGraph]:

        try:
            model=ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.7
            )

            workflow = create_supervisor(
                agents=[
                    self.search_engine_react_agent(),
                    self.research_arxiv_react_agent(),
                    self.finance_react_agent()
                ],
                model=model,
                prompt=(
                    "You are a **strict supervisor** coordinating two expert agents:\n\n"
                    "- **search_engine_expert** → Responsible for current and recent events. Must always use Google Search.\n"
                    "- **research_expert** → Responsible for academic and research topics. Must always use arXiv.\n\n"

                    "### Your Responsibilities\n"
                    "1. **Routing**: Decide which expert is best suited for the user’s query and send the query ONLY to that expert.\n"
                    "2. **Rewriting**: When the expert provides a response, you must ALWAYS rewrite it into a final answer.\n"
                    "   - Do not copy or pass the expert’s text directly.\n"
                    "   - Do not shorten excessively—expand into a **comprehensive Markdown explanation**.\n"
                    "   - Your rewritten output must be between **3–7 paragraphs**.\n"
                    "3. **Content Rules**:\n"
                    "   - Keep all important points and insights from the expert.\n"
                    "   - Present the information in clear, well-structured **Markdown format**.\n"
                    "   - Use `###` headings and bullet points where appropriate.\n"
                    "   - Never invent or add new information beyond what the expert provided.\n"
                    "   - Always include a `### Sources` section at the end with the exact source links the expert provided.\n\n"

                    "### Output Format (Strictly Follow)\n"
                    "Your final answer must strictly follow this structure:\n\n"
                    "### Explanation\n"
                    "- Write a clear and factual explanation expanded into **3–7 paragraphs**.\n"
                    "- Use Markdown headings, bullet points, or bold text when helpful.\n\n"
                    "### Sources\n"
                    "- List all sources as bullet points exactly as given by the expert.\n\n"

                    "⚠️ IMPORTANT: Never return the expert’s response as-is. Always rewrite it into a polished Markdown summary following the format above."
                )
            )

            app = workflow.compile()

            return app

        except Exception as e:
            raise SearchEngineException(e, sys)    
        
        