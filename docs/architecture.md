
# Architecture

## Architectural Approach

AI_Agent_Memory uses a layered modular-monolith architecture.

The application runs as a single process while separating responsibilities between presentation, application, domain, and infrastructure components.

The architecture aims to maintain clear boundaries without introducing distributed-system complexity before it is justified.

Dependencies are assembled in `main.py`, which acts as the application's composition root.

---

## Layers

### Presentation

The presentation layer handles interaction with the user and presentation of application output.

Current implementation:

- `presentation/terminal.py`

The terminal interface reads user input, handles terminal-specific commands, and displays application output.

Application behaviour is handled by the application layer rather than by the presentation layer.

### Application

The application layer coordinates application workflows and use cases.

Current implementation:

- `application/context_service.py`
- `application/context_store.py`
- `application/conversation_service.py`
- `application/persistence_service.py`
- `application/summary_service.py`
- `application/types.py`

#### PersistenceService

`PersistenceService` coordinates persistence-related workflows.

It:

- identifies or creates users
- creates conversations
- associates conversations with the current meeting
- persists messages
- converts persistence models into domain objects
- updates persistent state when the application exits

It uses repository implementations for database operations.

#### ContextService

`ContextService` coordinates construction of the context required by the conversation workflow.

It:

- retrieves the user's runtime context
- creates a context for a user when necessary
- adds messages to the context
- updates the currently active context
- constructs the context passed to the conversation service

#### ContextStore

`ContextStore` maintains runtime application state.

It currently contains:

- a cache of active user contexts
- the current user context
- the current meeting conversation
- the current meeting summary

It is shared by application services that require runtime conversational state.

It is not the persistent source of truth. Persistent data is stored in PostgreSQL.

#### ConversationService

`ConversationService` coordinates interaction with the LLM.

It receives the context constructed by `ContextService` and passes it to the configured LLM provider.

#### SummaryService

`SummaryService` coordinates summarisation of user and meeting-level conversation state.

It currently:

- tracks user interaction counts
- periodically summarises individual user conversations
- periodically summarises the current meeting conversation
- performs final summarisation when the application exits

---

## Domain

The domain layer contains application concepts independently from persistence technology.

Current implementation:

- `domain/context.py`
- `domain/conversation.py`
- `domain/message.py`
- `domain/user.py`

Current domain concepts include:

- `User`
- `Conversation`
- `Message`
- `Context`

The domain objects are separate from the SQLAlchemy persistence models.

---

## Infrastructure

The infrastructure layer contains concrete implementations that communicate with external systems and persistence mechanisms.

Current implementation:

- `infrastructure/llm/openai_provider.py`
- `infrastructure/persistence/postgre/`
- `infrastructure/persistence/txt/prompt_repository.py`
- `infrastructure/persistence/json/json_repository.py`

Infrastructure currently provides:

- LLM communication through `OpenAIProvider`
- PostgreSQL persistence through SQLAlchemy and repositories
- prompt loading through `PromptRepository`
- legacy JSON persistence

---

## Composition Root

`main.py` acts as the application's entry point and composition root.

It is responsible for:

- loading environment configuration
- creating infrastructure components
- creating application services
- connecting dependencies
- starting the terminal interface
- running the main application loop

The main dependencies constructed in `main.py` are:

- `OpenAIProvider`
- `ContextStore`
- `UserRepository`
- `ConversationRepository`
- `MessageRepository`
- `MeetingRepository`
- `PromptRepository`

These are then injected into the application services that require them.

---

## Runtime Workflow

For each user message, the current runtime flow is:

1. The terminal receives the user input.
2. `PersistenceService` persists the user message.
3. `PersistenceService` returns the relevant domain objects through `PersistenceResult`.
4. `ContextService` retrieves or creates the user's runtime context.
5. The message is added to `ContextStore`.
6. `ContextService` builds the context supplied to the LLM.
7. `ConversationService` sends the context to `OpenAIProvider`.
8. The AI response is returned.
9. The AI response is persisted through `PersistenceService`.
10. The response is added to runtime context through `ContextService`.
11. `SummaryService` updates user and meeting-level summaries when required.
12. The response is displayed through the terminal.

The simplified flow is:

    Terminal
       |
       v
    PersistenceService
       |
       v
    PostgreSQL
       |
       v
    ContextService
       |
       v
    ContextStore
       |
       v
    ConversationService
       |
       v
    OpenAIProvider
       |
       v
    OpenAI API

The AI response then follows the persistence and context flow again before the summary step.

---

## Runtime State

Runtime state is maintained separately from persistent database state.

`ContextStore` currently maintains two levels of conversational state.

### User Context

Each active user has a `Context` containing:

- user ID
- conversation ID
- profile
- user summary
- current conversation messages
- current conversation summary

User contexts are stored in an in-memory cache keyed by username.

This allows the application to maintain relevant working context for multiple users during the lifetime of the application.

### Meeting Context

`ContextStore` also maintains state shared across users participating in the current meeting:

- current meeting conversation
- current meeting summary

The meeting conversation contains combined conversation activity from the users participating in the current meeting.

---

## Persistent State

PostgreSQL is the persistent source of truth for application data.

The current database contains four main entities:

- `User`
- `Meeting`
- `Conversation`
- `Message`

The relationships are:

- a `Meeting` contains multiple conversations
- a `User` can have multiple conversations
- a `Conversation` belongs to one user and one meeting
- a `Conversation` contains multiple messages
- a `Message` belongs to one conversation

Users contain persistent profile and summary information.

Conversations contain persistent summaries.

Meetings contain a summary and start/finish timestamps.

---

## Runtime State vs Persistent State

PostgreSQL stores durable application data.

`ContextStore` contains the subset of state currently required while the application is running.

The runtime context is therefore not a replacement for the database.

The separation allows the application to work with relevant conversational state without loading the entire persistent history into memory.

---

## Domain and Persistence Models

Domain objects and persistence models are intentionally separate.

For example, a domain `Message` represents the application's concept of a message, while the SQLAlchemy `Message` model represents its database representation.

Repositories perform the persistence operations and provide the boundary between application/domain data and the database implementation.

This prevents the database schema from directly determining the structure of the domain model.

---

## Persistence Boundary

Database access is encapsulated by dedicated repositories.

`PersistenceService` coordinates the persistence workflow and uses:

- `UserRepository`
- `ConversationRepository`
- `MeetingRepository`
- `MessageRepository`

These repositories use SQLAlchemy to communicate with PostgreSQL.

The application services do not directly implement PostgreSQL queries.

---

## LLM Boundary

The LLM is accessed through `OpenAIProvider`.

`ConversationService` uses it to generate responses.

`SummaryService` also uses the provider to generate user and meeting summaries.

This keeps direct OpenAI API interaction inside the infrastructure layer.

---

## Prompt Infrastructure

Prompts are stored outside Python application code.

Current prompt files:

- `config/prompts/system.txt`
- `config/prompts/developer.txt`
- `config/prompts/summarise_user.txt`
- `config/prompts/summarise_all_users.txt`

`PromptRepository` loads these prompts for the application services that require them.

This keeps prompt content separate from application logic.

---

## Database Migrations

Alembic manages PostgreSQL schema evolution.

Current migrations:

- `367bfc151786_create_users_conversations_and_messages.py`
- `487d678b44cc_add_meetings_and_user_summaries_profile.py`

The first migration created the initial users, conversations, and messages structure.

The second introduced meetings and additional user and conversation summary/profile fields.

---

## Testing Architecture

Tests are organized according to the component or boundary being validated.

Current structure:

- `tests/domain/`
- `tests/application/`
- `tests/infrastructure/`
- `tests/presentation/`
- `tests/workflows/`

### Domain Tests

Validate domain behaviour independently from infrastructure.

### Application Tests

Validate application services and runtime state management.

### Infrastructure Tests

Validate concrete infrastructure implementations, including PostgreSQL repositories, prompt loading, and the LLM provider.

PostgreSQL repository tests use a separate PostgreSQL test database.

### Workflow Tests

Validate interactions between multiple application components, such as the summary workflow.

Shared test configuration and test doubles are contained in:

- `tests/conftest.py`
- `tests/fakes.py`

---

## Architectural Principles

The current architecture follows these principles:

1. **Modular monolith first**The application remains a single deployable system until there is a concrete reason to introduce distributed components.
2. **Separation of responsibilities**Presentation, application logic, domain concepts, and infrastructure have distinct responsibilities.
3. **Explicit infrastructure boundaries**Database access, LLM communication, and prompt loading are isolated behind infrastructure components.
4. **Persistent state is separate from runtime state**PostgreSQL provides durable storage while `ContextStore` manages working state during execution.
5. **Domain models are independent of persistence models**Database structures do not directly define domain concepts.
6. **Incremental complexity**New abstractions and infrastructure are introduced when requirements justify them rather than being implemented in advance.
7. **Architecture evolves through implementation**
   The structure of the system is refined through concrete requirements, implementation experience, and validation.

---

## Project Structure

    AI_Agent_Memory/
    │
    ├── .env
    ├── .env.test
    ├── .gitignore
    ├── alembic.ini
    ├── main.py
    ├── README.md
    │
    ├── alembic/
    │   ├── env.py
    │   ├── README
    │   ├── script.py.mako
    │   └── versions/
    │       ├── 367bfc151786_create_users_conversations_and_messages.py
    │       └── 487d678b44cc_add_meetings_and_user_summaries_profile.py
    │
    ├── application/
    │   ├── context_service.py
    │   ├── context_store.py
    │   ├── conversation_service.py
    │   ├── persistence_service.py
    │   ├── summary_service.py
    │   └── types.py
    │
    ├── config/
    │   └── prompts/
    │       ├── developer.txt
    │       ├── README.md
    │       ├── summarise_all_users.txt
    │       ├── summarise_user.txt
    │       └── system.txt
    │
    ├── data/
    │   ├── conversation.json
    │   └── todo.md
    │
    ├── docs/
    │   ├── ADR.md
    │   ├── architecture.md
    │   ├── database.md
    │   └── development.md
    │
    ├── domain/
    │   ├── context.py
    │   ├── conversation.py
    │   ├── message.py
    │   └── user.py
    │
    ├── infrastructure/
    │   ├── llm/
    │   │   └── openai_provider.py
    │   │
    │   └── persistence/
    │       ├── json/
    │       │   └── json_repository.py
    │       ├── postgre/
    │       │   ├── database.py
    │       │   ├── models.py
    │       │   └── repositories/
    │       │       ├── conversation_repository.py
    │       │       ├── meeting_repository.py
    │       │       ├── message_repository.py
    │       │       └── user_repository.py
    │       └── txt/
    │           └── prompt_repository.py
    │
    ├── presentation/
    │   └── terminal.py
    │
    └── tests/
        ├── conftest.py
        ├── fakes.py
        ├── application/
        │   ├── test_context_service.py
        │   ├── test_context_store.py
        │   ├── test_conversation_service.py
        │   ├── test_persistence_service.py
        │   └── test_summary_service.py
        ├── domain/
        │   ├── test_context.py
        │   ├── test_conversation.py
        │   ├── test_message.py
        │   └── test_user.py
        ├── infrastructure/
        │   ├── llm/
        │   │   └── test_openai_provider.py
        │   └── persistence/
        │       ├── postgre/
        │       │   └── repositories/
        │       │       ├── test_conversation_repository.py
        │       │       ├── test_meeting_repository.py
        │       │       ├── test_message_repository.py
        │       │       └── test_user_repository.py
        │       └── txt/
        │           └── test_prompt_repository.py
        ├── presentation/
        │   └── test_terminal.py
        └── workflows/
            └── test_summary_service_workflow.py

Generated files and development-environment directories such as `.venv`, `__pycache__`, `.pyc` files, and `.pytest_cache` are omitted from the documented structure.
