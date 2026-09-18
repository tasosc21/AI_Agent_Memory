from typing import cast

from dotenv import load_dotenv
from openai.types.shared import ReasoningEffort

from application.conversationservice import ConversationService
from application.persistenceservice import PersistenceService
from domain.context import Context
from domain.message import Message
from infrastructure.llm.openai_provider import OpenAIProvider
from infrastructure.persistence.postgre.repositories.conversation_repository import ConversationRepository
from infrastructure.persistence.postgre.repositories.message_repository import MessageRepository
from infrastructure.persistence.postgre.repositories.user_repository import UserRepository
from presentation import terminal

import os


load_dotenv()


def main() -> None:
    print()
    print("Starting application...")
    print()


    llm = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("MODEL"),
        reasoning_effort=cast(ReasoningEffort, os.getenv("REASONING_EFFORT")))

    context = Context()

    persistence_service = PersistenceService(
        context,
        UserRepository(),
        ConversationRepository(),
        MessageRepository(),
    )

    conversation_service = ConversationService(llm, context)
    current_user = "test"

    while True:

        user_input = Message(
            current_user,
            "user",
            terminal.read(),
            None,
        )

        if user_input.content == "!exit":
            print()
            print("Exiting application...")
            print()
            break

        persistence_service.run(user_input)

        response = Message(
            current_user,
            "assistant",
            conversation_service.run(),
            None,
        )

        persistence_service.run(response)

        terminal.write(response.content)
        print()


if __name__ == "__main__":
    main()