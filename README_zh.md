# LocalWhisperAPIService
Whisper 语音识别 API

这是一个基于 OpenAI 的 Whisper 语音识别模型构建的 API 服务。它能够将上传的音频文件（如 mp3、wav 等）转换为文本。

功能特性

• 支持多种常见音频格式上传，包括 mp3、wav、flac 等
• 基于 Whisper 模型，支持多种语言识别
• RESTful API 接口，方便前端集成
• 支持批量音频文件处理
• 并发控制和错误处理
• （其他特性）

技术栈

• Python 3.8+
• FastAPI 或 Flask Web 框架
• Whisper 语音识别模型
• （其他依赖库）

安装部署

1. 克隆代码仓库
2. (选项 A) 使用虚拟环境：
   a. 创建虚拟环境：
      python3 -m venv myvenv
   b. 激活虚拟环境：
      - Windows 系统：`myvenv\Scripts\activate`
      - macOS 和 Linux 系统：`source myvenv/bin/activate`
   c. 在安装依赖之前，打开 `requirements.txt` 文件并修改 `tokenizers` 行：
      - 找到以 `https://files.pythonhosted.org/packages/...` 开头的行
      - 将其替换为适合您系统的 wheel URL。例如：
        - 对于 Linux 上的 Python 3.10：使用现有的 URL
        - 对于其他系统：访问 https://pypi.org/project/tokenizers/#files，找到适合您系统的 wheel，并使用其 URL
   d. 安装依赖：`pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt`
   e. 启动 API 服务：`uvicorn app.main:app --reload`
3. (选项 B) 使用 Docker：
   a. 构建 Docker 镜像：
      `docker build -t localwhisperapi .`
   b. 运行 Docker 容器：
      `docker run -d -p 8000:8000 localwhisperapi`
4. 访问 http://localhost:8000/docs 查看接口文档

使用方法

1. 将音频文件 POST 到 /recognize 接口
2. 返回结果为一个 JSON 对象，包含识别出的文本内容

贡献代码

欢迎提交 Issue 或 Pull Request！
