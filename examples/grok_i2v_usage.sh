#!/usr/bin/env bash
# Example usage script for Grok I2V integration
# This script demonstrates how to use the Grok API for image-to-video generation

# Exit on error
set -e

echo "========================================"
echo "Grok I2V Integration - Usage Examples"
echo "========================================"
echo ""

# Check if API key is set
if [ -z "$XAI_API_KEY" ]; then
    echo "⚠️  Warning: XAI_API_KEY environment variable is not set"
    echo ""
    echo "To use the Grok API, you need to set your API key:"
    echo "  export XAI_API_KEY='your_api_key_here'"
    echo ""
    echo "Get your API key from: https://console.x.ai/"
    echo ""
    exit 1
fi

echo "✓ XAI_API_KEY is set"
echo ""

# Example 1: Basic usage with default settings
echo "Example 1: Basic image-to-video generation"
echo "-------------------------------------------"
echo "Command:"
echo "python generate.py \\"
echo "  --task grok-i2v \\"
echo "  --size 1280*720 \\"
echo "  --image examples/i2v_input.JPG \\"
echo "  --prompt 'Transform this image into a dynamic video'"
echo ""

# Example 2: Custom parameters
echo "Example 2: With custom parameters"
echo "----------------------------------"
echo "Command:"
echo "python generate.py \\"
echo "  --task grok-i2v \\"
echo "  --size 832*480 \\"
echo "  --image path/to/your/image.jpg \\"
echo "  --prompt 'A beautiful sunset scene with gentle motion' \\"
echo "  --frame_num 81 \\"
echo "  --sample_guide_scale 7.0 \\"
echo "  --base_seed 42"
echo ""

# Example 3: Portrait orientation
echo "Example 3: Portrait orientation video"
echo "--------------------------------------"
echo "Command:"
echo "python generate.py \\"
echo "  --task grok-i2v \\"
echo "  --size 720*1280 \\"
echo "  --image portrait.jpg \\"
echo "  --prompt 'Animate this portrait with subtle movements'"
echo ""

echo "========================================"
echo "For more details, see GROK_INTEGRATION.md"
echo "========================================"
