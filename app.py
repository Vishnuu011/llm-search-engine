from flask import render_template, Flask, send_from_directory, request, jsonify
from src.astrasearch.query_rewriter.query_rewriter import query_rewriter_agent
import requests
from flask_cors import CORS
from src.astrasearch.tools.tools import google_search, youtube_search, arxiv_search
from src.astrasearch.agents.agent_workflow import CompliedGraphSupervisorWorkflow
from src.astrasearch.utils.some_utils import *
from langchain_core.messages import HumanMessage
import os

app = Flask(__name__, template_folder="template")
CORS(app)  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    raw_query = data.get("query")

    # Get rewriter runnable
    rewriter = query_rewriter_agent(
        model_name="llama-3.3-70b-versatile",
        temperature=0.7
    )

    # Run rewriter
    rewritten_result = rewriter.invoke(raw_query)

  
    if hasattr(rewritten_result, "query"):
        rewritten_query = rewritten_result.query
    else:
        rewritten_query = str(rewritten_result)

    # Supervisor
    agent = CompliedGraphSupervisorWorkflow()
    apps = agent.supervisor_worflow()

    result = apps.invoke({
        "messages": [HumanMessage(content=rewritten_query)]
    })
    final_answer = get_final_answer(result=result)

    google_results = google_search(rewritten_query)
    youtube_results = youtube_search(rewritten_query)
    arxiv_results = arxiv_search(rewritten_query)

    sources = google_results[:7] + arxiv_results[:2]

    return jsonify({
        "answer": final_answer,
        "sources": sources,
        "videos": youtube_results,
        "papers": arxiv_results
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)