# Copyright 2024-2025 Integration for Grok API. All rights reserved.
"""
Grok API integration for Image-to-Video generation.
This module provides a wrapper around the xAI Grok API for converting images to videos.

IMPORTANT NOTES:
================
This implementation serves as a template/framework for integrating with xAI's Grok API.
The actual API endpoints and request/response structures may differ from what's implemented
here, as the official Grok image-to-video API documentation was not available at the time
of implementation.

BEFORE USING IN PRODUCTION:
===========================
1. Verify the actual Grok API endpoint for image-to-video generation
2. Update the payload structure to match the official API specification
3. Adjust response parsing based on actual API response format
4. Test with real API credentials and validate all functionality
5. Implement proper error handling for production use cases

The code structure and interface are designed to be easily adaptable once the official
API details are available. The main areas that may need adjustment:
- API endpoint URL (currently using /chat/completions as a placeholder)
- Request payload structure (currently based on common API patterns)
- Response parsing logic (currently handles multiple common patterns)

For the latest xAI Grok API documentation, visit:
https://docs.x.ai/docs/overview
"""

import logging
import os
import time
from typing import Optional, Union
from pathlib import Path

import requests
from PIL import Image
import torch
import numpy as np


class GrokI2V:
    """
    Grok Image-to-Video generation client.
    
    This class provides an interface to the xAI Grok API for generating
    videos from images using the Grok model.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: str = "https://api.x.ai/v1",
        model: str = "grok-2-vision-1212",
        device_id: int = 0,
        rank: int = 0,
    ):
        """
        Initialize the Grok Image-to-Video client.

        Args:
            api_key: xAI API key. If not provided, will read from XAI_API_KEY env var.
            api_url: Base URL for the xAI API.
            model: Grok model to use for image-to-video generation.
            device_id: Device ID (for compatibility with WAN interface).
            rank: Rank (for compatibility with distributed setups).
        """
        self.api_key = api_key or os.getenv("XAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Set XAI_API_KEY environment variable or pass api_key parameter."
            )
        
        self.api_url = api_url.rstrip("/")
        self.model = model
        self.device_id = device_id
        self.rank = rank
        
        logging.info(f"Initialized Grok I2V client with model: {model}")

    def _upload_image(self, image: Union[str, Image.Image]) -> str:
        """
        Upload or convert image to a format suitable for the API.

        Args:
            image: Either a path to an image file or a PIL Image object.

        Returns:
            Image URL or base64-encoded image string.
        """
        if isinstance(image, str):
            # If it's already a URL, return it
            if image.startswith("http://") or image.startswith("https://"):
                return image
            # Otherwise, load the image file
            image = Image.open(image).convert("RGB")
        
        # For local images, we need to save temporarily and potentially upload
        # For now, we'll save to a temporary location
        # In production, you might want to upload to a cloud storage service
        import base64
        from io import BytesIO
        
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"

    def generate(
        self,
        prompt: str,
        image: Union[str, Image.Image],
        max_area: Optional[int] = None,
        frame_num: int = 81,
        shift: float = 5.0,
        sample_solver: str = "unipc",
        sampling_steps: int = 40,
        guide_scale: float = 5.0,
        seed: int = 42,
        offload_model: bool = False,
        timeout: int = 300,
    ) -> torch.Tensor:
        """
        Generate a video from an image and prompt using the Grok API.

        Args:
            prompt: Text description for the video generation.
            image: Input image (path or PIL Image object).
            max_area: Maximum area for the output video (for compatibility).
            frame_num: Number of frames to generate.
            shift: Flow shift parameter (for compatibility).
            sample_solver: Sampling solver to use (for compatibility).
            sampling_steps: Number of sampling steps (for compatibility).
            guide_scale: Guidance scale for generation.
            seed: Random seed for reproducibility.
            offload_model: Whether to offload model (for compatibility).
            timeout: Request timeout in seconds.

        Returns:
            torch.Tensor: Generated video tensor in shape (frame_num, C, H, W).
        """
        logging.info(f"Generating video from image with Grok API")
        logging.info(f"Prompt: {prompt}")
        
        # Convert image to appropriate format
        image_data = self._upload_image(image)
        
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        # WARNING: This API structure is a template based on common patterns.
        # The actual xAI Grok API for image-to-video may have a different structure.
        # Please refer to the official xAI documentation and update accordingly.
        # 
        # Common alternative endpoint patterns that might be used:
        # - f"{self.api_url}/video/generate"
        # - f"{self.api_url}/v1/images/animate"
        # - f"{self.api_url}/v1/media/generate"
        # 
        # You may need to adjust:
        # 1. The endpoint URL
        # 2. The payload structure
        # 3. The parameter names and values
        
        logging.warning(
            "Using template API structure. Verify against official xAI Grok API documentation."
        )
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_data, "detail": "high"}
                        },
                        {
                            "type": "text",
                            "text": f"Generate a video from this image: {prompt}"
                        }
                    ]
                }
            ],
            "temperature": 0.5,
            "max_tokens": 1000,
            "stream": False,
            # Video generation specific parameters - these may need adjustment
            "video_config": {
                "num_frames": frame_num,
                "guidance_scale": guide_scale,
                "seed": seed,
            }
        }
        
        try:
            # Make API request
            # NOTE: The endpoint may need to be updated based on official API docs
            endpoint = f"{self.api_url}/chat/completions"
            logging.info(f"Sending request to: {endpoint}")
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=timeout,
            )
            
            # Log response status for debugging
            logging.info(f"API response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            logging.debug(f"API response: {result}")
            
            # Extract video URL or data from response
            # Note: The actual response format will depend on the Grok API
            video_url = self._extract_video_from_response(result)
            
            if video_url:
                # Download and convert video to tensor
                video_tensor = self._download_and_convert_video(video_url, frame_num)
                return video_tensor
            else:
                logging.error(f"Failed to extract video URL from response: {result}")
                raise ValueError(
                    "No video URL found in API response. "
                    "This may indicate that the API structure has changed or "
                    "the endpoint doesn't support video generation. "
                    "Please check the official xAI Grok API documentation and "
                    "update the implementation accordingly."
                )
                
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error from API: {e}")
            logging.error(f"Response content: {e.response.text if hasattr(e, 'response') else 'N/A'}")
            raise RuntimeError(
                f"API request failed with status {e.response.status_code if hasattr(e, 'response') else 'unknown'}. "
                f"This may indicate an incorrect endpoint or payload structure. "
                f"Please verify the API implementation against official documentation."
            ) from e
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error during API request: {e}")
            raise RuntimeError(
                f"Failed to connect to Grok API: {e}. "
                f"Please check your internet connection and API endpoint configuration."
            ) from e
        except Exception as e:
            logging.error(f"Unexpected error during video generation: {e}")
            raise

    def _extract_video_from_response(self, response: dict) -> Optional[str]:
        """
        Extract video URL or data from API response.

        Args:
            response: API response dictionary.

        Returns:
            Video URL or None if not found.
        """
        # This is a placeholder - actual extraction logic depends on API response format
        # Common patterns might include:
        # - response['choices'][0]['message']['video_url']
        # - response['data']['video_url']
        # - response['video']['url']
        
        # Try common response patterns
        if 'choices' in response and len(response['choices']) > 0:
            choice = response['choices'][0]
            if 'message' in choice:
                message = choice['message']
                if 'video_url' in message:
                    return message['video_url']
                if 'content' in message and isinstance(message['content'], str):
                    # The response might contain a URL in the text
                    content = message['content']
                    if content.startswith('http'):
                        return content
        
        if 'video_url' in response:
            return response['video_url']
        
        if 'data' in response and 'url' in response['data']:
            return response['data']['url']
        
        logging.warning(f"Could not extract video URL from response: {response}")
        return None

    def _download_and_convert_video(self, video_url: str, frame_num: int) -> torch.Tensor:
        """
        Download video from URL and convert to tensor.

        Args:
            video_url: URL of the generated video.
            frame_num: Expected number of frames.

        Returns:
            torch.Tensor: Video tensor in shape (frame_num, C, H, W).
        """
        import tempfile
        import imageio
        import cv2
        
        # Download video
        logging.info(f"Downloading video from: {video_url}")
        
        if video_url.startswith("data:"):
            # Handle base64 encoded video
            import base64
            header, encoded = video_url.split(",", 1)
            video_data = base64.b64decode(encoded)
            
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
                tmp.write(video_data)
                video_path = tmp.name
        else:
            # Download from URL
            response = requests.get(video_url, stream=True, timeout=60)
            response.raise_for_status()
            
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp.write(chunk)
                video_path = tmp.name
        
        try:
            # Read video and convert to tensor
            reader = imageio.get_reader(video_path)
            frames = []
            
            for i, frame in enumerate(reader):
                if i >= frame_num:
                    break
                # Convert to RGB if needed
                if len(frame.shape) == 2:
                    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
                elif frame.shape[2] == 4:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
                frames.append(frame)
            
            reader.close()
            
            # Pad with last frame if needed
            while len(frames) < frame_num:
                frames.append(frames[-1] if frames else np.zeros((480, 832, 3), dtype=np.uint8))
            
            # Convert to tensor: (frame_num, H, W, C) -> (frame_num, C, H, W)
            frames = np.stack(frames[:frame_num], axis=0)
            video_tensor = torch.from_numpy(frames).permute(0, 3, 1, 2).float()
            
            # Normalize to [-1, 1]
            video_tensor = (video_tensor / 127.5) - 1.0
            
            return video_tensor
            
        finally:
            # Clean up temporary file
            if os.path.exists(video_path):
                os.unlink(video_path)
