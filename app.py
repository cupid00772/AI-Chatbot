import gradio as gr
from chatbot import get_chat_chain, extract_text, encode_image
from google.api_core.exceptions import ResourceExhausted
import os

def respond(message, history, session_id: str, system_prompt: str):
    # Initial yield
    yield history, ""
    
    try:
        # 動態建立（或復用）特定的聊天鏈
        chain_with_history = get_chat_chain(system_prompt=system_prompt)
    except ValueError as val_err:
        history.append({"role": "user", "content": message["text"] if isinstance(message, dict) else message})
        history.append({"role": "assistant", "content": f"初始化模型失敗: {val_err}"})
        yield history, ""
        return
    except Exception as e:
        history.append({"role": "user", "content": message["text"] if isinstance(message, dict) else message})
        history.append({"role": "assistant", "content": f"初始化 Chat Chain 失敗: {e}"})
        yield history, ""
        return
        
    text = message.get("text", "") if isinstance(message, dict) else message
    files = message.get("files", []) if isinstance(message, dict) else []
    
    payload_content = []
    
    # 處理上傳的檔案
    if files:
        for file in files:
            file_path = file if isinstance(file, str) else file.path
            ext = file_path.lower().split('.')[-1]
            
            if ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                try:
                    base64_image = encode_image(file_path)
                    payload_content.append({
                        "type": "image_url", 
                        "image_url": f"data:image/{ext};base64,{base64_image}"
                    })
                except Exception as e:
                    payload_content.append({"type": "text", "text": f"\n[讀取圖片失敗: {e}]\n"})
            else:
                content, err = extract_text(file_path)
                if not err:
                    payload_content.append({"type": "text", "text": f"\n[提供檔案內容參考]\n{content}\n"})
                else:
                    payload_content.append({"type": "text", "text": f"\n[讀取檔案失敗: {err}]\n"})
    
    if text.strip():
        payload_content.append({"type": "text", "text": text})
        
    if not payload_content:
        history.append({"role": "assistant", "content": "請輸入文字或上傳檔案圖片。"})
        yield history, ""
        return
        
    from langchain_core.messages import HumanMessage
    payload = {"input": [HumanMessage(content=payload_content)]}
    
    # 如果使用者未輸入 session_id，則提供預設值
    if not session_id or not session_id.strip():
        session_id = "default_session"
    
    # Init empty response slot
    display_msg = text if text.strip() else "[多模態內容]"
    history.append({"role": "user", "content": display_msg})
    history.append({"role": "assistant", "content": ""})
    yield history, ""
    
    try:
        response_text = ""
        # 逐塊更新(Stream)
        for chunk in chain_with_history.stream(
            payload,
            config={"configurable": {"session_id": str(session_id).strip()}}
        ):
            response_text += chunk.content
            history[-1]["content"] = response_text
            yield history, ""
            
    except ResourceExhausted:
        error_msg = "\n\n⚠️ **系統提示：** 您已達到 Gemini API 免費方案的使用上限 (429 RESOURCE_EXHAUSTED)。請稍後再試！"
        history[-1]["content"] += error_msg
        yield history, ""
    except Exception as e:
        error_msg = f"\n\n處理請求時發生錯誤: {e}"
        if "429" in str(e):
            error_msg = "\n\n⚠️ **系統提示：** 您已達到 Gemini API 使用上限。請稍後再試！"
        history[-1]["content"] += error_msg
        yield history, ""


with gr.Blocks(title="Langchain + Gemini 聊天機器人") as demo:
    gr.Markdown("# 🤖 Langchain + Gemini 聊天機器人")
    gr.Markdown("支援多模態輸入，您可以上傳圖片 (jpg, png) 或是文件 (txt, pdf) 來與 AI 助手對話。此版本支援側邊欄動態切換聊天室與 AI 人設！")
    
    with gr.Row():
        # 左側邊欄配置
        with gr.Column(scale=1, min_width=250):
            gr.Markdown("### ⚙️ 聊天室設定")
            
            session_id_input = gr.Textbox(
                value="default_session", 
                label="聊天室名稱 (Session ID)", 
                info="切換不同名稱即可前往不同的聊天室並存檔對話紀錄。"
            )
            
            system_prompt_input = gr.Textbox(
                value="你是一個有用的、友善的 AI 助手。", 
                label="AI 個人設定 (System Prompt)", 
                lines=4, 
                info="設定你專屬的 AI 角色，例如：『你是一位專屬的 Python 工程師，你只用繁體中文回應...』"
            )
            
            gr.Markdown("---")
            gr.Markdown("*每個 Session ID 都會有獨立的 JSON 歷史紀錄檔！*")

        # 右側聊天區域
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="對話視窗", height=500, avatar_images=(None, "https://api.iconify.design/logos:google-gemini.svg"))
            msg = gr.MultimodalTextbox(
                interactive=True,
                file_types=["image", ".txt", ".pdf"],
                placeholder="輸入文字 或 點擊 ➕ 上傳檔案...",
                show_label=False
            )
            
            clear = gr.Button("清空畫面")

    # 事件綁定
    msg.submit(
        respond, 
        inputs=[msg, chatbot, session_id_input, system_prompt_input], 
        outputs=[chatbot, msg]
    )
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch()

