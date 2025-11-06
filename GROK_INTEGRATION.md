# Grok API Integration for Image-to-Video

This integration adds support for using xAI's Grok API to generate videos from images, replacing the WAN model for image-to-video tasks.

## ⚠️ Important Disclaimer

**This integration is a template/framework implementation.** The actual xAI Grok API endpoints and structure for image-to-video generation may differ from this implementation. 

**Before using in production:**

1. ✅ Verify the actual Grok API endpoint for image-to-video generation with [xAI's official documentation](https://docs.x.ai/docs/overview)
2. ✅ Update the request payload structure in `wan/grok_i2v.py` to match official specs
3. ✅ Adjust response parsing logic based on actual API response format
4. ✅ Test thoroughly with real API credentials
5. ✅ Monitor for API changes and updates from xAI

This code serves as a starting point and may require adjustments based on the official API specification. The interface is designed to be easily adaptable once full API details are available.

## Overview

The Grok API integration (`grok-i2v`) allows you to leverage xAI's Grok model for image-to-video generation through a simple API interface. This provides an alternative to the local WAN model, with the following benefits:

- **Cloud-based processing**: No need for local GPU resources
- **API-driven**: Simple HTTP API calls for video generation
- **Scalable**: Leverages xAI's infrastructure

## Setup

### 1. Get Your API Key

1. Sign up at the [xAI Console](https://console.x.ai/)
2. Generate your API key
3. Set the API key as an environment variable:

```bash
export XAI_API_KEY="your_api_key_here"
```

### 2. Install Dependencies

Make sure you have the required dependencies installed:

```bash
pip install requests>=2.31.0
```

All other dependencies should already be installed from the main requirements.txt.

## Usage

### Basic Example

Generate a video from an image using the Grok API:

```bash
python generate.py \
  --task grok-i2v \
  --size 1280*720 \
  --image examples/i2v_input.JPG \
  --prompt "Transform this image into a dynamic video with smooth motion and cinematic quality"
```

### Command Line Options

The `grok-i2v` task supports the same command-line options as the regular `i2v-14B` task:

- `--task grok-i2v`: Specify the Grok I2V task
- `--size`: Video resolution (e.g., `1280*720`, `832*480`)
- `--image`: Path to the input image
- `--prompt`: Description for the video generation
- `--frame_num`: Number of frames to generate (default: 81)
- `--sample_guide_scale`: Guidance scale for generation (default: 5.0)
- `--base_seed`: Random seed for reproducibility

### Example with Custom Parameters

```bash
XAI_API_KEY="your_key" python generate.py \
  --task grok-i2v \
  --size 1280*720 \
  --image path/to/your/image.jpg \
  --prompt "A beautiful sunset scene coming to life with gentle movements" \
  --frame_num 81 \
  --sample_guide_scale 5.0 \
  --base_seed 42
```

### Supported Resolutions

The Grok I2V integration supports the following resolutions:
- `1280*720` (720P)
- `720*1280` (720P portrait)
- `832*480` (480P)
- `480*832` (480P portrait)

## API Configuration

### Environment Variables

- `XAI_API_KEY` (required): Your xAI API key
- `XAI_API_URL` (optional): Custom API endpoint URL (default: `https://api.x.ai/v1`)

### Advanced Configuration

You can customize the Grok model and API endpoint by modifying the initialization in the code:

```python
from wan import GrokI2V

grok_i2v = GrokI2V(
    api_key="your_api_key",
    api_url="https://api.x.ai/v1",
    model="grok-2-vision-1212",  # Customize model version
)
```

## Comparison: Grok I2V vs WAN I2V

| Feature | Grok I2V | WAN I2V |
|---------|----------|---------|
| GPU Required | No | Yes |
| Processing Location | Cloud | Local |
| Model Size | N/A | 14B parameters |
| Cost | API usage fees | Free (self-hosted) |
| Customization | Limited | Full control |
| Setup Complexity | Simple | Requires model download |

## Troubleshooting

### API Key Error

If you see an error about missing API key:
```
ValueError: API key is required. Set XAI_API_KEY environment variable or pass api_key parameter.
```

Make sure you've set the `XAI_API_KEY` environment variable:
```bash
export XAI_API_KEY="your_api_key_here"
```

### Connection Issues

If you experience connection issues:
1. Check your internet connection
2. Verify the API endpoint is accessible
3. Check if your API key is valid
4. Review the xAI API status page

### Video Quality Issues

If the generated video quality doesn't meet expectations:
- Try adjusting the `--sample_guide_scale` parameter (range: 1.0 to 10.0)
- Provide more detailed prompts
- Experiment with different seeds using `--base_seed`

### API Structure Mismatch

If you encounter errors like "No video URL found in API response" or HTTP 400/404 errors:

This likely means the API structure has changed or differs from the template implementation. To fix:

1. Check the [official xAI API documentation](https://docs.x.ai/docs/overview)
2. Update the endpoint URL in `wan/grok_i2v.py` (line ~189)
3. Adjust the request payload structure (lines ~155-178)
4. Modify the response parsing logic in `_extract_video_from_response()` (lines ~218-244)

The code includes detailed comments marking these areas for easy updates.

## Technical Details

### Implementation Notes

**This implementation is a template.** Key areas that may need adjustment:

#### 1. API Endpoint (Line ~189 in grok_i2v.py)
Current: `f"{self.api_url}/chat/completions"`

Possible alternatives based on common API patterns:
- `f"{self.api_url}/video/generate"`
- `f"{self.api_url}/v1/images/animate"`
- `f"{self.api_url}/v1/media/generate"`

#### 2. Request Payload (Lines ~155-178)
The payload structure is based on common multimodal API patterns. You may need to adjust:
- Parameter names (e.g., `video_config` might be `video_settings`)
- Structure (flat vs nested parameters)
- Required vs optional fields

#### 3. Response Format (Lines ~218-244)
The code attempts to extract video URLs from multiple common response patterns:
```python
response['choices'][0]['message']['video_url']
response['video_url']
response['data']['url']
```

Update `_extract_video_from_response()` to match the actual response format.

### Implementation Structure

The Grok I2V integration is implemented in `wan/grok_i2v.py` and provides:

1. **API Client**: Handles authentication and HTTP requests to the Grok API
2. **Image Processing**: Converts PIL Images to API-compatible formats
3. **Video Conversion**: Downloads and converts API responses to PyTorch tensors
4. **Error Handling**: Robust error handling for network and API issues

### Output Format

The generated video is returned as a PyTorch tensor with shape `(frame_num, C, H, W)` where:
- `frame_num`: Number of frames (default: 81)
- `C`: Color channels (3 for RGB)
- `H`: Height in pixels
- `W`: Width in pixels

Values are normalized to the range `[-1, 1]`.

## Known Limitations

1. **Template Implementation**: The actual Grok image-to-video API endpoint structure may differ from the current implementation. This code serves as a template that requires verification against official API documentation.

2. **Response Format**: The video extraction logic assumes certain response structures. Adjustments may be needed based on the actual API response format.

3. **Rate Limiting**: API usage may be subject to rate limits. Implement appropriate retry logic for production use.

4. **Cost**: Unlike the local WAN model, using the Grok API incurs costs based on usage.

## Future Enhancements

Potential improvements for this integration:

- [ ] Add streaming support for real-time video generation
- [ ] Implement caching for repeated requests
- [ ] Add batch processing for multiple images
- [ ] Support for custom video effects and transitions
- [ ] Integration with Grok's advanced video editing features

## References

- [xAI API Documentation](https://docs.x.ai/docs/overview)
- [xAI Console](https://console.x.ai/)
- [Grok API Pricing](https://x.ai/api)

## Support

For issues related to:
- **Grok API**: Contact xAI support or check their documentation
- **Integration code**: Open an issue in this repository
- **WAN model**: Refer to the main README.md

## License

This integration follows the same license as the main Wan2.1 repository (Apache 2.0 License).
