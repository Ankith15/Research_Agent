import os
from dotenv import load_dotenv
# from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import google.generativeai as genai
import json
from agent_caller import agent_invoke_tools
from combine import combined_output

load_dotenv()

import json

def extract_json(data: str):
    try:
        # Remove the '```json' and '```' Markdown code block markers and extra spaces
        json_str = data.strip().replace("```json", "").replace("```", "").strip()
        # sending the parsed text to json object
        final_result = json.loads(json_str)
        
        return final_result
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

def query_analyzer(query):
    api_key = os.getenv("GEMINI_API")
    genai.configure(api_key=api_key)
    
    prompt = f"""
    You are an intelligent query analyzer for a Research Agent system.

    Your task is to analyze the following user query:
    "{query}"

    You should call all the tools and you must decide what args should go to the following tools to be activated and fulfill this query.

    Here are the available tools:

    1. **serpapi_tool**  
    - Use when the query requires general web search results.  
    - Input: a complete sentence or question.  
    - Output: Top 5 URLs (to be scraped later).

    2. **wikipedia_tool**  
    - Use when the query is about a well-known topic suitable for Wikipedia.  
    - Input: a single **keyword** only (not a sentence).

    3. **current_news_tool**  
    - Use when the query involves **recent or trending topics**.  
    - Input: a short phrase or keyword related to the current topic.

    4. **generate_tool**  
    - Use when the query involves **reasoning, summarization, explanation, or open-ended tasks**.  
    - Powered by Groq's LLaMA model.  
    - Input: full sentence or detailed prompt.

    Your response must be a dictionary containing all the tools to invoke, formatted exactly like this:
    Note: Should not miss any of the tools to invoke. all the four tools should be invoked
    for example:
    ```json
    {{
    "functions": [
        {{
        "function_name": "current_news_tool",
        "function_args": "soil contamination"
        }},
        {{
        "function_name": "wikipedia_tool",
        "function_args": "soil pollution"
        }}
    ]
    }}
    ```

    """
    # initializing the gemini model
    llm = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-04-17")
    res = llm.generate_content(prompt)
    print("the result we have obtained is", res.text)
    # Ensure that the extracted JSON is in the correct format
    data = extract_json(res.text)
    
    
    
    result = {}
    if data:
        for function in data["functions"]:
            function_name = function["function_name"]
            function_args = function["function_args"]  
            result[function_name] = function_args
    print("the dict res is",result)
    result = agent_invoke_tools(result)
    # getting combined output
    result = combined_output(result)

    return result

