#!/bin/bash
# 快捷运行 MemABC encoding_B2C 冥想程序脚本
# 用法：bash b2c.sh

cd "$(dirname "$0")"/..
echo "[B2C] 启动 MemABC encoding_B2C 冥想程序流程..."
echo "[B2C] 激活虚拟环境..."
source venv/bin/activate
echo "[B2C] 开始执行 encoding_b2c.py ..."
PYTHONPATH=. python3 MemABC/encoding_b2c.py
status=$?
if [ $status -eq 0 ]; then
  echo "[B2C] encoding_b2c.py 执行完成！"
else
  echo "[B2C] encoding_b2c.py 执行失败，退出码: $status"
fi 