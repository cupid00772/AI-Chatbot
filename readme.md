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

問題：
解法：

---

## 學習心得

> 請簡要寫出本次作業的學習心得。

---

## GitHub 專案連結

請填入小組各組員 GitHub repository 網址。
https://github.com/james09021030-sudo/chatbot
https://github.com/Eric-wu0805/chatbot
https://github.com/cupid00772/AI-Chatbot.git
https://github.com/Eason92k/AI-agent.git
