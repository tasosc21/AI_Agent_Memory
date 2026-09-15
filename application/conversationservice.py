from infrastructure.llm.openai_provider import OpenAIProvider
from infrastructure.persistence.json_repository import JSONRepository



class ConversationService:

    # retrieve/create conversation
    # retrieve conversation history
    def __init__(self, repository: JSONRepository, llm: OpenAIProvider):
        self.persistance = repository
        self.llm = llm

    # request LLM response
    # save user & assistant message
    # return response
    def send_message(self, user_input):
        self.persistance.add_message("user", user_input)
        response = self.llm.generate(self.persistance.data)
        self.persistance.add_message("assistant", response)
        self.persistance.save()
        return response


