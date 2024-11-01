import aiohttp
import asyncio
import json

OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL1 = "qwen2.5:3b"  # 替换为实际的第一个模型名称
MODEL2 = "qwen2.5:3b"  # 替换为实际的第二个模型名称
DIALOGUE_LIMIT = 30  # 设置对话次数限制
CONTEXT_LENGTH = 10240  # 设置上下文长度为10240

async def generate_chat(session, model, messages):
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "num_ctx": CONTEXT_LENGTH  # 设置上下文长度
        }
    }
    async with session.post(OLLAMA_API_URL, json=payload) as response:
        response.raise_for_status()
        return await response.json()

async def chat(models, limit):
    async with aiohttp.ClientSession() as session:
        # 设置初始提示词
        prompt1 = "你好，我是洛天依。今天天气不错，我们来聊聊日常吧。你最近有什么新鲜事吗？"
        prompt2 = "嗨，我是言和。确实，天气真好。我最近在忙着学习新技能。你呢，有什么有趣的计划？"
        
        # 根据模型轮流设置提示词和开始对话
        current_model = models[0]
        previous_prompt = prompt1 if models[0] == current_model else prompt2
        
        messages = [{"role": "user", "content": previous_prompt}]
        
        for i in range(limit):
            # 生成聊天回复
            response = await generate_chat(session, current_model, messages)
            reply = response['message']['content']
            print(f"{current_model} 说: {reply}")
            
            # 将上一个模型的回复作为下一个模型的输入
            next_model = models[1] if current_model == models[0] else models[0]
            messages = [{"role": "user", "content": reply}]
            
            # 切换到另一个模型
            current_model = next_model
        
        print("对话结束。")

# 运行聊天流程
models = [MODEL1, MODEL2]
asyncio.run(chat(models, DIALOGUE_LIMIT))
