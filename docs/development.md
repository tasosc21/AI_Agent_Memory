# Development History

## Development Approach

AI_Agent_Memory is developed incrementally.

Each version introduces a specific capability or architectural improvement while avoiding complexity that is not yet justified by the system's requirements.

Development follows the general cycle:

    Requirement
        ↓
    Design
        ↓
    Implementation
        ↓
    Validation
        ↓
    Refinement
        ↓
    Documentation

Architectural decisions are recorded separately when they have lasting consequences for the system.

---

# v0.1.0 — Core Conversation

## Objective

Establish the smallest complete application capable of receiving a user message, communicating with an LLM, returning the response, and persisting the conversation.

## Implemented

- terminal-based interaction
- LLM communication
- local JSON conversation persistence
- initial layered application structure
- separation between application logic and infrastructure

## Architecture

    Terminal
        ↓
    ConversationService
        ├── LLMProvider
        └── JsonRepository
                ↓
             JSON

The application layer coordinated the conversation workflow while infrastructure components encapsulated external communication and persistence.

Abstractions were kept minimal at this stage. Additional boundaries were deferred until a concrete requirement emerged.

## Data Model

Conversation history was represented as message objects containing:

    Message
    ────────────
    role
    content

Supported roles were:

    user
    assistant

The model was intentionally minimal and did not yet include user identity, conversation identifiers, or persistence metadata.

## Result

v0.1 established the first complete end-to-end application workflow:

    Input
      ↓
    Application workflow
      ↓
    LLM
      ↓
    Persistence
      ↓
    Output

This provided the foundation for introducing relational persistence and explicit user and conversation modelling.

---

# v0.2.0 — PostgreSQL Persistence

## Objective

Replace the active JSON persistence mechanism with a relational database and establish the persistence model required for multiple users, conversations, and messages.

## Implemented

- PostgreSQL persistence
- relational user/conversation/message model
- foreign-key relationships
- SQLAlchemy ORM
- Alembic migrations
- database-generated UUIDs and timestamps
- dedicated repositories
- `PersistenceService`
- runtime context
- separation between domain and persistence models
- separation between persistent state and runtime state

The JSON repository remains as legacy v0.1 infrastructure but is no longer part of the active persistence workflow.

## Data Model

The relational model introduced in v0.2 is:

    User
     │
     └── 1:N
          │
          ▼
    Conversation
     │
     └── 1:N
          │
          ▼
    Message

The database consists of:

    users
    conversations
    messages

A message identifies its conversation rather than redundantly storing its user.

    Message
       ↓
    Conversation
       ↓
    User

## Persistence Architecture

The active persistence path is:

    Application
        ↓
    PersistenceService
        ↓
    Repositories
        ↓
    SQLAlchemy
        ↓
    PostgreSQL

`PersistenceService` coordinates the workflow.

Repositories encapsulate database access.

SQLAlchemy provides the ORM layer.

PostgreSQL provides persistent storage.

## Runtime State

v0.2 introduced runtime context as the application's working state.

The distinction is:

    PostgreSQL
        │
        │ persistent state
        ▼
    Runtime Context
        │
        │ active application state
        ▼
    Application

The runtime context allowed the application to maintain currently relevant conversation state without treating the database itself as the application's working context.

## Database Evolution

Alembic was introduced to manage schema changes through versioned migrations.

The initial migration creates:

    users
    conversations
    messages

Future database changes are intended to be introduced through additional migrations rather than manual schema modification.

## Result

v0.2 replaced local JSON persistence with a relational persistence architecture capable of representing multiple users, conversations, and messages.

The project now had a persistent data foundation on which later context, memory, retrieval, and user-specific capabilities could be built.

---

# v0.3.0 — Automated Testing

## Objective

Introduce automated testing to validate the behaviour of the existing domain, application, and persistence layers.

The objective was not to achieve complete test coverage or redesign the architecture, but to establish a reliable test suite and use testing to identify real defects and architectural issues.

## Implemented

- pytest-based automated test suite
- unit tests for domain objects
- application service tests
- repository integration tests
- test doubles for isolated application testing
- isolated PostgreSQL test database
- database cleanup between tests
- validation of database-generated identifiers and persisted relationships
- validation of runtime state alongside persistent state
- workflow-level testing

External LLM communication is not part of the normal automated test suite. Tests do not make real API requests.

## Testing Scope

### Domain

Domain tests verify behaviour such as:

- message creation
- username normalization
- optional conversation identifiers
- conversation initialization
- adding messages to conversations
- preservation of message order

These tests do not require PostgreSQL or external services.

### Application

Application services are tested independently where infrastructure can be replaced with test doubles.

The tests verify behaviours including:

- creating users when necessary
- creating conversations
- assigning conversation identifiers to messages
- reusing existing runtime context
- persisting subsequent messages
- maintaining runtime state
- constructing application-level workflows

### Persistence

Repository tests use a separate PostgreSQL test database.

The tests verify:

- user creation and retrieval
- conversation creation
- message creation and retrieval
- conversation ownership
- message relationships
- foreign-key constraints
- behaviour when referenced records do not exist
- database-generated identifiers

The test database is isolated from the development database and its schema is created through the same migration system used by the application.

## Testing and Design

Testing exposed implementation issues that were not apparent during normal interactive use.

One example was unintended shared state caused by a mutable default argument in the `Conversation` constructor. Because the same default list was reused between instances, tests executed together could affect one another.

The issue was corrected by creating the conversation list for each `Conversation` instance.

Testing also helped identify issues at boundaries between application components and persistence components.

Testing did not result in a broad architectural refactor. Existing boundaries were retained where they remained sufficient for the current requirements.

## Result

v0.3 established the project's first automated validation layer.

The application now had tests covering domain behaviour, application services, persistence repositories, presentation behaviour, and selected workflows.

The project remained a modular monolith, and no additional architectural abstractions were introduced solely for the sake of testing.

---

# v0.4.0 — Context & Conversation Continuity

## Objective

Introduce runtime context and conversation continuity so that AI_Agent can maintain relevant conversational state while the application is running and distinguish between individual user conversations and the broader meeting context.

## Implemented

- runtime `ContextStore`
- per-user runtime contexts
- current user context tracking
- current conversation message state
- user conversation summaries
- meeting-level conversation state
- meeting-level summaries
- meeting persistence
- persistent user profiles and summaries
- persistent conversation summaries
- interaction-based summarisation
- prompt repository for system and summarisation prompts
- application-level context orchestration
- expanded automated testing
- separate summary workflow tests

## Context Architecture

v0.4 introduced `ContextStore` as the central runtime state container.

It maintains:

- a cache of active user contexts
- the currently active user context
- the current meeting conversation
- the current meeting summary

The simplified structure is:

    ContextStore
        │
        ├── User A → Context
        ├── User B → Context
        ├── User C → Context
        │
        ├── Current meeting conversation
        │
        └── Current meeting summary

Each user context contains information such as:

    Context
    ────────────────
    user_id
    conversation_id
    profile
    summary
    messages
    current_conversation_summary

This separates active conversational state from the complete persistent history stored in PostgreSQL.

## Meeting Model

v0.4 introduced the concept of a meeting as a higher-level container for multiple user conversations.

The relationship became:

    Meeting
       │
       ├── Conversation ── User
       │       │
       │       └── Messages
       │
       ├── Conversation ── User
       │       │
       │       └── Messages
       │
       └── Conversation ── User
               │
               └── Messages

A meeting can therefore contain conversations from multiple users.

The runtime context additionally maintains a combined meeting conversation and meeting summary.

## Persistence Changes

The database was extended to support the new context model.

Users gained:

- profile
- summary
- last interaction timestamp

Conversations gained:

- meeting relationship
- summary

Meetings were introduced with:

- meeting ID
- summary
- start timestamp
- finish timestamp

The changes were introduced through a new Alembic migration rather than modifying the existing schema manually.

## Application Services

v0.4 expanded the application layer with dedicated services for context and summarisation.

The main workflow became:

    User message
        ↓
    PersistenceService
        ↓
    ContextService
        ↓
    ContextStore
        ↓
    ConversationService
        ↓
    OpenAIProvider
        ↓
    AI response
        ↓
    PersistenceService
        ↓
    ContextService
        ↓
    SummaryService

`ContextService` builds the context supplied to the LLM.

`SummaryService` periodically compresses accumulated conversation state into summaries.

## Summarisation

Summarisation was introduced as a mechanism for preventing the active context from growing indefinitely.

The current implementation maintains separate summarisation levels.

### User Conversation

Individual user interactions are periodically summarised.

The current threshold is based on user interaction count.

When the threshold is reached, the current user messages are summarised and the message list is reset while retaining the resulting conversation summary.

### Meeting Conversation

The combined meeting conversation is periodically summarised based on total interactions across users.

The resulting summary is retained as meeting-level runtime state.

### Application Exit

When the application exits, remaining unsummarised user and meeting context is summarised before the application finishes.

## Prompt Infrastructure

v0.4 introduced dedicated prompt infrastructure.

Prompt files are stored in:

    config/prompts/

The `PromptRepository` loads prompts for:

- normal conversation
- user conversation summarisation
- meeting summarisation

This keeps prompt content separate from application implementation.

## Testing

The test suite was expanded alongside the new functionality.

Tests were added for:

- `ContextStore`
- `ContextService`
- `SummaryService`
- summary workflows
- meeting repository behaviour
- updated persistence behaviour
- updated domain behaviour

The test suite validates the new behaviour without attempting to test every implementation detail.

The purpose of the tests is to provide a safety net around meaningful application behaviour and boundaries.

## Result

v0.4 established the first version of AI_Agent with runtime conversational continuity.

The application can now maintain separate active user contexts, track a broader meeting context, persist meeting and conversation relationships, and periodically compress conversation history into summaries.

This provides the foundation for the next major conceptual step: defining and implementing persistent memory.

---

# Future Development

Future versions will be defined as concrete requirements emerge.

Potential areas include:

- persistent memory
- defining what constitutes a memory
- memory retrieval
- semantic retrieval
- embeddings and RAG
- knowledge acquisition
- web research
- agent capabilities
- API access
- authentication and authorization
- asynchronous processing
- background workers
- machine-learning components
- additional interfaces
- web UI
- containerisation
- CI/CD
- systems-level components

These are potential development areas rather than commitments to a fixed implementation order.

The next development focus is expected to explore **persistent memory** and the underlying model of what information AI_Agent should retain, how it should be represented, and how it should later be retrieved.
