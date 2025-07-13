"""
encoding_A2C: 分析 memA 聊天记录，抓取极为重要的信息，智能合并到 memC/memC.txt。
- 使用 LLM 将新信息与现有 memC 内容进行智能合并
- 自动进行去重、归纳和逻辑重组
- 保持 memC.txt 结构（# memC记忆 标志必须保留在首行）
- 跳过 memA 文件头部 '# memA记忆' 标志
- 使用 LLM 精炼，提示词专为"极为重要信息"提取和合并设计
"""
import os
import sys
from pathlib import Path

# 添加父目录到Python路径，以便导入core模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.llm_client import LLMClient

# 提取极为重要信息的提示词
A2C_EXTRACT_PROMPT = (
    "你是对话记录里的'ai'，请以'ai'第一人称视角，从以下聊天记录中只抓取极为重要、对AI长期行为和个性有深远影响的信息，尤其要关注重要的人的重要的事"
    "请丢弃一切琐碎、重复、无关内容，只保留对AI世界观、价值观、行为模式、重大事件等有决定性影响的内容。"
    "输出内容必须简洁、精炼，对于无重复的内容直接追加到memC.txt，且不能改变memC.txt原有结构。"
    "每次综合内容时，总是检查整个内容，对内容进行去重，重组."
    "不要输出任何格式头，只输出内容本身。"
)

# 合并和去重的提示词
A2C_MERGE_PROMPT = (
    "你是AI记忆管理专家，请将新的重要信息与现有的核心记忆进行智能合并。"
    "重要要求："
    "1. 必须保留现有核心记忆中的所有重要信息，不能丢失任何现有内容"
    "2. 将新的重要信息添加到现有记忆中"
    "3. 对重复或相似的信息进行去重和归纳"
    "4. 保持原有的结构化格式，每个记忆条目用换行分隔"
    "5. 保持信息的完整性和重要性"
    "6. 输出内容要清晰易读，保持原有的层次结构"
    "7. 不要输出任何格式头，只输出合并后的内容本身"
    "8. 如果新信息与现有信息冲突，优先保留更重要的信息"
    "9. 确保最终输出包含所有独特的重要信息"
    "10. 保持原有的换行和段落结构，不要将所有内容压缩成一行"
    "现有核心记忆：\n{existing_content}\n\n新的重要信息：\n{new_content}"
)

def check_llm_env():
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("HUGGINGFACE_API_KEY")
    if not api_key:
        print("❌ 未检测到 LLM API 令牌 (OPENAI_API_KEY 或 HUGGINGFACE_API_KEY)，请先配置环境变量！")
        sys.exit(1)

def call_llm_extract(summary_prompt, raw_text):
    llm = LLMClient()
    if raw_text:
        prompt = summary_prompt + "\n" + raw_text
    else:
        prompt = summary_prompt
    return llm.get_response(prompt)

def call_llm_merge(merge_prompt):
    """
    专门用于合并内容的LLM调用函数
    """
    llm = LLMClient()
    return llm.get_response(merge_prompt)

def update_memC(memC_file, new_content):
    """
    使用LLM将新内容与现有memC内容合并，进行去重和归纳。
    """
    # 检查文件是否存在
    if not os.path.exists(memC_file):
        # 确保目录存在
        os.makedirs(os.path.dirname(memC_file), exist_ok=True)
        # 创建新文件并写入内容
        with open(memC_file, 'w', encoding='utf-8') as f:
            f.write('# memC记忆\n')
            f.write(new_content.strip() + '\n')
        return
    
    # 读取现有memC内容
    try:
        with open(memC_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        # 备份原文件
        backup_file = memC_file + '.backup'
        try:
            import shutil
            shutil.copy2(memC_file, backup_file)
        except Exception as backup_e:
            pass
        raise
    
    # 保证首行为 # memC记忆
    if not lines or not lines[0].strip().startswith('# memC记忆'):
        # 尝试修复文件格式
        existing_content = ''.join(lines).strip()
        if existing_content:
            # 如果文件有内容但没有正确头部，添加头部
            with open(memC_file, 'w', encoding='utf-8') as f:
                f.write('# memC记忆\n')
                f.write(existing_content + '\n')
        else:
            # 如果文件为空，直接写入新内容
            with open(memC_file, 'w', encoding='utf-8') as f:
                f.write('# memC记忆\n')
                f.write(new_content.strip() + '\n')
            return
    
    # 提取现有内容（跳过首行标志）
    existing_content = ''.join(lines[1:]).strip()
    
    if not existing_content:
        # 如果现有内容为空，直接使用新内容
        merged_content = new_content.strip()
    else:
        # 使用LLM合并现有内容和新内容
        merge_prompt = A2C_MERGE_PROMPT.format(
            existing_content=existing_content,
            new_content=new_content
        )
        
        try:
            merged_content = call_llm_merge(merge_prompt)
            
            # 验证LLM响应质量
            if not merged_content or len(merged_content.strip()) < 10:
                # 如果LLM返回内容有问题，使用智能备选合并
                merged_content = smart_merge_fallback(existing_content, new_content)
                
        except Exception as e:
            # 如果LLM失败，使用智能备选合并
            merged_content = smart_merge_fallback(existing_content, new_content)
    
    # 验证合并结果
    if existing_content and new_content:
        # 检查合并结果是否包含足够的内容
        if len(merged_content.strip()) < max(len(existing_content), len(new_content)) * 0.5:
            merged_content = smart_merge_fallback(existing_content, new_content)
        
        # 检查结构完整性
        existing_lines = existing_content.strip().split('\n')
        merged_lines = merged_content.strip().split('\n')
        
        # 如果合并后的行数明显少于原有行数，可能结构被破坏了
        if len(merged_lines) < len(existing_lines) * 0.7:
            merged_content = smart_merge_fallback(existing_content, new_content)
        
        # 检查是否所有内容被压缩成一行
        if len(merged_lines) <= 2 and len(merged_content.strip()) > 100:
            merged_content = smart_merge_fallback(existing_content, new_content)
    
    # 备份原文件
    backup_file = memC_file + '.backup'
    try:
        import shutil
        shutil.copy2(memC_file, backup_file)
    except Exception as e:
        pass
    
    # 写入合并后的内容
    try:
        with open(memC_file, 'w', encoding='utf-8') as f:
            f.write('# memC记忆\n')
            f.write(merged_content.strip() + '\n')
    except Exception as e:
        # 尝试恢复备份
        try:
            shutil.copy2(backup_file, memC_file)
        except Exception as restore_e:
            pass
        raise

def smart_merge_fallback(existing_content, new_content):
    """
    智能备选合并策略，保持原有结构
    """
    # 分析现有内容的结构
    existing_lines = existing_content.strip().split('\n')
    new_lines = new_content.strip().split('\n')
    
    # 检查新内容是否与现有内容重复
    new_unique_content = []
    for new_line in new_lines:
        if new_line.strip() and new_line.strip() not in existing_content:
            new_unique_content.append(new_line.strip())
    
    if not new_unique_content:
        return existing_content
    
    # 将新内容添加到现有内容后面，保持结构
    result = existing_content.strip()
    if result:
        result += "\n\n"
    result += "\n".join(new_unique_content)
    
    return result

def encode_and_append_memA2C(memA_path, memC_file):
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
        return
    new_raw = '\n'.join(all_new_text)
    # LLM 精炼极为重要信息
    new_important = call_llm_extract(A2C_EXTRACT_PROMPT, new_raw)
    # 用新内容整体覆盖 memC.txt
    update_memC(memC_file, new_important)

if __name__ == "__main__":
    check_llm_env()
    memA_dir = os.path.join(os.path.dirname(__file__), 'memA')
    memC_file = os.path.join(os.path.dirname(__file__), 'memC', 'memC.txt')
    encode_and_append_memA2C(memA_dir, memC_file) 