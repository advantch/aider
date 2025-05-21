import tiktoken

from .model import Model


class ClaudeModel(Model):
    def __init__(self, name):
        self.name = name
        
        # Map Claude model names to their context window sizes (in tokens)
        claude_models = {
            "claude-3-opus-20240229": 200,  # 200k tokens
            "claude-3-sonnet-20240229": 180,  # 180k tokens
            "claude-3-haiku-20240307": 150,  # 150k tokens
            "claude-2.1": 100,  # 100k tokens
            "claude-2.0": 100,  # 100k tokens
            "claude-instant-1.2": 100,  # 100k tokens
        }
        
        # Check if the model name is in our known Claude models
        if name in claude_models:
            tokens = claude_models[name]
        else:
            # Default to 100k if unknown Claude model (assuming it starts with "claude-")
            if name.startswith("claude-"):
                tokens = 100
            else:
                raise ValueError(f"Unknown Claude model: {name}")
        
        self.max_context_tokens = tokens * 1024
        
        # Use cl100k_base tokenizer as an approximation for Claude
        # This is not perfect but should be close enough for token counting
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # Claude models are good at following instructions, so use diff format
        self.edit_format = "diff"
        self.use_repo_map = True
        self.send_undo_reply = True
        
        # Set pricing based on model
        if name == "claude-3-opus-20240229":
            self.prompt_price = 0.015  # $15 per million tokens
            self.completion_price = 0.075  # $75 per million tokens
            self.max_chat_history_tokens = 8 * 1024
        elif name == "claude-3-sonnet-20240229":
            self.prompt_price = 0.003  # $3 per million tokens
            self.completion_price = 0.015  # $15 per million tokens
            self.max_chat_history_tokens = 6 * 1024
        elif name == "claude-3-haiku-20240307":
            self.prompt_price = 0.00025  # $0.25 per million tokens
            self.completion_price = 0.00125  # $1.25 per million tokens
            self.max_chat_history_tokens = 4 * 1024
        elif name in ["claude-2.1", "claude-2.0"]:
            self.prompt_price = 0.008  # $8 per million tokens
            self.completion_price = 0.024  # $24 per million tokens
            self.max_chat_history_tokens = 4 * 1024
        elif name == "claude-instant-1.2":
            self.prompt_price = 0.0016  # $1.6 per million tokens
            self.completion_price = 0.0056  # $5.6 per million tokens
            self.max_chat_history_tokens = 4 * 1024
        else:
            # Default pricing for unknown Claude models
            self.prompt_price = 0.008
            self.completion_price = 0.024
            self.max_chat_history_tokens = 4 * 1024
    
    def is_claude(self):
        return True

