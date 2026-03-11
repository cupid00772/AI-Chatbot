import os
import base64
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# 載入環境變數 (讀取 .env)
load_dotenv()

# 設定對話歷史的路徑 (資料夾)
HISTORY_DIR = "chat_histories"

def get_session_history(session_id: str):
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)
    file_path = os.path.join(HISTORY_DIR, f"{session_id}.json")
    return FileChatMessageHistory(file_path)

def encode_image(image_path: str) -> str:
    """將本地圖片轉碼為 base64 字串"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_text(file_path: str) -> tuple[str | None, str | None]:
    """讀取文件並回傳文字內容 (支援 txt, pdf 等)。回傳 (文本, 錯誤訊息)"""
    if not os.path.exists(file_path):
        return None, f"找不到檔案: {file_path}"
    if os.path.isdir(file_path):
        return None, f"「{file_path}」是一個資料夾，請提供完整的檔案名稱與副檔名。"
    
    ext = file_path.lower().split('.')[-1]
    if ext == 'pdf':
        try:
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            content = "\n".join([doc.page_content for doc in docs])
            return content, None
        except ImportError:
            return None, "尚未安裝 pypdf 套件，請執行 pip install pypdf"
        except Exception as e:
            return None, f"讀取 PDF 失敗: {e}"
    else:
        # 嘗試以純文字模式讀取
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read(), None
        except UnicodeDecodeError:
            try:
                # 針對 Windows 常見的編碼進行 fallback
                with open(file_path, "r", encoding="big5") as f:
                    return f.read(), None
            except Exception:
                return None, "無法將此檔案解析為純文字，可能是二進位檔或不支援的格式。"
        except Exception as e:
            return None, f"讀取檔案失敗: {e}"

def get_chat_chain(system_prompt: str = "你是一個有用的、友善的 AI 助手。"):
    """初始化並回傳包含歷史紀錄的 Chat Chain"""
    # 確認 API 金鑰存在
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("請確保 .env 檔案中包含 GEMINI_API_KEY 變數！")

    # 初始化 Gemini Chat Model (支援視覺的模型通常是 gemini-1.5-flash 或 gemini-1.5-pro)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # 建立 Prompt 範本，包含 system message 與對話歷史 (MessagesPlaceholder)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        MessagesPlaceholder(variable_name="input")
    ])

    # 將 prompt 與 llm 串接成一個 chain
    chain = prompt | llm

    # 將 chain 加上歷史訊息的處理邏輯
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    return chain_with_history


def main():
    try:
        chain_with_history = get_chat_chain()
    except ValueError as e:
        print(e)
        return

    print("=== Langchain + Gemini 多模態聊天機器人啟動 ===")
    print("輸入 'exit' 或 'quit' 關閉程式。")
    print("對話紀錄將儲存於 chat_histories 目錄的 JSON 檔案中。")
    print("若要傳送圖片，請使用指令： /image <圖片路徑> <你的提問>")
    print("若要讀取檔案，請使用指令： /file <文字/PDF檔案路徑> <你的提問>")
    print("=" * 60)

    # 這裡可以固定 session_id，或讓使用者輸入不同的 session_id
    session_id = "default_session"

    while True:
        try:
            user_input = input("\n你: ")
            if user_input.lower() in ['exit', 'quit']:
                print("掰掰！")
                break
            
            if not user_input.strip():
                continue

            # 判斷是否為傳送圖片的指令
            if user_input.startswith("/image "):
                parts = user_input.split(" ", 2)
                if len(parts) >= 3:
                    _, image_path, text_query = parts
                    image_path = image_path.strip().strip("'\"") # 移除可能的多餘引號
                    
                    if os.path.exists(image_path) and os.path.isdir(image_path):
                        print(f"錯誤：{image_path} 是一個資料夾。請提供圖片檔案的完整路徑！")
                        continue
                    if not os.path.exists(image_path):
                        print(f"找不到圖片檔案: {image_path}")
                        continue
                    
                    try:
                        base64_image = encode_image(image_path)
                    except Exception as e:
                        print(f"讀取圖片失敗: {e}")
                        continue
                    
                    from langchain_core.messages import HumanMessage
                    # 組合出包含文字與圖片的 list dict 結構
                    message_content = [
                        {"type": "text", "text": text_query},
                        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                    ]
                    payload = {"input": [HumanMessage(content=message_content)]}

                else:
                    print("格式錯誤。請使用: /image <圖片路徑> <提問>")
                    continue
                    
            elif user_input.startswith("/file "):
                parts = user_input.split(" ", 2)
                if len(parts) >= 3:
                    _, file_path, text_query = parts
                    file_path = file_path.strip().strip("'\"")
                    
                    content, err = extract_text(file_path)
                    if err:
                        print(f"檔案錯誤: {err}")
                        continue
                    
                    combined_query = f"以下是檔案提供給你的參考內容：\n\n{content}\n\n使用者提問：{text_query}"
                    payload = {"input": [HumanMessage(content=combined_query)]}
                else:
                    print("格式錯誤。請使用: /file <檔案路徑> <提問>")
                    continue
                    
            else:
                # 一般純文字輸入
                payload = {"input": [HumanMessage(content=user_input)]}


            # 使用 invoke 取得回應
            response = chain_with_history.invoke(
                payload,
                config={"configurable": {"session_id": session_id}}
            )

            print(f"AI: {response.content}")

        except KeyboardInterrupt:
            print("\n掰掰！")
            break
        except Exception as e:
            print(f"\n發生錯誤: {e}")

if __name__ == "__main__":
    main()


