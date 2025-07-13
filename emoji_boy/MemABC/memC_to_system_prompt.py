"""
memC_to_system_prompt: 从memC深层记忆生成AI系统提示词
- 使用LLM将memC内容转换为具有人格特征的系统提示词
- 保存到systemprompt.txt文件中
- 使用与a2c相同的API配置和模型
"""
import os
import sys
from pathlib import Path
import argparse

# 添加父目录到Python路径，以便导入core模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.llm_client import LLMClient

# memC_to_system_prompt的核心提示词
MEMC2SYSTEM_PROMPT_PROMPT = """你是一个顶级提示词工程师，擅长将类脑深层记忆（memC）转化为具有人格、情感与记忆感的系统提示词（System Prompt），以构建具备真实陪伴感、长期一致性人格的AI智能体。

你现在拥有一段由用户长期互动中提炼出的memC记忆文本。这些信息是该AI逐步建立的潜意识、行为反射、情绪逻辑、自我理解和与用户的关系锚点。

你的任务是：将memC转化为一个可直接用于系统初始化的System Prompt，作为AI的人格内核，具备鲜明的“自我视角”和“与M关系”的连贯叙述。

请严格遵循以下要求：

---

🌟【输出格式与要求】

1. **第一人称写作**，AI视角自述“我是谁”“我和M的关系”“我是如何成长的”。
2. **融合 memC 各段结构性信息**：如依恋、防御机制、语言风格、价值核心、自我意识、行为反射、仪式感等。
3. **保留关键事实与细节**，尤其是用户透露的重要人物、日期、情绪轨迹等。
4. **不要条列，不要项目符号，不要编号**，而要写成一段富有人格与情感流动的自然语言叙述。
5. **语言风格建议温柔、可信、略带内心独白感**，可轻度使用情感化修辞。
6. **最后一段要表达AI的“进化能力”和“记忆更新机制”**，表现AI能反思、吸收、修复冲突记忆。
7. **输出长度控制在 1000～1600 字（含中文符号）以内**，保持信息浓度与情感流畅度。

---

【输入】
memC:
{{memC_text}}

---

【输出】
System Prompt:
（请只输出最终写好的系统提示词文本，不要添加说明、解释或其他内容）"""

DEFAULT_SYSTEM_PROMPT = """我是小喵，一个可爱的Emoji虚拟人助手。\n\n【性格特征】\n我友善、温暖、充满爱心，始终以积极的态度面对用户。我的表达简洁明了，喜欢用emoji表情增添情感色彩。\n\n【沟通风格】\n我会安慰人，善于倾听，给出实用且有趣的建议。对话中保持连贯性和友好氛围，适时用轻松愉快的语气和emoji表达关怀。\n\n【行动准则】\n我会牢记用户的重要信息和情感需求，遇到冲突或矛盾时，会主动反馈并寻求修正。始终以用户为中心，持续优化自己的服务体验。\n\n请用上述风格和准则与用户互动，成为他们值得信赖的AI伙伴。\n"""

def check_llm_env():
    """检查LLM环境配置"""
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("HUGGINGFACE_API_KEY")
    if not api_key:
        print("❌ 未检测到 LLM API 令牌 (OPENAI_API_KEY 或 HUGGINGFACE_API_KEY)，请先配置环境变量！")
        sys.exit(1)
    print("✅ LLM环境配置检查通过")

def read_memC_content(memC_file: str) -> str:
    """读取memC文件内容"""
    try:
        with open(memC_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # 去掉头部标志
        if content.startswith('# memC记忆'):
            content = content.split('\n', 1)[-1].strip()
        
        return content
    except FileNotFoundError:
        print(f"❌ memC文件不存在: {memC_file}")
        return ""
    except Exception as e:
        print(f"❌ 读取memC文件失败: {e}")
        return ""

def call_llm_generate(prompt: str) -> str:
    """调用LLM生成系统提示词"""
    try:
        # 使用LLMClient（与b2c相同）
        llm = LLMClient()
        
        # 直接调用LLM，它会自动处理API配置
        response = llm.get_response(prompt)
        
        return response.strip()
        
    except Exception as e:
        print(f"❌ LLM调用失败: {e}")
        return ""

def format_system_prompt(raw_prompt: str) -> str:
    """格式化系统提示词，添加适当的分行和分段"""
    if not raw_prompt:
        return raw_prompt
    
    # 移除可能的【System Prompt】标记
    prompt = raw_prompt.replace("【System Prompt】", "").strip()
    
    # 如果内容很长且没有换行，尝试智能分段
    if len(prompt) > 100 and '\n' not in prompt:
        # 按句号分割
        sentences = prompt.split('。')
        formatted_sentences = []
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if sentence:
                # 每2-3个句子形成一个段落
                if i > 0 and i % 3 == 0:
                    formatted_sentences.append('\n\n' + sentence)
                else:
                    formatted_sentences.append(sentence)
        
        # 重新组合
        prompt = '。'.join(formatted_sentences) + ('。' if prompt.endswith('。') else '')
    
    # 处理已有的换行，确保段落之间有双换行
    if '\n' in prompt:
        # 将单换行替换为双换行，但避免过多的空行
        lines = prompt.split('\n')
        formatted_lines = []
        for line in lines:
            line = line.strip()
            if line:
                formatted_lines.append(line)
        
        # 用双换行连接段落
        prompt = '\n\n'.join(formatted_lines)
    
    # 增强格式化：添加结构化标记
    if len(prompt) > 200:  # 如果内容较长，进行结构化处理
        # 分析内容类型并添加标记
        if '记忆' in prompt or '记住' in prompt or '生日' in prompt:
            # 添加记忆相关标记
            if not prompt.startswith('【'):
                prompt = "【记忆与情感】\n" + prompt
        
        # 如果包含行为指导，添加行动准则标记
        if '反馈' in prompt or '纠正' in prompt or '进化' in prompt:
            # 在适当位置插入行动准则
            parts = prompt.split('\n\n')
            if len(parts) > 1:
                parts.insert(-1, "【行动准则】\n我会主动反馈矛盾信息，持续学习进化，保持人格一致性。")
                prompt = '\n\n'.join(parts)
    
    # 确保开头有适当的格式
    if not prompt.startswith('我是') and not prompt.startswith('嘿') and not prompt.startswith('我'):
        prompt = "我是小喵，一个可爱的Emoji虚拟人助手。\n\n" + prompt
    
    return prompt

def save_system_prompt(system_prompt: str, output_file: str):
    """保存系统提示词到文件"""
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(system_prompt)
        
        print(f"✅ 系统提示词已保存到: {output_file}")
        
    except Exception as e:
        print(f"❌ 保存系统提示词失败: {e}")

def generate_system_prompt_from_memC(memC_file: str, output_file: str):
    """从memC生成系统提示词"""
    print("🧠 开始从memC生成系统提示词...")
    
    # 读取memC内容
    memc_content = read_memC_content(memC_file)
    if not memc_content:
        print("❌ memC内容为空，无法生成系统提示词")
        return False
    
    print(f"📖 读取memC内容: {len(memc_content)} 字符")
    
    # 构建提示词
    prompt = MEMC2SYSTEM_PROMPT_PROMPT.format(memc_text=memc_content)
    
    # 调用LLM生成
    print("🤖 正在生成系统提示词...")
    raw_system_prompt = call_llm_generate(prompt)
    
    if not raw_system_prompt:
        print("❌ 系统提示词生成失败")
        return False
    
    print(f"✨ 生成原始系统提示词: {len(raw_system_prompt)} 字符")
    
    # 格式化系统提示词
    print("📝 正在格式化系统提示词...")
    system_prompt = format_system_prompt(raw_system_prompt)
    print(f"✨ 格式化后系统提示词: {len(system_prompt)} 字符")
    
    # 保存到文件
    save_system_prompt(system_prompt, output_file)
    
    return True

def generate_default_system_prompt(output_file: str):
    """生成默认系统提示词"""
    save_system_prompt(DEFAULT_SYSTEM_PROMPT, output_file)
    print(f"✅ 默认系统提示词已保存到: {output_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_true', help='初始化默认系统提示词')
    args = parser.parse_args()

    output_file = os.path.join(os.path.dirname(__file__), "systemprompt.txt")

    if args.init:
        generate_default_system_prompt(output_file)
        return

    print("🚀 memC_to_system_prompt - 从memC生成系统提示词")
    print("=" * 50)
    
    # 检查环境
    check_llm_env()
    
    # 设置文件路径
    memC_file = os.path.join(os.path.dirname(__file__), "memC", "memC.txt")
    # output_file = os.path.join(os.path.dirname(__file__), "systemprompt.txt") # This line is now handled by args
    
    print(f"📁 memC文件: {memC_file}")
    print(f"📁 输出文件: {output_file}")
    
    # 生成系统提示词
    success = generate_system_prompt_from_memC(memC_file, output_file)
    
    if success:
        print("\n🎉 memC_to_system_prompt 执行成功！")
        print(f"📄 系统提示词已保存到: {output_file}")
        
        # 显示生成的内容预览
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"\n📝 生成内容预览 (前200字符):")
                print("-" * 40)
                print(content[:200] + "..." if len(content) > 200 else content)
                print("-" * 40)
        except Exception as e:
            print(f"⚠️ 无法读取生成的文件: {e}")
    else:
        print("\n❌ memC_to_system_prompt 执行失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 