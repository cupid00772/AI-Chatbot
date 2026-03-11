# AI Chatbot 專案名稱

## 小組：第10組

### 組員： 

* 吳宸宇
* 林富閎
* 葉政毅
* 張承新

## 專案簡介

Gemini 多模態聊天機器人 — 一個用 Python 打造的 AI 聊天助手，透過 LangChain 串接 Google Gemini 2.5 Flash 模型，能理解文字、圖片、PDF 和文字檔，支援多輪對話記憶，並提供終端機（CLI）與網頁（Chainlit Web GUI）兩種操作介面。

## 目前功能

## 執行方式

1. 下載專案
2. 

範例指令：

```bash
git clone 你的專案網址
```

---

## 環境變數說明

請自行建立 `.env` 檔案，並填入自己的 API key。

範例：

```env
GEMINI_API_KEY=your_api_key_here
```

## 遇到的問題與解法

### 問題 1

問題： git 指令無法辨識 — Git 已安裝在 C:\Program Files\Git，但其路徑未加入系統 PATH，導致 PowerShell 找不到 git 指令。

解法： 將 C:\Program Files\Git\cmd 加入使用者環境變數 PATH：[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Program Files\Git\cmd", "User")


### 問題 2

問題： git commit 時出現 Author identity unknown 錯誤 — Git 無法自動偵測使用者身份，拒絕執行 commit。

解法： 使用 git config --global 設定使用者名稱與 Email


---

## 學習心得

> 請簡要寫出本次作業的學習心得。

---葉政毅:### 1. 核心大腦：Gemini 2.5 Flash + LangChain
我們選擇了最新的 `gemini-2.5-flash` 作為語言模型，並透過 `langchain-google-genai` 進行串接。LangChain 成功地將零散的對話封裝成易於管理的 `HumanMessage` 與 `AIMessage`，讓機器人不僅能單次問答，更具備了「記憶」整個上下文的對話能力。

### 2. 環境變數的踩坑與防護
在串接 API 的過程中，我們經歷了一段小小的環境變數名稱不一致（`GEMINI_API_KEY` 與 `GOOGLE_API_KEY`）的除錯過程。這提醒了我們，在建構這類依賴外部金鑰的應用時，同時支援多種慣用的變數名稱能大幅提升容錯率，並利用 `.env` 加上 `.gitignore` 來確保機敏資料不會不小心被上傳到公開的 GitHub。

### 3. 多模態 (Multimodal) 的賦能
有別於傳統只能輸入文字的腳本，我們引入了 `langchain-community` 的 `PyPDFLoader` 以及 Base64 轉換技術，讓專案具備了「讀圖」與「讀文件」的強大能力。這使得 AI 不再侷限於程式碼的世界，而能真正成為一個日常助手。

### 4. 從黑窗走到精美 UI：Chainlit
最後且最關鍵的一步，我們拋棄了傳統的終端機 `chat.py` 介面，轉而擁抱專為 AI 設計的 Web 框架 —— **Chainlit**。
這讓我們短短用一個 `app.py` 就實作出了：
- 現代化的對話氣泡與上傳檔案介面
- 即時打字機效果 (Streaming)
- 透過 `cl.user_session` 將繁雜的對話紀錄與 JSON 儲存功能無縫整合在背景處理

## 💡 未來可期的優化方向

這個專案目前已經擁有非常完整的雛形，若未來想進一步擴充，可以考慮：
1. **RAG (檢索增強生成)**：目前上傳的 PDF 是一股腦全塞給模型，若後續檔案過大（超過 Token 限制），可引入向量資料庫做切片檢索。
2. **工具調用 (Tool Calling)**：讓 Gemini 不只是聊天，還能幫忙查天氣、打 API 去抓取即時資訊。
3. **雲端部署**：考慮將 Chainlit 服務打包成 Docker，部署在 Render 或是 Zeabur 上，隨時隨地用手機也能操作。

---

> **開發小結**：這次專案深刻體會到，有了優質的模型搭上生態圈完善的套件（LangChain + Chainlit），開發出一個具備商業化潛力的 AI 助理已經不再遙不可及，期待這個小助手在未來能發揮更大的價值！


## GitHub 專案連結

請填入小組各組員 GitHub repository 網址。
https://github.com/james09021030-sudo/chatbot
https://github.com/Eric-wu0805/chatbot
https://github.com/cupid00772/AI-Chatbot.git
https://github.com/Eason92k/AI-agent.git
