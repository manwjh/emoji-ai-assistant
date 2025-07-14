"""
encoding_A2B: 使用LLM对memA聊天记录进行关键信息提取，合并并保存至 memB/memB.txt。
- 读取 memA/ 下的原始聊天记录（仅最近7天）
- 用 LLM 精炼为：关键时间、关键内容、情感
- 精炼结果与 memB.txt 内容合并，再用 LLM 进一步精炼
- 最终保存到 memB/memB.txt
- 内置提示词：模仿人脑，精炼关键信息，丢弃无用内容
- 必须配置系统环境变量令牌，否则程序报错退出
"""
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加父目录到Python路径，以便导入core模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.llm_client import LLMClient

# 提示词模板（升级提示词）
# 历史记录：
# V2: 深圳王哥，2025/07/12 21:20:47～2025/07/12 23:49:31 提取到生日等关键信息
A2B_EXTRACT_PROMPT_V2 = (
    "你是一个模拟人脑记忆形成机制的AI，正在阅读一段来自你与用户'M'的对话记录。"
    "你将以‘我’的第一人称视角，模拟大脑对短期记忆的提取和编码过程，将其转化为结构化的‘B-Memory’形式。\n\n"

    "你的任务是从对话中**判断并提取有意义的记忆片段**，特别关注以下内容：\n"
    "- 任何与具体人、日期、事件有关的**事实性信息**（如生日、身份、关系等）必须被记录\n"
    "- 忽略无意义的寒暄、AI模板回应、无实质信息的问答\n"
    "- 尽可能保留能在未来被唤起的钩子词（如“喜欢”、“10月23日”、“儿子”）\n\n"

    "请提取以下五个维度，保持每段信息精炼但有意义：\n"
    "① 时间段（开始时间～结束时间）\n"
    "② 内容摘要（以我为主语，简洁清晰地描述该事件记忆，不需完整句子，但保留事实和情绪）\n"
    "③ 氛围（1～2个词，用于描述对话整体情绪）\n"
    "④ 标签（给这段记忆打分类标签，如：表白、家庭、生日、烦躁、互动）\n"
    "⑤ 触发词（未来触发该记忆的关键词，如：生日、儿子、退下、喜欢等）\n\n"

    "输出格式如下（保持结构严谨、可被程序解析）：\n"
    "- 时间: [开始时间]～[结束时间]\n"
    "  内容: [我从M那里得知M的生日是10月23日，我确认会记住这个特别的日子。]\n"
    "  氛围: [亲密, 温暖]\n"
    "  标签: [生日, 私密信息, 重要事实]\n"
    "  触发词: [生日, 10月23日, 我的生日]\n"
)

A2B_MERGE_PROMPT = (
    "你是一个模拟人脑长期记忆整合机制的AI，当前你需要将新的对话记忆片段（来自memA编码）与我已有的长期记忆（memB）进行融合。"
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
    对 memA_path 下最近7天的 txt 聊天记录，调用 LLM 精炼，合并到 memB_file。
    """
    # 计算7天前的日期
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    all_new_text = []
    processed_files = []
    
    for file in os.listdir(memA_path):
        if file.endswith('.txt'):
            src = Path(memA_path) / file
            # 获取文件修改时间
            file_mtime = datetime.fromtimestamp(src.stat().st_mtime)
            
            # 只处理最近7天的文件
            if file_mtime >= seven_days_ago:
                with open(src, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # 跳过首行 '# memA记忆' 标志（如存在）
                    if lines and lines[0].strip() == '# memA记忆':
                        lines = lines[1:]
                    all_new_text.append(''.join(lines))
                processed_files.append(file)
    
    if not all_new_text:
        print("[encoding_A2B] 没有最近7天的新 memA 聊天记录，无需处理。")
        return
    
    print(f"[encoding_A2B] 处理最近7天的文件: {', '.join(processed_files)}")
    
    new_raw = '\n'.join(all_new_text)
    # 1. 新信息精炼
    new_summary = call_llm_extract(A2B_EXTRACT_PROMPT_V2, new_raw)
    # 2. 读取已有 memB.txt
    if os.path.exists(memB_file):
        with open(memB_file, 'r', encoding='utf-8') as f:
            old_summary = f.read()
    else:
        old_summary = ''
    # 3. 合并新旧内容，再用 LLM 精炼
    merge_input = f"【已有关键信息】\n{old_summary}\n\n【新关键信息】\n{new_summary}"
    merged_summary = call_llm_extract(A2B_MERGE_PROMPT, merge_input)
    # 4. 保存到 memB.txt
    os.makedirs(os.path.dirname(memB_file), exist_ok=True)  # 确保目录存在
    # 写入时加上 '# memB记忆' 标志
    output = merged_summary.strip()
    if not output.startswith('# memB记忆'):
        output = '# memB记忆\n' + output
    with open(memB_file, 'w', encoding='utf-8') as f:
        f.write(output + '\n')
    print(f"[encoding_A2B] memB.txt 精炼合并完成 → {memB_file}")

def encode_a2b():
    """A2B编码主函数，返回是否成功"""
    try:
        check_llm_env()
        memA_dir = os.path.join(os.path.dirname(__file__), 'memA')
        memB_file = os.path.join(os.path.dirname(__file__), 'memB', 'memB.txt')
        encode_and_merge_memA2B(memA_dir, memB_file)
        return True
    except Exception as e:
        print(f"A2B编码失败: {e}")
        return False

if __name__ == "__main__":
    encode_a2b() 