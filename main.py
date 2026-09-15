from presentation import terminal
from application.conversationservice import ConversationService
from infrastructure.llm.openai_provider import OpenAIProvider
from infrastructure.persistence.json_repository import JSONRepository
import os
from dotenv import load_dotenv

load_dotenv()
print("OPENAI_API_KEY exists:", os.getenv("OPENAI_API_KEY") is not None)

def main():
    print()
    print("Starting application...")
    print()

    llm = OpenAIProvider(
        api_key=os.getenv('OPENAI_API_KEY'),
        model="gpt-5-nano-2025-08-07"
    )

    persistence_service = JSONRepository()
    conversation_service = ConversationService(persistence_service, llm)

    while True:
        user_input = terminal.read()
        if user_input == '!exit':
            print()
            print("Exiting application...")
            print()
            break

        response = conversation_service.send_message(user_input)    
        terminal.write(response)



if __name__ == "__main__":
    main()