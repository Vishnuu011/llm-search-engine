import requests
import os
import arxiv
from dotenv import load_dotenv
from googleapiclient.discovery import build
from langchain.tools import tool
import yfinance as yf

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")



def google_search(queary: str) -> list[dict]:

    """Searches Google for the given query."""

    try:
        url = "https://google.serper.dev/search"
        payload = {
            "q":queary
        }
        headers = {
            "X-API-KEY": SERPER_API_KEY, 
            "Content-Type": "application/json"
        }
        res = requests.post(
            url=url,
            json=payload,
            headers=headers
        )
        results = res.json().get("organic", [])

        return [
            {"title": r["title"], "link": r["link"], "meta": r.get("snippet", "")}
            for r in results[:10]
        ]

    except Exception as e:
        print(f"[ERROR in google_search] : {e}")

       

def arxiv_search(query: str) -> list[dict]:

    """Searches ArXiv for the given query."""

    try:
        search = arxiv.Search(
            query=query, 
            max_results=5, 
            sort_by=arxiv.SortCriterion.Relevance
        )
        results = []
        for result in search.results():
            results.append({
                "title": result.title,
                "link": result.entry_id,
                "meta": ", ".join(a.name for a in result.authors)
            })
        return results   
        
    except Exception as e:
        print(f"[ERROR in arxiv_search] : {e}")


 

def youtube_search(query: str) -> list[dict]:

    """Searches youtube for the given query."""

    try:
        youtube = build(
            "youtube", 
            "v3", 
            developerKey=YOUTUBE_API_KEY
        )
        req = youtube.search().list(
            q=query, 
            part="snippet", 
            type="video", 
            maxResults=5
        )
        res = req.execute()
        return [
            {
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "channel": item["snippet"]["channelTitle"],
            }
            for item in res.get("items", [])
        ]       
    except Exception as e:
        print(f"[ERROR in youtubesearch] : {e}")




def get_stock_price(stock_symbol: str) -> str:

    """
    Retrieves the latest stock price and other relevant info for a given stock symbol using Yahoo Finance.

    Parameters:
        stock_symbol (str): The ticker symbol of the stock (e.g., AAPL, TSLA, MSFT, INFY.NS, TATASTEEL.NS).

    Returns:
        str: A summary of the stock's current price, daily change, and other key data.
    """
  
    try:
        stock = yf.Ticker(stock_symbol)
        info = stock.info

        current_price = info.get("regularMarketPrice")
        change = info.get("regularMarketChange")
        change_percent = info.get("regularMarketChangePercent")
        currency = info.get("currency", "USD")

        if current_price is None:
            return f"Could not fetch price for {stock_symbol}. Please check the symbol."

        return (
            f"Stock: {stock_symbol.upper()}\n"
            f"Price: {current_price} {currency}\n"
            f"Change: {change} ({round(change_percent, 2)}%)"
        )
    
    except Exception as e:
        print(f"[ERROR get_stock_price (tool)]: {e}")    


result = get_stock_price(stock_symbol="TATASTEEL.NS")
print(result)