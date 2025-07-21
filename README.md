# ResonantSoul 

心灵伴侣-您的AI心理健康助手，这是一个基于Gradio和Camel-AI框架构建的心理健康智能体系统，主要面向大学生群体，提供心理咨询和支持服务。系统的核心是基于Camel-AI的多智能体对话框架，通过角色扮演实现专业的心理咨询功能。

## 环境安装

1. 基础环境：Python3.10+

2. 安装UV
```shell
pip install uv
set UV_INDEX=https://mirrors.aliyun.com/pypi/simple
```

3. 安装Python依赖包
```shell
uv sync --python 3.10 --all-extras
```

4. 切换到本地环境(.venv)
```shell
cd .venv/Scripts
activate
```

## 启动项目
1. 在conf路径中，配置系统文件`config.ini`

```text
[LLM]
base_url = https://ark.cn-beijing.volces.com/api/v3
api_key = your_api_key
model_id = deepseek-r1-250120
```

2. 启动项目的前后端

```shell
python api/memchain_server.py
python web/web_server.py
```

3. 访问项目：

系统 API 详情访问地址：http://127.0.0.1:8000/docs
用户界面访问地址：http://127.0.0.1:7860