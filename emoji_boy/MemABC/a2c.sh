#!/bin/bash
# 快捷运行 MemABC encoding_A2C 极重要信息提取脚本
# 用法：bash a2c.sh

cd "$(dirname "$0")"/..
echo "[A2C] 启动 MemABC encoding_A2C 极重要信息提取流程..."
echo "[A2C] 激活虚拟环境..."
source venv/bin/activate
echo "[A2C] 开始执行 encoding_a2c.py ..."
PYTHONPATH=. python3 MemABC/encoding_a2c.py
status=$?
if [ $status -eq 0 ]; then
  echo "[A2C] encoding_a2c.py 执行完成！"
else
  echo "[A2C] encoding_a2c.py 执行失败，退出码: $status"
fi 