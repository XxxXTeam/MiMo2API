# Mimo2API Python版本

将小米 Mimo AI 转换为 OpenAI 兼容 API，支持深度思考功能。

## 特性

- ✅ **OpenAI 兼容**: 完全兼容 OpenAI API 格式
- ✅ **深度思考**: 支持 `reasoning_effort` 参数启用深度思考模式
- ✅ **流式响应**: 支持 SSE 实时流式传输
- ✅ **账号轮询**: 多账号负载均衡
- ✅ **Web 管理**: 内置管理界面，方便配置
- ✅ **异步支持**: 基于 FastAPI 的高性能异步实现
- ✅ **自动文档**: 自动生成 API 文档（访问 `/docs`）

## 快速开始

### 1. 安装依赖

```bash
cd mimo2api_python
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8080` 启动。

### 3. 配置账号

访问 `http://localhost:8080` 打开管理界面，按照以下步骤配置：

1. **获取凭证**：
   - 登录 [aistudio.xiaomimimo.com](https://aistudio.xiaomimimo.com)
   - 打开浏览器开发者工具 → Network
   - 发送一条消息，找到 `chat` 请求
   - 右键 → Copy as cURL
   - 粘贴到管理界面

2. **配置 API Keys**：
   - 在管理界面设置自定义 API Key（逗号分隔多个）
   - 默认为 `sk-default`

## 使用示例

## 支持模型

| 模型 ID (Model) | 模型名称 (Name) | 备注 |
|------|------|------|
| `mimo-v2.5-pro` | MiMo-V2.5-Pro | 默认旗舰模型 (开源性能旗舰) |
| `mimo-v2.5` | MiMo-V2.5 | 全模态理解大模型 (支持翻译/视觉问答) |
| `mimo-v2-flash-studio` | MiMo-V2-Flash | 极速推理轻量级模型 |
| `mimo-v2-flash` | MiMo-V2-Flash | 极速推理轻量级大模型 (旧版ID) |
| `mimo-v2-pro` | MiMo-V2-Pro | 深度思考模型 (旧版ID) |
| `mimo-v2-omni` | MiMo-V2-Omni | 支持多模态生文 (旧版ID) |

接口同时兼容 `-thinking`、`-search`、`-thinking-search`、`-search-thinking` 后缀，例如 `mimo-v2.5-pro-thinking`。

### 基础调用

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-default" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'
```

### 启用深度思考

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-default" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [
      {"role": "user", "content": "解释量子纠缠"}
    ],
    "reasoning_effort": "medium"
  }'
```

### 流式响应

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-default" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [
      {"role": "user", "content": "写一首诗"}
    ],
    "stream": true
  }'
```

## API 端点

| 端点 | 方法 | 功能 | 认证 |
|------|------|------|------|
| `/v1/chat/completions` | POST | OpenAI 兼容的聊天接口 | Bearer Token |
| `/api/config` | GET/POST | 获取/更新配置 | 无 |
| `/api/parse-curl` | POST | 解析 cURL 命令提取凭证 | 无 |
| `/api/test-account` | POST | 测试 Mimo 账号有效性 | 无 |
| `/` | GET | 管理界面 | 无 |
| `/docs` | GET | API 文档（Swagger UI） | 无 |

## 配置文件

配置文件 `config.json` 会自动创建在运行目录：

```json
{
  "api_keys": "sk-default,sk-custom",
  "mimo_accounts": [
    {
      "service_token": "your_service_token",
      "user_id": "123456",
      "xiaomichatbot_ph": "your_xiaomichatbot_ph"
    }
  ]
}
```

## 环境变量

- `PORT`: 服务端口（默认 8080）

```bash
PORT=3000 python main.py
```

## 项目结构

```
mimo2api_python/
├── app/
│   ├── __init__.py          # 包初始化
│   ├── config.py            # 配置管理
│   ├── mimo_client.py       # Mimo API 客户端
│   ├── models.py            # OpenAI 数据模型
│   ├── routes.py            # API 路由
│   └── utils.py             # 工具函数
├── web/
│   └── index.html           # 管理界面
├── main.py                  # 主程序入口
├── requirements.txt         # 依赖列表
└── README.md               # 项目文档
```

## 技术栈

- **Web 框架**: FastAPI 0.115.5
- **ASGI 服务器**: Uvicorn 0.32.1
- **HTTP 客户端**: httpx 0.27.2
- **数据验证**: Pydantic 2.10.3

## 深度思考模式

通过设置 `reasoning_effort` 参数启用深度思考：

- `low`: 低强度思考
- `medium`: 中等强度思考
- `high`: 高强度思考

**流式响应格式**：
```json
{"choices":[{"delta":{"reasoning":"思考内容..."}}]}
{"choices":[{"delta":{"content":"回复内容..."}}]}
```

**非流式响应格式**：
```json
{
  "choices": [{
    "message": {
      "content": "<think>思考内容</think>\n回复内容"
    }
  }]
}
```

## 与 Go 版本的对比

| 特性 | Go 版本 | Python 版本 |
|------|---------|-------------|
| 性能 | 更高 | 良好 |
| 内存占用 | 更低 | 适中 |
| 部署 | 单一二进制 | 需要 Python 环境 |
| 开发效率 | 中等 | 更高 |
| 异步支持 | 标准库 | 原生异步 |
| API 文档 | 无 | 自动生成 |
| 类型检查 | 编译时 | 运行时（Pydantic） |

## 开发

### 安装开发依赖

```bash
pip install -r requirements.txt
```

### 运行开发服务器

```bash
# 自动重载模式
uvicorn main:app --reload --port 8080
```

### 查看 API 文档

启动服务后访问：
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## 故障排除

### 1. 端口被占用

```bash
# 更改端口
PORT=3000 python main.py
```

### 2. 账号无效

- 在管理界面使用"测试"功能验证账号
- 重新获取最新的 cURL 命令

### 3. 依赖安装失败

```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 许可证

本项目基于原 Go 版本 [mimo2api](https://github.com/leookun/mimo2api) 重写。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关链接

- [原 Go 版本](https://github.com/leookun/mimo2api)
- [小米 Mimo AI](https://aistudio.xiaomimimo.com)
- [FastAPI 文档](https://fastapi.tiangolo.com)
