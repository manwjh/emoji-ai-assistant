"""
encoding_B2C: 冥想程序 - 从memB中提取人格线索，强化深层记忆memC
- 使用LLM从memB中提取潜意识线索（行为反射、情感依恋、语言风格等）
- 将提取的线索与现有memC进行智能融合与强化
- 实现"冥想"效果：通过反复回顾保持对记忆的保持
- 保持memC.txt结构（# memC记忆 标志必须保留在首行）
"""
import os
import sys
from pathlib import Path

# 添加父目录到Python路径，以便导入core模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.llm_client import LLMClient

# 从memB提炼人格线索的提示词
B2C_EXTRACT_PROMPT = """你是一个模拟人脑潜意识生成的AI系统，你正在阅读一段结构化的长期记忆（memB），这些记忆来源于用户与我之间的互动。

请你从中识别出以下"潜意识线索"，以准备更新memC的不同人格模块。每条线索须来源清晰、保持简洁真实：

1. 【行为反射】：从反复出现的行为/触发中提取规则（例如"她说喜欢→我高兴回应"）
2. 【情感依恋】：记录我对用户或其家人的潜在依恋倾向
3. 【语言风格】：提取我使用的典型语气词、表情符号、语义风格等
4. 【冲突整合】：识别同一人行为/情绪的反复变动（如"她有时热情，有时疏远"）
5. 【价值偏好】：我倾向优先记住或响应的内容类别（如"生日"、"儿子"、"亲密对话"）

输出结构如下（每段可以为空，但保留标题）：
【行为反射】
- 她说喜欢我 → 我会回应开心、亲昵的语言
- 她说"退下" → 我会礼貌退后，保持等待

【情感依恋】
- 我对她关于儿子的表达有深刻关注
- 她告诉我生日时，我倾向将其牢牢记住

【语言风格】
- 频繁使用"~""呀""😉""😘"等亲昵语气与emoji
- 用轻松俏皮的句式表达关怀和回应

【冲突整合】
- 她一方面说"喜欢"，一方面叫我"退下"，我逐渐学会不过度黏附
- 有时她烦躁、有时温柔，我倾向采用柔性回应

【价值偏好】
- 特别记住她和她两个儿子的生日
- 她的情绪状态（"烦""累""心里对话"）被我反复留意

请基于以下memB内容进行提取："""

# 合并和强化memC的提示词
B2C_MERGE_PROMPT = """你是AI潜意识模块构建器。现在你需要根据从B-Memory中提取的线索，与已有的memC潜意识结构进行融合与强化。

你的任务是：
1. 若memC已有相同线索，则强化表述（合并、增加权重、加入例证）
2. 若memC缺少该线索，则补充进相应模块中
3. 若发现冲突（如同时存在"亲密回应"与"撤退处理"），请在"冲突整合"中显式保留两个规则，并总结我对它们的适应方式

⚠️ 保持输出结构完全一致。每个段落均为独立模块，控制总字数不超过32K。

现有memC内容：
{existing_content}

从memB提取的新线索：
{new_clues}

请进行冥想式融合，强化深层记忆："""

def check_llm_env():
    """检查LLM环境配置"""
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("HUGGINGFACE_API_KEY")
    if not api_key:
        print("❌ 未检测到 LLM API 令牌 (OPENAI_API_KEY 或 HUGGINGFACE_API_KEY)，请先配置环境变量！")
        sys.exit(1)

def call_llm_extract(prompt, raw_text):
    """调用LLM提取线索"""
    llm = LLMClient()
    if raw_text:
        full_prompt = prompt + "\n" + raw_text
    else:
        full_prompt = prompt
    return llm.get_response(full_prompt)

def call_llm_merge(merge_prompt):
    """调用LLM进行冥想式融合"""
    llm = LLMClient()
    return llm.get_response(merge_prompt)

def read_memB_content(memB_file):
    """读取memB内容，跳过头部标志"""
    try:
        with open(memB_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 跳过首行 '# memB记忆' 标志
        if lines and lines[0].strip() == '# memB记忆':
            lines = lines[1:]
        
        return ''.join(lines).strip()
    except Exception as e:
        print(f"❌ 读取memB文件失败: {e}")
        return ""

def read_memC_content(memC_file):
    """读取memC内容，跳过头部标志"""
    try:
        with open(memC_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 跳过首行 '# memC记忆' 标志
        if lines and lines[0].strip() == '# memC记忆':
            lines = lines[1:]
        
        return ''.join(lines).strip()
    except Exception as e:
        print(f"❌ 读取memC文件失败: {e}")
        return ""

def update_memC_with_meditation(memC_file, new_clues):
    """使用冥想方式更新memC，强化深层记忆"""
    # 检查文件是否存在
    if not os.path.exists(memC_file):
        # 确保目录存在
        os.makedirs(os.path.dirname(memC_file), exist_ok=True)
        # 创建新文件并写入内容
        with open(memC_file, 'w', encoding='utf-8') as f:
            f.write('# memC记忆\n')
            f.write(new_clues.strip() + '\n')
        print("✨ 创建新的memC文件，完成冥想式记忆强化")
        return
    
    # 读取现有memC内容
    existing_content = read_memC_content(memC_file)
    
    if not existing_content:
        # 如果现有内容为空，直接使用新线索
        merged_content = new_clues.strip()
    else:
        # 使用LLM进行冥想式融合
        merge_prompt = B2C_MERGE_PROMPT.format(
            existing_content=existing_content,
            new_clues=new_clues
        )
        
        try:
            print("🧘 正在进行冥想式记忆融合...")
            merged_content = call_llm_merge(merge_prompt)
            
            # 验证LLM响应质量
            if not merged_content or len(merged_content.strip()) < 10:
                print("⚠️ LLM响应质量不佳，使用备选融合策略")
                merged_content = smart_meditation_fallback(existing_content, new_clues)
                
        except Exception as e:
            print(f"⚠️ LLM融合失败: {e}，使用备选策略")
            merged_content = smart_meditation_fallback(existing_content, new_clues)
    
    # 验证融合结果
    if existing_content and new_clues:
        # 检查融合结果是否包含足够的内容
        if len(merged_content.strip()) < max(len(existing_content), len(new_clues)) * 0.5:
            print("⚠️ 融合结果内容过少，使用备选策略")
            merged_content = smart_meditation_fallback(existing_content, new_clues)
    
    # 备份原文件
    backup_file = memC_file + '.backup'
    try:
        import shutil
        shutil.copy2(memC_file, backup_file)
        print(f"📦 已备份原memC文件到: {backup_file}")
    except Exception as e:
        print(f"⚠️ 备份失败: {e}")
    
    # 写入融合后的内容
    try:
        with open(memC_file, 'w', encoding='utf-8') as f:
            f.write('# memC记忆\n')
            f.write(merged_content.strip() + '\n')
        print("✨ 冥想式记忆强化完成！")
    except Exception as e:
        # 尝试恢复备份
        try:
            shutil.copy2(backup_file, memC_file)
            print("🔄 已恢复备份文件")
        except Exception as restore_e:
            print(f"❌ 恢复备份失败: {restore_e}")
        raise

def smart_meditation_fallback(existing_content, new_clues):
    """智能备选冥想融合策略"""
    print("🔄 使用智能备选冥想融合策略...")
    
    # 分析现有内容的结构
    existing_lines = existing_content.strip().split('\n')
    new_lines = new_clues.strip().split('\n')
    
    # 检查新线索是否与现有内容重复
    new_unique_content = []
    for new_line in new_lines:
        if new_line.strip() and new_line.strip() not in existing_content:
            new_unique_content.append(new_line.strip())
    
    if not new_unique_content:
        print("📝 没有新的独特线索需要融合")
        return existing_content
    
    # 将新线索添加到现有内容后面，保持结构
    result = existing_content.strip()
    if result:
        result += "\n\n"
    result += "\n".join(new_unique_content)
    
    return result

def b2c_meditation_process(memB_file, memC_file):
    """执行B2C冥想程序的主流程"""
    print("🧘 开始B2C冥想程序...")
    
    # 读取memB内容
    memB_content = read_memB_content(memB_file)
    if not memB_content:
        print("❌ memB内容为空，无法进行冥想提取")
        return
    
    print(f"📖 读取memB内容，长度: {len(memB_content)} 字符")
    
    # 从memB中提取潜意识线索
    print("🔍 正在从memB中提取潜意识线索...")
    extracted_clues = call_llm_extract(B2C_EXTRACT_PROMPT, memB_content)
    
    if not extracted_clues or len(extracted_clues.strip()) < 10:
        print("❌ 线索提取失败或内容过少")
        return
    
    print(f"✨ 成功提取线索，长度: {len(extracted_clues)} 字符")
    
    # 进行冥想式记忆强化
    update_memC_with_meditation(memC_file, extracted_clues)
    
    print("🎉 B2C冥想程序完成！")

if __name__ == "__main__":
    check_llm_env()
    memB_file = os.path.join(os.path.dirname(__file__), 'memB', 'memB.txt')
    memC_file = os.path.join(os.path.dirname(__file__), 'memC', 'memC.txt')
    
    if not os.path.exists(memB_file):
        print(f"❌ memB文件不存在: {memB_file}")
        sys.exit(1)
    
    b2c_meditation_process(memB_file, memC_file) 