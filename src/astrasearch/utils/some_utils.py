from langchain.schema import AIMessage

def get_final_answer(result) -> str:
    """
    Extract the final AIMessage content from a LangGraph app.invoke result.
    Works when result['messages'] contains LangChain message objects.
    """
    messages = result.get("messages", [])
    ai_messages = [m for m in messages if isinstance(m, AIMessage)]
    return ai_messages[-1].content if ai_messages else ""