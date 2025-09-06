from src.astrasearch.tools.tools import youtube_search
from dotenv import load_dotenv

load_dotenv()

result = youtube_search(query="what is Differential Geometry ?")
print(result)