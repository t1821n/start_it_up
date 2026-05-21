import pydantic
from dotenv import load_dotenv
from typing import Annotated, List

from langgraph import graph
from langgraph.graph import StateGraph ,START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import  init_chat_model
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from web_operations import serp_search


load_dotenv()

llm_chat_model = init_chat_model("gpt-4o")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_ques: str | None
    google_res: str | None
    bing_res: str | None
    reddit_res: str | None
    selected_reddit_urls: list[str] | None
    reddit_post_data: list | None
    google_analysis: str | None
    bing_analysis: str | None
    reddit_analysis: str | None
    final_ans: str | None


def google_search(state: State):
    user_ques = state.get("user_ques", "")
    print(f"searching for google:{user_ques}")

    google_res = serp_search(user_ques, engine="google")
    print(google_res)

    return {"google_res": google_res}


def bing_search(state: State):
    user_ques = state.get("user_ques", "")
    print(f"searching for bing:{user_ques}")

    bing_res = serp_search(user_ques, engine="bing")
    print(bing_res)


    return {"bing_res": bing_res}


def reddit_search(state: State):
    user_ques = state.get("user_ques", "")
    print(f"searching for reddit:{user_ques}")

    reddit_res = []

    return {"reddit_res": reddit_res}


def analyse_reddit_posts(state: State):
    return {"analyse_reddit_res": []}


def retrieve_reddit_posts(state: State):
    return {"retrieve_reddit_posts": []}


def analyse_google_res(state: State):
    return {"google_analysis": ""}


def analyse_bing_res(state: State):
    return {"bing_analysis": ""}


def analyse_reddit_res(state: State):
    return {"reddit_analysis": ""}


def synthesize_analyses(state: State):
    return {"final_ans": ""}


#nodes
graph_builder = StateGraph(State)

graph_builder.add_node("google_search", google_search)
graph_builder.add_node("bing_search", bing_search)
graph_builder.add_node("reddit_search", reddit_search)
graph_builder.add_node("analyse_reddit_posts", analyse_reddit_posts)
graph_builder.add_node("retrieve_reddit_posts", retrieve_reddit_posts)
graph_builder.add_node("analyse_google_res", analyse_google_res)
graph_builder.add_node("analyse_bing_res", analyse_bing_res)
graph_builder.add_node("analyse_reddit_res", analyse_reddit_res)
graph_builder.add_node("synthesize_analyses", synthesize_analyses)


#edges connection
graph_builder.add_edge(START, "google_search")
graph_builder.add_edge(START, "bing_search")
graph_builder.add_edge(START, "reddit_search")

graph_builder.add_edge("google_search", "analyse_reddit_posts")
graph_builder.add_edge("bing_search", "analyse_reddit_posts")
graph_builder.add_edge("reddit_search", "analyse_reddit_posts")
graph_builder.add_edge("analyse_reddit_posts", "retrieve_reddit_posts")

graph_builder.add_edge("retrieve_reddit_posts", "analyse_google_res")
graph_builder.add_edge("retrieve_reddit_posts", "analyse_bing_res")
graph_builder.add_edge("analyse_google_res", "analyse_reddit_res")


graph_builder.add_edge("analyse_google_res", "synthesize_analyses")
graph_builder.add_edge("analyse_bing_res", "synthesize_analyses")
graph_builder.add_edge("analyse_reddit_res", "synthesize_analyses")

graph_builder.add_edge("synthesize_analyses", END)


graph = graph_builder.compile()

def run_chatbot():
    print("multi source research agent")
    print("type 'exit' to quite")

    while True:
        user_input = input("ask me anything:")
        if  user_input.lower() == "exit":
            print('happy analysis')
            break

        state = {
            "messages": [{"role": "user", "content": user_input}],
            "user_ques": user_input,
            "google_res": None,
            "bing_res": None,
            "reddit_res": None,
            "selected_reddit_urls": None,
            "reddit_post_data": None,
            "google_analysis": None,
            "bing_analysis": None,
            "reddit_analysis": None,
            "final_ans": None,
        }

        print("\n starting parallel research process")
        print("\n launching google, bing, reddit searches")

        final_state = graph.invoke(state)
        if final_state.get("final_ans"):
            print(f"\n final answer: {final_state['final_ans']}")

        print("-" * 80)


if __name__ == "__main__":
    run_chatbot()