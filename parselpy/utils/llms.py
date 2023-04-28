import langchain.chat_models as chat_models
import langchain.llms as llms

from parselpy.utils.chat2vanilla_lm import Chat2VanillaLM

LLM_CONSTRUCTORS = {
    **{name: Chat2VanillaLM(getattr(chat_models, name)) for name in chat_models.__all__},
    **{name: getattr(llms, name) for name in llms.__all__},
}
