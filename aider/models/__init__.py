from .model import Model
from .openai import OpenAIModel
from .openrouter import OpenRouterModel
from .claude import ClaudeModel

GPT4 = Model.create("gpt-4")
GPT35 = Model.create("gpt-3.5-turbo")
GPT35_16k = Model.create("gpt-3.5-turbo-16k")
CLAUDE3_SONNET = Model.create("claude-3-sonnet-20240229")
CLAUDE3_HAIKU = Model.create("claude-3-haiku-20240307")

__all__ = [
    OpenAIModel,
    OpenRouterModel,
    ClaudeModel,
    GPT4,
    GPT35,
    GPT35_16k,
    CLAUDE3_SONNET,
    CLAUDE3_HAIKU,
]
