import json
import os
from typing import Any, Dict, List, Optional, Union

import requests


class AnthropicClient:
    """
    A client for the Anthropic API to interact with Claude models.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Anthropic API client.

        Args:
            api_key: Anthropic API key. If not provided, will look for ANTHROPIC_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No Anthropic API key provided. Use --anthropic-api-key or set ANTHROPIC_API_KEY"
                " env var."
            )

        self.api_base = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

    def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
        **kwargs,
    ) -> Union[Dict[str, Any], Any]:
        """
        Create a chat completion using the Anthropic Claude API.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: The Claude model to use
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum number of tokens to generate
            stream: Whether to stream the response
            **kwargs: Additional parameters to pass to the API

        Returns:
            API response as a dictionary or a stream
        """
        # Convert OpenAI-style messages to Anthropic format
        system_message = ""
        anthropic_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            elif msg["role"] in ["user", "assistant"]:
                anthropic_messages.append({"role": msg["role"], "content": msg["content"]})

        payload = {
            "model": model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream,
        }

        if system_message:
            payload["system"] = system_message

        # Add any additional parameters
        for key, value in kwargs.items():
            if key not in payload:
                payload[key] = value

        response = requests.post(
            f"{self.api_base}/messages", headers=self.headers, json=payload, stream=stream
        )

        if response.status_code != 200:
            raise Exception(f"Error from Anthropic API: {response.text}")

        if stream:
            return self._handle_streaming_response(response)
        else:
            result = response.json()
            # Convert to OpenAI-like format for compatibility
            return {
                "choices": [
                    {
                        "message": {"role": "assistant", "content": result["content"][0]["text"]},
                        "finish_reason": (
                            "stop"
                            if result.get("stop_reason") == "stop_sequence"
                            else result.get("stop_reason", "unknown")
                        ),
                    }
                ],
                "usage": {
                    "prompt_tokens": result.get("usage", {}).get("input_tokens", 0),
                    "completion_tokens": result.get("usage", {}).get("output_tokens", 0),
                    "total_tokens": result.get("usage", {}).get("input_tokens", 0) + result.get(
                        "usage", {}
                    ).get("output_tokens", 0),
                },
                "model": result.get("model", model),
                "id": result.get("id", ""),
                "object": "chat.completion",
            }

    def _handle_streaming_response(self, response):
        """
        Handle streaming response from Anthropic API.

        Args:
            response: Streaming response from requests

        Returns:
            Generator that yields chunks in OpenAI-compatible format
        """
        for line in response.iter_lines():
            if line:
                if line.startswith(b"data: "):
                    data = json.loads(line[6:])
                    if data.get("type") == "content_block_delta":
                        delta_text = data.get("delta", {}).get("text", "")
                        yield {
                            "choices": [{"delta": {"content": delta_text}, "finish_reason": None}]
                        }
                    elif data.get("type") == "message_stop":
                        yield {"choices": [{"delta": {}, "finish_reason": "stop"}]}
