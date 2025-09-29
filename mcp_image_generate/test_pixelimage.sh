#!/bin/bash

# 测试脚本：text_pixelimage.sh
# 用于测试 pixel_image_generate 方法

echo "=== 像素表情符号图片生成测试 ==="
echo

# 设置测试参数
API_KEY="sk-sizdciquzgledafoqeguebohudunufoztppywmclondftwij"
SERVER_SCRIPT="stdio_server.py"

# 检查服务器脚本是否存在
if [ ! -f "$SERVER_SCRIPT" ]; then
    echo "错误: 找不到 $SERVER_SCRIPT 文件"
    exit 1
fi

# 测试用例数组
declare -a test_cases=(
    "我今天好累"
    "好开心！"
    "生气的猫"
    "I want a cute dog"
    "想要一个可爱的熊猫"
    "悲伤的表情"
    "惊讶的脸"
    "愤怒的机器人"
)

echo "开始测试 pixel_image_generate 方法..."
echo "测试用例数量: ${#test_cases[@]}"
echo

# 测试 help 方法
echo "1. 测试 help 方法:"
echo "请求:"
echo '{"jsonrpc": "2.0", "method": "help", "params": {}, "id": 1}'
echo
echo "响应:"
echo '{"jsonrpc": "2.0", "method": "help", "params": {}, "id": 1}' | python3 $SERVER_SCRIPT
echo
echo "----------------------------------------"
echo

# 测试每个像素表情符号生成用例
for i in "${!test_cases[@]}"; do
    test_input="${test_cases[$i]}"
    test_id=$((i + 2))
    
    echo "$((i + 2)). 测试用例 $((i + 1)): '$test_input'"
    echo "请求:"
    
    # 构建 JSON-RPC 请求
    request_json=$(cat <<EOF
{
    "jsonrpc": "2.0",
    "method": "pixel_image_generate",
    "params": {
        "user_input": "$test_input",
        "image_size": "512x512",
        "num_inference_steps": 15,
        "guidance_scale": 7.0
    },
    "id": $test_id
}
EOF
)
    
    echo "$request_json"
    echo
    echo "响应:"
    
    # 发送请求并获取响应
    response=$(echo "$request_json" | python3 $SERVER_SCRIPT)
    
    # 检查响应是否包含错误
    if echo "$response" | grep -q '"error"'; then
        echo "❌ 错误响应:"
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    else
        echo "✅ 成功响应:"
        # 尝试格式化 JSON 输出
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
        
        # 检查是否包含图片数据
        if echo "$response" | grep -q '"image_base64"'; then
            echo "📸 图片生成成功！"
        else
            echo "⚠️  响应中未找到图片数据"
        fi
    fi
    
    echo
    echo "----------------------------------------"
    echo
done

echo "测试完成！"
echo
echo "注意事项："
echo "- 确保 API 密钥有效"
echo "- 确保网络连接正常"
echo "- 生成的图片以 base64 格式返回"
echo "- 可以通过 base64 解码保存为图片文件"
