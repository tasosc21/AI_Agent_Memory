from typing import TypedDict
from domain.user import User as DomainUser
from domain.message import Message as DomainMessage
from domain.conversation import Conversation as DomainConversation
from infrastructure.persistence.postgre.models import Message as DBMessage, Conversation as DBConversation, User as DBUser

class PersistenceResult(TypedDict):
    user: DomainUser
    conversation: DomainConversation
    message: DomainMessage