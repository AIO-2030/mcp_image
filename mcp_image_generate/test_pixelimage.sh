#!/bin/bash

# 测试脚本：text_pixelimage.sh
# 用于测试 pixel_image_generate 方法

# 切换到脚本所在目录
cd "$(dirname "$0")"

echo "=== 像素表情符号图片生成测试 ==="
echo "当前目录: $(pwd)"
echo

# 设置测试参数
API_KEY="sk-sizdciquzgledafoqeguebohudunufoztppywmclondftwij"
SERVER_SCRIPT="stdio_server.py"
TEST_DIR="test"

# 创建测试目录
if [ ! -d "$TEST_DIR" ]; then
    echo "创建测试目录: $TEST_DIR"
    mkdir -p "$TEST_DIR"
fi

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
    echo "正在发送请求..."
    response=$(echo "$request_json" | python3 $SERVER_SCRIPT 2>&1)
    
    # 保存原始响应到文件用于调试
    echo "$response" > "debug_response_${test_id}.json"
    echo "原始响应已保存到: debug_response_${test_id}.json"
    
    # 显示响应的前几行用于快速调试
    echo "响应前5行:"
    echo "$response" | head -5
    echo "..."
    
    # 检查响应是否包含错误
    if echo "$response" | grep -q '"error"'; then
        echo "❌ 错误响应:"
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    else
        echo "✅ 成功响应:"
        # 尝试格式化 JSON 输出
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
        
        # 显示响应结构用于调试
        echo "🔍 响应结构分析:"
        echo "$response" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    def print_structure(obj, indent=0):
        spaces = '  ' * indent
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    print(f'{spaces}{key}: {type(value).__name__}')
                    print_structure(value, indent + 1)
                else:
                    print(f'{spaces}{key}: {type(value).__name__}')
        elif isinstance(obj, list):
            print(f'{spaces}[list with {len(obj)} items]')
            if obj:
                print_structure(obj[0], indent + 1)
    print_structure(data)
except Exception as e:
    print(f'Error analyzing structure: {e}')
"
        
        # 检查是否包含图片数据并保存
        if echo "$response" | grep -q '"image_base64"'; then
            echo "📸 图片生成成功！"
            
            # 提取 base64 图片数据并保存
            image_base64=$(echo "$response" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    # 调试：打印整个响应的结构
    print('Full response keys:', list(data.keys()), file=sys.stderr)
    
    # 尝试不同的可能结构
    if 'output' in data and 'image_base64' in data['output']:
        print(data['output']['image_base64'])
    elif 'result' in data and 'image_base64' in data['result']:
        print(data['result']['image_base64'])
    elif 'image_base64' in data:
        print(data['image_base64'])
    elif 'data' in data and 'image_base64' in data['data']:
        print(data['data']['image_base64'])
    else:
        # 递归搜索 image_base64 字段
        def find_image_base64(obj, path=''):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == 'image_base64':
                        return value
                    elif isinstance(value, (dict, list)):
                        result = find_image_base64(value, f'{path}.{key}' if path else key)
                        if result:
                            return result
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    result = find_image_base64(item, f'{path}[{i}]' if path else f'[{i}]')
                    if result:
                        return result
            return None
        
        result = find_image_base64(data)
        if result:
            print(result)
        else:
            print('image_base64 not found in any location', file=sys.stderr)
            print('')
except Exception as e:
    print('Error:', str(e), file=sys.stderr)
    print('')
")
            
            # 调试信息
            echo "🔍 调试: 提取到的 base64 数据长度: ${#image_base64}"
            
            if [ -n "$image_base64" ]; then
                # 生成文件名（使用测试输入的前几个字符，替换特殊字符）
                safe_filename=$(echo "$test_input" | sed 's/[^a-zA-Z0-9\u4e00-\u9fff]/_/g' | cut -c1-20)
                image_filename="${TEST_DIR}/pixel_${safe_filename}_${test_id}.png"
                
                # 解码并保存图片
                echo "$image_base64" | base64 -d > "$image_filename"
                
                if [ -f "$image_filename" ]; then
                    echo "💾 图片已保存到: $image_filename"
                else
                    echo "❌ 图片保存失败"
                fi
            else
                echo "⚠️  无法提取图片数据"
            fi
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
echo "- 生成的图片已自动保存到 $TEST_DIR 目录"
echo "- 图片文件名格式: pixel_[描述]_[ID].png"
echo "- 可以通过图片查看器打开保存的图片文件"
