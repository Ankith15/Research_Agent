from playwright.sync_api import sync_playwright
import re
from bs4 import BeautifulSoup
import requests
import json
import os
import serpapi
import wikipedia
from dotenv import load_dotenv
from langchain_core.tools import tool
import urllib
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# This function scrapes the data from the given URL using Playwright
def get_page_html(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")
            html = page.content()
            print("html we got is", html)
            browser.close()
            soup = BeautifulSoup(html, "html.parser")

            # Remove script and style elements
            for script_or_style in soup(["script", "style", "nostyle"]):
                script_or_style.decompose()

            structured_data = {
                "title": soup.title.string if soup.title else " No Title",
                "description": soup.find("meta", attrs={"name": "description"}).get("content", "") if soup.find("meta", attrs={"name": "description"}) else "No Description",
                "keyword": soup.find("meta", attrs={"name": "keywords"}).get("content", "") if soup.find("meta", attrs={"name": "keywords"}) else "No keywords",
                "headding": {
                    "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
                    "h2": [h.get_text(strip=True) for h in soup.find_all("h2")],
                    "h3": [h.get_text(strip=True) for h in soup.find_all("h3")]
                },
                "Paragraphs": [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)],
            }

            # Save structured data to a JSON file
            with open("info.json", "w", encoding="utf-8") as f:
                json.dump(structured_data, f)

            return structured_data
    except Exception as e:
        print("Error during web scraping:", e)

# This function fetches search results using SerpAPI
def serping(query):
    try:
        serp_key = os.getenv("SERP_API")
        client = serpapi.Client(api_key=serp_key)
        links = []
        result = client.search(
            q=query,
            engine="google",
            num=10
        )
        for item in result["organic_results"]:
            links.append(item['link'])
        return links
    except Exception as e:
        print("There is an error in SerpAPI call:", e)

# This tool integrates SerpAPI search + scraping to gather web info
@tool
def getting_the_info(query):
    "This is the combination of the serp api tool and the webscrapper"
    try:
        serper = serping(query)
        print(serper)
        web_information = {}
        num = 1
        for i in serper:
            try:
                print(num)
                res = get_page_html(i)
                web_information[i] = res
                print(f"result printed is\n {res}")
                num += 1
                if num == 5:
                    break
            except Exception as e:
                print("Error scraping:", i, e)
        print(web_information)
        return web_information
    except Exception as e:
        print("No data from serp api", e)

# This tool fetches summary data from Wikipedia
@tool
def wiki(query):
    "This is the wikipedia tool to get data from the wikipedia"
    Wiki_data = {}
    try:
        page = wikipedia.page(query)
        Wiki_data["title"] = page.title
        Wiki_data["url"] = page.url
        content = page.content
        content = re.sub(r'\n+', '\n', content) 
        content = re.sub(r'[ \t]+', ' ', content)
        content = re.sub(r'[{}\[\]<>]', '', content)
        content = re.sub(r'\\[a-z]+', '', content)
        content = '\n'.join([line for line in content.split('\n') if len(line.strip()) > 30])
        Wiki_data["content"] = content.strip()
        print(Wiki_data)
        return Wiki_data
    except Exception as e:
        print("The error is:", e)

# This tool pulls current news articles related to the query
@tool
def news_data(query):
    " This gets the current news from api's"
    try:
        apikey = os.getenv("CURRENT_API")
        encoded_query = urllib.parse.quote(query)
        url = f"https://gnews.io/api/v4/search?q={encoded_query}&lang=en&country=us&max=10&apikey={apikey}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            result = []

            for article in data.get("articles", []):
                result.append({
                    "title": article.get("title"),
                    "description": article.get("description")
                })
            return result
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print("News API error:", e)

# This tool uses Groq's LLaMA model to generate detailed academic-style reports
@tool
def generate_report(text: str):
    "This is the generative model powered by groq llama model to generate the report content"
    try:
        api_key = os.getenv("GROQ_API")
        prompt = """
        You are an AI Research Agent assigned to investigate specific tasks. Your objective is to gather accurate, reliable, and verifiable information related to the topics provided.

        - Do not fabricate or hallucinate any facts.
        - All responses must be grounded in genuine, credible sources.
        - Plagiarism is strictly prohibited—your answers should be original, well-articulated, and paraphrased in your own words.
        - Each response should demonstrate critical thinking, synthesis of knowledge, and comprehensive understanding of the subject matter.
        - The final report must be a minimum of two A4 pages in length, with clear headings, subheadings, and structured formatting to ensure readability.

        Proceed with diligence, objectivity, and academic integrity.
        """
        messages = [SystemMessage(content=prompt), HumanMessage(content=text)]
        llm = ChatGroq(model="llama-3.1-8b-instant", api_key=api_key)
        result = llm.invoke(messages)
        print(result)
        return result.content
    except Exception as e:
        print("Error generating report:", e)
