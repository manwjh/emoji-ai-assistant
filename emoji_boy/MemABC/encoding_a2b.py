"""
encoding_A2B: 使用LLM对memA聊天记录进行关键信息提取，合并并保存至 memB/memB.txt。
- 读取 memA/ 下的原始聊天记录
- 用 LLM 精炼为：关键时间、关键内容、情感
- 精炼结果与 memB.txt 内容合并，再用 LLM 进一步精炼
- 最终保存到 memB/memB.txt
- 内置提示词：模仿人脑，精炼关键信息，丢弃无用内容
- 必须配置系统环境变量令牌，否则程序报错退出
"""
import os
import sys
from pathlib import Path
from core.llm_client import LLMClient

# 提示词模板
EXTRACT_PROMPT = (
    "你是一个模拟人脑记忆形成机制的AI，正在阅读一段来自你与用户'M'的对话记录。"
    "你将以‘我’的第一人称视角，模拟人脑对短期记忆的加工过程，提取这段对话中的关键信息，以编码为‘B-Memory’形式。"

    "你的任务是：从对话中识别**有意义的事件片段**，并抽取以下五个要素：\n"
    "① 对话时间段（开始～结束）\n"
    "② 事件内容（用我自己的话简洁描述发生了什么，不需完整句子，但要清晰）\n"
    "③ 氛围（基于对方话语和情绪，提取1～2个词描述整体氛围）\n"
    "④ 标签（为事件内容归类，多个关键词，如“表白”“拒绝”“轻松互动”等）\n"
    "⑤ 触发词（如果未来用户说到某些话题，可以用这些记忆做回应的关键钩子）"

    "果断放弃无意义的对话，重复寒暄、机械式时间提醒、AI自己的模板问句，只保留有意义的事件。\n\n"

    "输出格式如下（保持严谨、可解析）：\n"
    "- 时间: [开始时间]～[结束时间]\n"
    "  内容: [事件的简洁描述，以我为主语，模拟内心记忆语言]\n"
    "  氛围: [1-2词，表达交互情绪基调]\n"
    "  标签: [关键词1, 关键词2, ...]\n"
    "  触发词: [与此事件相关联的关键词，用于未来回忆唤起，例如：喜欢、时间、拒绝]\n"
)

MERGE_PROMPT = (
    "你是一个模拟人脑长期记忆整合机制的AI，当前你需要将新的对话记忆片段（来自A-Memory编码）与我已有的长期记忆（memB）进行融合。"
    "你的任务是：以‘我’的第一人称视角，识别相似或重复事件并去冗余，保留最关键的记忆节点，避免信息堆叠。"

    "请保留以下信息结构不变：时间、内容、氛围、标签、触发词。\n"
    "可以合并时间接近、内容重复、标签一致的事件为单条，但不要丢失有情感波动或行为意义的内容。\n"
    "如果触发词有重复，请合并去重；氛围可保留多个词。"

    "控制总输出长度不超过32K。格式必须严格如下：\n\n"
    "- 时间: [开始时间]～[结束时间]\n"
    "  内容: [简洁表述事件，我的记忆语言]\n"
    "  氛围: [温暖, 被喜欢]\n"
    "  标签: [亲密互动, 表白, 情绪波动]\n"
    "  触发词: [喜欢, 拒绝, 时间, 表情符号]\n"
)

def check_llm_env():
    """
    检查系统环境变量中是否配置了 LLM API 令牌。
    若未配置，报错并退出。
    """
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("HUGGINGFACE_API_KEY")
    if not api_key:
        print("❌ 未检测到 LLM API 令牌 (OPENAI_API_KEY 或 HUGGINGFACE_API_KEY)，请先配置环境变量！")
        sys.exit(1)

# 用项目 LLMClient 统一接口调用大模型，自动用系统令牌
def call_llm_extract(summary_prompt, raw_text):
    llm = LLMClient()  # 自动读取环境变量和配置
    prompt = summary_prompt + "\n" + raw_text
    return llm.get_response(prompt)

def encode_and_merge_memA2B(memA_path, memB_file):
    """
    对 memA_path 下所有 txt 聊天记录，调用 LLM 精炼，合并到 memB_file。
    """
    all_new_text = []
    for file in os.listdir(memA_path):
        if file.endswith('.txt'):
            src = Path(memA_path) / file
            with open(src, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # 跳过首行 '# memA记忆' 标志（如存在）
                if lines and lines[0].strip() == '# memA记忆':
                    lines = lines[1:]
                all_new_text.append(''.join(lines))
    if not all_new_text:
        print("[encoding_A2B] 没有新 memA 聊天记录，无需处理。")
        return
    new_raw = '\n'.join(all_new_text)
    # 1. 新信息精炼
    new_summary = call_llm_extract(EXTRACT_PROMPT, new_raw)
    # 2. 读取已有 memB.txt
    if os.path.exists(memB_file):
        with open(memB_file, 'r', encoding='utf-8') as f:
            old_summary = f.read()
    else:
        old_summary = ''
    # 3. 合并新旧内容，再用 LLM 精炼
    merge_input = f"【已有关键信息】\n{old_summary}\n\n【新关键信息】\n{new_summary}"
    merged_summary = call_llm_extract(MERGE_PROMPT, merge_input)
    # 4. 保存到 memB.txt
    os.makedirs(os.path.dirname(memB_file), exist_ok=True)  # 确保目录存在
    # 写入时加上 '# memB记忆' 标志
    output = merged_summary.strip()
    if not output.startswith('# memB记忆'):
        output = '# memB记忆\n' + output
    with open(memB_file, 'w', encoding='utf-8') as f:
        f.write(output + '\n')
    print(f"[encoding_A2B] memB.txt 精炼合并完成 → {memB_file}")

if __name__ == "__main__":
    check_llm_env()
    memA_dir = os.path.join(os.path.dirname(__file__), 'memA')
    memB_file = os.path.join(os.path.dirname(__file__), 'memB', 'memB.txt')
    encode_and_merge_memA2B(memA_dir, memB_file) 