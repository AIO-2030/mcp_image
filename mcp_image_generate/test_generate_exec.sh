#!/bin/bash

# 测试图像生成功能
echo "测试图像生成功能..."

# 确保在正确的目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查可执行文件是否存在
if [ ! -f "dist/image_stdio" ]; then
    echo "错误：找不到 image_stdio 可执行文件"
    echo "请先运行 python build.py 构建可执行文件"
    exit 1
fi

# 构建测试请求
REQUEST='{
    "jsonrpc": "2.0",
    "method": "generate_image",
    "params": {
        "prompt": "an island near sea, with seagulls, moon shining over the sea, light house, boats in the background, fish flying over the sea",
        "negative_prompt": "blurry, low quality",
        "num_inference_steps": 20,
        "guidance_scale": 7.5,
        "seed": 4999999999,
        "image_size": "1024x1024"
    },
    "id": 1
}'

# 发送请求到 stdio 服务器
echo "$REQUEST" | ./dist/image_stdio

# 检查退出状态
if [ $? -eq 0 ]; then
    echo "测试成功完成"
else
    echo "测试失败"
    exit 1
fi 