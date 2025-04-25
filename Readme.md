
# AI Research Agent

The **AI Research Agent** is a web-based tool designed to gather, analyze, and compile research information from various sources using AI and multiple tools. The agent uses **Langchain**, **Playwright**, **Gemini**, **Groq**, and **Agentic AI** to extract and process data. The tool allows users to query about specific topics, retrieve relevant content, and generate research reports. The project is hosted on AWS EC2.

## Architecture
![_- visual selection](https://github.com/user-attachments/assets/0ae5d9ee-7932-4669-b016-237c9754cc91)


## Available Tools:
1. **serpapi_tool**  
   - Used for general web search results.  
   - Input: A complete sentence or question.  
   - Output: Top 5 URLs (to be scraped later).

2. **wikipedia_tool**  
   - Used when the query is about a well-known topic suitable for Wikipedia.  
   - Input: A single **keyword** only (not a sentence).

3. **current_news_tool**  
   - Used when the query involves **recent or trending topics**.  
   - Input: A short phrase or keyword related to the current topic.

4. **generate_tool**  
   - Used for **reasoning, summarization, explanation, or open-ended tasks**.  
   - Powered by Groq's LLaMA model.  
   - Input: Full sentence or detailed prompt.

5. **combined_output**  
   - Combines the results from all the tools and provides a comprehensive research report.

## Features:
- **Langchain Integration:** For orchestrating multiple tools.
- **Playwright Web Scraping:** Used to scrape information from web pages.
- **Groq LLaMA Model:** For generating research content based on prompts.
- **Gemini API:** Integrated for powerful AI responses.
- **Streamlit UI:** For easy interaction with the system via a web interface.
- **Cache System:** Frequently asked queries are stored in session state to enhance performance and reduce redundant queries.

## How it Works:
1. User inputs a query on the Streamlit UI.
2. The system processes the query using relevant tools (web search, Wikipedia, current news, etc.).
3. The results are combined and presented as a structured research report.
4. The report is generated with insights, key findings, and references.
5. The app is hosted on AWS EC2 and can be accessed via this link:
   - [AI Research Agent - Live on AWS EC2](http://13.60.48.129:8501/)

## Steps to Run Locally:
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd <repo_name>
   ```

2. Install the dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file with the necessary API keys:
   - **GEMINI_API_KEY**: For Gemini API access.
   - **GROQ_API_KEY**: For Groq API access.
   - **SERP_API_KEY**: For SerpAPI integration.
   - **CURRENT_API_KEY**: For news API.

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

