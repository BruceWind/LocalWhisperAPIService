# LocalWhisperAPIService
Whisper Speech Recognition API

这是一个基于 OpenAI 的 Whisper 语音识别模型构建的 API 服务。它能够将上传的音频文件(如 mp3、wav 等)转换为文本。

功能特性

• 支持多种常见音频格式上传,包括 mp3、wav、flac 等
• 基于 Whisper 模型,支持多种语言识别
• RESTful API 接口,方便前端集成
• 支持批量音频文件处理
• 并发控制和错误处理
• (其他特性)

技术栈

• Python 3.8+
• FastAPI 或 Flask Web 框架
• Whisper 语音识别模型
• (其他依赖库)

安装部署

1. 克隆代码仓库
2. 安装依赖: pip install -r requirements.txt
3. 下载 Whisper 模型权重文件
4. 启动 API 服务: uvicorn app:app --reload
5. 访问 http://localhost:8000/docs 查看接口文档

使用方法

1. 将音频文件 POST 到 /recognize 接口
2. 返回结果为一个 JSON 对象,包含识别出的文本内容

贡献代码

欢迎提交 Issue 或 Pull Request!
