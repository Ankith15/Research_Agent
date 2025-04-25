from langchain_core.messages import HumanMessage, ToolMessage
from common import wiki, news_data, generate_report, getting_the_info
import urllib
import json


def agent_invoke_tools(tool_calls):
    """This is an Agent invoking tool"""
    result = {}

    for tool_name, tool_args in tool_calls.items():
        print("Tool name is:", tool_name)
        print("Arguments are:", tool_args)

        if tool_name == "wikipedia_tool":
            tool_output = wiki(tool_args)
        elif tool_name == "generate_tool":
            tool_output = generate_report(tool_args)
        elif tool_name == "current_news_tool":
            tool_output = news_data(tool_args)
        elif tool_name == "serpapi_tool":
            tool_output = getting_the_info(tool_args)
        else:
            print(f"Unknown tool: {tool_name}")
            continue  # Skip unknown tool calls

        result[tool_name] = tool_output
        with open('re.json', "w", encoding='utf-8') as f:
            json.dump(result, f, indent=4)

    return result
