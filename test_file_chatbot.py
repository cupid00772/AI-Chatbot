import sys
import os
from chatbot import extract_text, get_chat_chain
chain_with_history = get_chat_chain()

def test():
    print("Testing /file logic...")
    session_id = "test_session_2"
    
    file_path = r"C:\Users\cupid\Downloads\AI_Chatbot\test_doc.txt"
    query = "這份文件在說什麼？"
    
    print(f"User: /file {file_path} {query}")
    
    content, err = extract_text(file_path)
    if err:
        print(f"Error: {err}")
        return
        
    combined_query = f"以下是檔案提供給你的參考內容：\n\n{content}\n\n使用者提問：{query}"
    
    res = chain_with_history.invoke(
        {"input": combined_query},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"AI: {res.content}")
    

if __name__ == "__main__":
    test()
