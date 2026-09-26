import os
from typing import cast
from dotenv import load_dotenv
from openai.types.shared import ReasoningEffort

from application.conversation_service import ConversationService
from application.persistence_service import PersistenceService
from application.context_service import ContextService
from application.context_store import ContextStore
from application.summary_service import SummaryService

from domain.context import Context
from domain.message import Message as DomainMessage, MessageRole

from infrastructure.llm.openai_provider import OpenAIProvider

from infrastructure.persistence.postgre.repositories.conversation_repository import ConversationRepository
from infrastructure.persistence.postgre.repositories.message_repository import MessageRepository
from infrastructure.persistence.postgre.repositories.user_repository import UserRepository
from infrastructure.persistence.postgre.repositories.meeting_repository import MeetingRepository
from infrastructure.persistence.txt.prompt_repository import PromptRepository

from presentation import terminal

load_dotenv()


def main() -> None:
    terminal.start()

    llm = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("MODEL"),
        reasoning_effort=cast(ReasoningEffort, os.getenv("REASONING_EFFORT")))

    context_store = ContextStore()
    user_repository = UserRepository()
    conversation_repository = ConversationRepository()
    message_repository = MessageRepository()
    meeting_repository = MeetingRepository()
    prompt_repository = PromptRepository()

    persistence_service = PersistenceService(
        context_store,
        user_repository,
        conversation_repository,
        meeting_repository,
        message_repository)

    context_service = ContextService(
        context_store,
        prompt_repository
        )

    conversation_service = ConversationService(
        llm)

    summary_service = SummaryService(llm, prompt_repository, context_store)

    current_user = "Jane"

    while True:

        user_input = terminal.read()
        if user_input.startswith('!'):
            parts = user_input[1:].split(maxsplit=2)
            match parts:
                case ["exit"]:
                    print("Summarising and saving to database...")
                    summary_service.on_exit()
                    persistence_service.on_exit()
                    terminal.exit()
                    break

                case ["cu", username, message]:
                    current_user, user_message = terminal.change_user(username, message)

                case ["cu", username]:
                    current_user, s = terminal.change_user(username, "")
                    print(s)
                    continue

                case _:
                    continue
        else:
            user_message = user_input

        domain_user_msg = DomainMessage(
            username=current_user,
            role=MessageRole.USER,
            content=user_message,
            conversation_id=None,
        )

        db_objects = persistence_service.run(domain_user_msg)
        full_context = context_service.run(db_objects)
        ai_response = conversation_service.run(full_context)

        domain_response = DomainMessage(
            username=current_user,
            role=MessageRole.ASSISTANT,
            content=ai_response,
            conversation_id=None,
        )
        db_objects = persistence_service.run(domain_response)
        full_context = context_service.run(db_objects)

        summary_service.run(domain_user_msg)

        terminal.write(domain_response.content)

if __name__ == "__main__":
    main()