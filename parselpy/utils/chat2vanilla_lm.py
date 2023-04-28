from functools import wraps
from typing import Type

from langchain.schema import SystemMessage


def Chat2VanillaLM(ChatModel: Type):
    old_call = ChatModel.__call__

    @wraps(ChatModel.__call__)
    def __call__(self, prompt: str, *args, **kwargs):
        return old_call(self, [SystemMessage(content=prompt)], *args, **kwargs).content

    return type(ChatModel.__name__, (ChatModel,), {"__call__": __call__})
