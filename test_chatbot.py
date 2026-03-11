import sys
from chatbot import get_chat_chain
chain_with_history = get_chat_chain()

def test():
    print("Testing chatbot...")
    session_id = "test_session_1"
    
    # Message 1
    input1 = "你好，我是小明"
    print(f"User: {input1}")
    res1 = chain_with_history.invoke(
        {"input": input1},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"AI: {res1.content}")
    
    # Message 2
    input2 = "我剛剛說我叫什麼名字？"
    print(f"User: {input2}")
    res2 = chain_with_history.invoke(
        {"input": input2},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"AI: {res2.content}")
    
    print("Test finished successfully!")

if __name__ == "__main__":
    test()
