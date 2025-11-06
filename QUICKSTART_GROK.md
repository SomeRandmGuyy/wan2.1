# Quick Start: Grok API Integration

Get started with Grok API image-to-video generation in 5 minutes!

## ⚠️ Important Note

This is a template implementation. Verify against [xAI's official documentation](https://docs.x.ai/docs/overview) before production use.

## Step 1: Get API Key (2 minutes)

1. Visit [xAI Console](https://console.x.ai/)
2. Sign up or log in
3. Generate your API key
4. Copy the key (you'll need it in Step 3)

## Step 2: Install Dependencies (1 minute)

```bash
cd wan2.1
pip install requests>=2.31.0
```

That's it! No GPU required, no model downloads needed.

## Step 3: Set API Key (30 seconds)

```bash
export XAI_API_KEY="your_api_key_here"
```

## Step 4: Generate Your First Video (1 minute)

### Using Default Example
```bash
python generate.py \
  --task grok-i2v \
  --size 1280*720
```

This uses the default example image and prompt.

### Using Your Own Image
```bash
python generate.py \
  --task grok-i2v \
  --size 1280*720 \
  --image path/to/your/image.jpg \
  --prompt "Your creative prompt here"
```

## Example Prompts

Try these prompts with your images:

**Nature/Landscape:**
```bash
--prompt "Transform this scene with gentle wind and flowing water, golden hour lighting"
```

**Portrait:**
```bash
--prompt "Animate this portrait with subtle breathing and natural eye movements"
```

**Action:**
```bash
--prompt "Bring this scene to life with dynamic motion and cinematic camera movement"
```

**Creative:**
```bash
--prompt "Add magical sparkles and dreamy atmosphere to this scene"
```

## Common Parameters

```bash
--task grok-i2v              # Use Grok API (required)
--size 1280*720              # Video resolution (720P)
--image input.jpg            # Your input image
--prompt "your prompt"       # Description for generation
--frame_num 81               # Number of frames (default: 81)
--sample_guide_scale 5.0     # Guidance strength (1-10)
--base_seed 42               # For reproducible results
```

## Supported Resolutions

Choose from:
- `1280*720` (720P landscape)
- `720*1280` (720P portrait)
- `832*480` (480P landscape)
- `480*832` (480P portrait)

## Troubleshooting

### "API key is required" error
Make sure you've set the environment variable:
```bash
export XAI_API_KEY="your_actual_key"
echo $XAI_API_KEY  # Verify it's set
```

### Connection issues
1. Check your internet connection
2. Verify your API key is valid
3. Try again in a few minutes

### API structure mismatch
If you see errors about response parsing, the API structure may differ from this template. See [GROK_INTEGRATION.md](GROK_INTEGRATION.md) for details on updating the code.

## Switching Between Models

**Use Grok API:** (no GPU needed)
```bash
python generate.py --task grok-i2v --image input.jpg
```

**Use WAN Model:** (requires GPU and model download)
```bash
python generate.py --task i2v-14B --ckpt_dir ./Wan2.1-I2V-14B-720P --image input.jpg
```

Same interface, different backends!

## Next Steps

### Learn More
- **Full Guide:** [GROK_INTEGRATION.md](GROK_INTEGRATION.md)
- **Comparison:** [COMPARISON.md](COMPARISON.md) - WAN vs Grok
- **Complete Summary:** [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)

### Advanced Usage
- Adjust generation parameters for quality
- Batch process multiple images
- Integrate into your pipeline

### Verify Implementation
Once official xAI API docs are available:
1. Review [GROK_INTEGRATION.md](GROK_INTEGRATION.md) "Implementation Notes"
2. Update API endpoint and payload
3. Test thoroughly

## Need Help?

1. Check [GROK_INTEGRATION.md](GROK_INTEGRATION.md) troubleshooting section
2. Verify against [xAI documentation](https://docs.x.ai/docs/overview)
3. Review error messages for guidance
4. Open an issue with details

## Success Checklist

✅ API key obtained from xAI Console
✅ Dependencies installed (`pip install requests`)
✅ Environment variable set (`XAI_API_KEY`)
✅ First video generated successfully
✅ Understand how to switch between models
✅ Ready to explore advanced features

---

**Ready to generate?** Just run:
```bash
XAI_API_KEY="your_key" python generate.py --task grok-i2v --image your_image.jpg
```

Enjoy creating videos with Grok AI! 🚀
