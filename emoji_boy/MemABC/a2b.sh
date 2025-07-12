#!/bin/bash
# 快捷运行 MemABC encoding_A2B 精炼合并脚本
# 用法：bash quick_encode_A2B.sh

cd "$(dirname "$0")"/..
echo "[A2B] 启动 MemABC encoding_a2b 精炼合并流程..."
echo "[A2B] 激活虚拟环境..."
source venv/bin/activate
echo "[A2B] 开始执行 encoding_a2b.py ..."
PYTHONPATH=. python3 MemABC/encoding_a2b.py
status=$?
if [ $status -eq 0 ]; then
  echo "[A2B] encoding_a2b.py 执行完成！"
else
  echo "[A2B] encoding_a2b.py 执行失败，退出码: $status"
fi 