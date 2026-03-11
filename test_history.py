import os
from chatbot import get_chat_chain, get_session_history
from langchain_core.messages import HumanMessage

chain = get_chat_chain()
session_id = "test_memory_stream"

print("1. history before:", get_session_history(session_id).messages)

try:
    payload = {"input": [HumanMessage(content=[{"type": "text", "text": "我的名字是 Bob"}])]}
    response = ""
    for chunk in chain.stream(payload, config={"configurable": {"session_id": session_id}}):
        response += chunk.content

    print("1. history after:", get_session_history(session_id).messages)

    payload2 = {"input": [HumanMessage(content=[{"type": "text", "text": "我剛剛說我的名字是什麼？"}])]}
    response2 = ""
    for chunk in chain.stream(payload2, config={"configurable": {"session_id": session_id}}):
        response2 += chunk.content

    print("2. response:", response2)
    print("2. history after:", get_session_history(session_id).messages)
except Exception as e:
    import traceback
    traceback.print_exc()
