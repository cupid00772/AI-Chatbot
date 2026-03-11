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

- 🤖 **AI 對話**：串接 Google Gemini 2.5 Flash 模型，支援繁體中文回應
- 💬 **多輪記憶**：具備對話上下文記憶，能理解前後文脈絡
- 🖼️ **圖片分析**：上傳 JPG / PNG 圖片，AI 自動辨識並描述內容
- 📄 **PDF 閱讀**：上傳 PDF 檔案，AI 提取文字並進行摘要或問答
- 📝 **文字檔處理**：上傳 .txt 檔案，AI 分析文字內容
- 💾 **對話紀錄**：自動將對話歷史儲存為 JSON 格式（含時間戳記與檔案資訊）
- 🌐 **Web GUI**：透過 Chainlit 提供瀏覽器介面，支援拖曳上傳與串流回應
- ⌨️ **CLI 模式**：終端機介面，輸入檔案路徑即可分析

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
林富閎:
這次製作 AI Chatbot 的過程，讓我對人工智慧與程式設計有了更深入的了解。一開始在設計聊天流程時，常常會遇到不知道如何讓機器正確理解使用者問題的困難，但透過不斷測試與修改，我慢慢學會如何調整回應邏輯，讓聊天機器人能更順利地與使用者互動。

在製作的過程中，我也體會到 AI 並不是只要寫好程式就能完成，還需要考慮使用者體驗，例如回應是否清楚、是否能解決問題等。這讓我了解到設計一個好的 Chatbot，需要同時具備技術能力與同理心。

透過這次的專題，我不僅提升了自己的問題解決能力，也對 AI 的應用產生更大的興趣。未來如果有機會，我希望能繼續學習更多人工智慧相關的技術，並嘗試把 AI 應用在更多不同的領域
> 吳宸宇# 一、LangChain 框架整合
這次實作讓我理解了 LangChain 的模組化設計。透過 `ChatGoogleGenerativeAI` 串接 Gemini 模型，搭配 `HumanMessage`、`AIMessage`、`SystemMessage` 等訊息物件來管理對話流程，整體架構清晰且易於擴充。特別是多模態的處理方式——將圖片以 Base64 編碼嵌入 `HumanMessage` 的 content list 中，讓文字與圖片能在同一個訊息中傳遞給模型，這種設計模式值得學習。
吳宸宇一、LangChain 框架整合
這次實作讓我理解了 LangChain 的模組化設計。透過 `ChatGoogleGenerativeAI` 串接 Gemini 模型，搭配 `HumanMessage`、`AIMessage`、`SystemMessage` 等訊息物件來管理對話流程，整體架構清晰且易於擴充。特別是多模態的處理方式——將圖片以 Base64 編碼嵌入 `HumanMessage` 的 content list 中，讓文字與圖片能在同一個訊息中傳遞給模型，這種設計模式值得學習。
### 二、多模態檔案處理
學會了三種不同檔案類型的處理策略：
- **圖片**：Base64 編碼後以 `image_url` 格式直接傳給 Gemini 視覺模型
- **PDF**：透過 `PyPDFLoader` 逐頁提取文字，再以文本方式傳入
- **TXT**：直接讀取內容，並考慮編碼問題（UTF-8 優先、Big5 備援）
這讓我體會到不同資料型態需要不同的前處理方式，而好的架構能讓這些處理邏輯各自獨立、互不干擾。
### 三、Chainlit Web GUI 開發
從 CLI 轉換到 Web GUI，Chainlit 的事件驅動模型（`@cl.on_chat_start`、`@cl.on_message`、`@cl.on_chat_end`）讓整合過程非常直覺。最有收穫的是學會了**串流回應**（`llm.astream()` + `stream_token()`），讓使用者體驗從「等待完整回應」提升到「即時看到文字逐步產生」，這在實際應用中差異很大。
另外，透過 [app.py](cci:7://file:///c:/Users/User/Desktop/chatbot/app.py:0:0-0:0) 直接 import [chatbot.py](cci:7://file:///c:/Users/User/Desktop/chatbot/chatbot.py:0:0-0:0) 的函式，實現了**零重複程式碼**的雙介面架構，這是良好的模組化設計實踐。
### 四、Git 版控與環境管理
實際操作中遇到了 Git 路徑未加入 PATH、使用者身份未設定等環境問題，也學到了 [.gitignore](cci:7://file:///c:/Users/User/Desktop/chatbot/.gitignore:0:0-0:0) 的重要性——確保 API Key（[.env](cci:7://file:///c:/Users/User/Desktop/chatbot/.env:0:0-0:0)）、虛擬環境（`venv/`）和自動生成的檔案不會被提交到版本庫中。
### 五、總結
這個專案完整走過了從**核心邏輯開發 → 多模態擴充 → Web GUI 包裝 → 版控上線**的全流程，是一次理論與實務結合的寶貴經驗。
本次作業的學習心得。


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
