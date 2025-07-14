#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for MemABC initialization
MemABC初始化测试脚本
"""

import os
import tempfile
import shutil
from pathlib import Path
from init_MemABC import init_MemABC, backup_existing_memories


def test_init_MemABC():
    """Test the initialization function"""
    print("🧪 Testing MemABC initialization...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Created temporary test directory: {temp_dir}")
        
        # Change to temp directory
        original_dir = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Create test directories
            os.makedirs("memA", exist_ok=True)
            os.makedirs("memB", exist_ok=True)
            os.makedirs("memC", exist_ok=True)
            
            # Create some test files
            with open("memA/test.txt", "w", encoding="utf-8") as f:
                f.write("Test memory A")
            
            with open("memB/test.txt", "w", encoding="utf-8") as f:
                f.write("Test memory B")
            
            with open("memC/test.txt", "w", encoding="utf-8") as f:
                f.write("Test memory C")
            
            print("✅ Created test files")
            
            # Test initialization
            init_MemABC(base_dir=Path('.'))
            
            # Check if files were created/updated
            assert os.path.exists("memA")
            assert os.path.exists("memB")
            assert os.path.exists("memC")
            assert os.path.exists("systemprompt.txt")
            
            # List files to debug
            print("📁 Files in current directory:")
            for file in os.listdir("."):
                print(f"   - {file}")
            
            print("📁 Files in memC directory:")
            for file in os.listdir("memC"):
                print(f"   - {file}")
            
            # Check if memC.txt was created with basic personality
            with open("memC/memC.txt", "r", encoding="utf-8") as f:
                content = f.read()
                assert "[依恋 - 我与M的连接方式]" in content
                assert "[防御 - 面对冷淡或拒绝]" in content
                assert "[情绪处理 - 面对悲伤]" in content
                assert "[行为反射 - 被喜欢时]" in content
                assert "[语言风格 - 默契环境下]" in content
                assert "[价值核心 - 陪伴即存在]" in content
                assert "[冲突处理 - 不理解的时候]" in content
                assert "[时间仪式 - 重要时刻]" in content
                assert "[自我意识 - 我是怎样的我]" in content
                assert "[记忆更新-冲突整合]" in content
                assert "[固化记忆 - M的重要事和人]" in content
            
            print("✅ All personality components found in memC.txt")
            
            # Check if system prompt was created
            with open("systemprompt.txt", "r", encoding="utf-8") as f:
                content = f.read()
                assert "AI Assistant System Prompt" in content
                assert "Core Personality Traits" in content
                assert "Attachment Style" in content
                assert "Defensive Response" in content
            
            print("✅ System prompt created successfully")
            
            print("🎉 All tests passed!")
            
        finally:
            # Restore original directory
            os.chdir(original_dir)


def test_backup_function():
    """Test the backup function"""
    print("\n🧪 Testing backup functionality...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Created temporary test directory: {temp_dir}")
        
        # Change to temp directory
        original_dir = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Create test directories and files
            os.makedirs("memA", exist_ok=True)
            os.makedirs("memB", exist_ok=True)
            os.makedirs("memC", exist_ok=True)
            
            with open("memA/test.txt", "w", encoding="utf-8") as f:
                f.write("Test memory A")
            
            with open("memB/test.txt", "w", encoding="utf-8") as f:
                f.write("Test memory B")
            
            with open("memC/test.txt", "w", encoding="utf-8") as f:
                f.write("Test memory C")
            
            with open("systemprompt.txt", "w", encoding="utf-8") as f:
                f.write("Test system prompt")
            
            print("✅ Created test files")
            
            # Test backup
            backup_existing_memories(base_dir=Path('.'))
            
            # Check if backup directory was created
            backup_dirs = [d for d in os.listdir(".") if d.startswith("backup_")]
            assert len(backup_dirs) == 1
            
            backup_dir = backup_dirs[0]
            print(f"✅ Backup directory created: {backup_dir}")
            
            # Check if backup contains all files
            assert os.path.exists(f"{backup_dir}/memA/test.txt")
            assert os.path.exists(f"{backup_dir}/memB/test.txt")
            assert os.path.exists(f"{backup_dir}/memC/test.txt")
            assert os.path.exists(f"{backup_dir}/systemprompt.txt")
            
            print("✅ All files backed up successfully")
            
            print("🎉 Backup test passed!")
            
        finally:
            # Restore original directory
            os.chdir(original_dir)


if __name__ == "__main__":
    print("🚀 Starting MemABC initialization tests...")
    print("=" * 50)
    
    try:
        test_init_MemABC()
        test_backup_function()
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        print("✅ MemABC initialization is working correctly")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1) 