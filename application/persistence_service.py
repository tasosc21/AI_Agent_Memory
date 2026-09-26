from uuid import UUID

from application.types import PersistenceResult
from application.context_store import ContextStore

from domain.message import Message as DomainMessage, MessageRole
from domain.user import User as DomainUser
from domain.conversation import Conversation as DomainConversation

from infrastructure.persistence.postgre.database import SessionFactory

from infrastructure.persistence.postgre.repositories.conversation_repository import ConversationRepository
from infrastructure.persistence.postgre.repositories.message_repository import MessageRepository
from infrastructure.persistence.postgre.repositories.user_repository import UserRepository
from infrastructure.persistence.postgre.repositories.meeting_repository import MeetingRepository

class PersistenceService:

    def __init__(self,
                 context_store: ContextStore,
                 user_repository: UserRepository,
                 conversation_repository: ConversationRepository,
                 meeting_repository: MeetingRepository,
                 message_repository: MessageRepository) -> None:

        self.context_store = context_store
        self.user_repository = user_repository
        self.conversation_repository = conversation_repository
        self.meeting_repository = meeting_repository
        self.message_repository = message_repository
        self.meeting_id: UUID = self.get_meeting_id()


    def get_meeting_id(self) -> UUID:
        with SessionFactory() as session:
            with session.begin():
                dbmeeting = self.meeting_repository.create(session)
                return dbmeeting.meeting_id

    def run(self, domain_message: DomainMessage) -> PersistenceResult:
        username = domain_message.username

        with SessionFactory() as session:
            with session.begin():

                dbuser = self.user_repository.get(session, username)

                if dbuser is None:
                    dbuser = self.user_repository.create(session, username)
                    dbconversation = self.conversation_repository.create(session, dbuser.user_id, self.meeting_id)
                    domain_message.conversation_id = dbconversation.conversation_id
                else:
                    if username in self.context_store.context_cache:
                        user_context = self.context_store.context_cache[username]
                        domain_message.conversation_id = user_context.conversation_id
                    else:
                        dbconversation = self.conversation_repository.create(session, dbuser.user_id, self.meeting_id)
                        domain_message.conversation_id = dbconversation.conversation_id

                dbmessage = self.message_repository.create(session, domain_message)

                domain_user = DomainUser(dbuser.user_id, dbuser.username, dbuser.profile, dbuser.summary)
                domain_conversation = DomainConversation(dbuser.username, domain_message.conversation_id)
                domain_message = DomainMessage(dbuser.username, MessageRole(dbmessage.role), dbmessage.content, domain_message.conversation_id)

                return {"user": domain_user,
                        "conversation": domain_conversation,
                        "message": domain_message}

    def on_exit(self):

        with SessionFactory() as session:
            with session.begin():

                for _, context in self.context_store.context_cache.items():
                    self.user_repository.update(session, context)
                    self.conversation_repository.update(session, context)

                self.meeting_repository.update(session, self.meeting_id, self.context_store.current_meeting_summary)