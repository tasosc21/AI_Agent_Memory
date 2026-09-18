# Development History

## Development Approach

AI_Agent_Memory is developed incrementally.

Each version introduces a specific capability or architectural improvement while avoiding complexity that is not yet justified by the system's requirements.

Development follows the general cycle:

```text
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
```

Architectural decisions are recorded separately when they have lasting consequences for the system.

---

# v0.1.0 — Core Conversation

## Objective

Establish the smallest complete application capable of receiving a user message, communicating with an LLM, returning the response and persisting the conversation.

---

## Implemented

* terminal-based interaction
* LLM communication
* local JSON conversation persistence
* initial layered application structure
* separation between application logic and infrastructure

---

## Architecture

```text
      ┌──────────────┐
      │   Terminal   │
      │ Presentation │
      └──────┬───────┘
             │
             ▼
  ┌────────────────────┐
  │ ConversationService│
  │    Application     │
  └──────┬─────────┬───┘
         │         │
         ▼         ▼
┌────────────┐ ┌────────────────┐
│ LLMProvider│ │ JsonRepository │
│Infrastructure│ │Infrastructure│
└──────┬─────┘ └───────┬────────┘
       │               │
       ▼               ▼
  OpenAI API           JSON
```

The application layer coordinated the conversation workflow while infrastructure components encapsulated external communication and persistence.

Abstractions were kept minimal at this stage. Additional boundaries were deferred until a concrete requirement emerged.

---

## Data Model

Conversation history was represented as message objects containing:

```text
Message
────────────
role
content
```

Supported roles were:

```text
user
assistant
```

The model was intentionally minimal and did not yet include user identity, conversation identifiers or persistence metadata.

---

## Result

v0.1 established the first complete end-to-end application workflow:

```text
Input
  ↓
Application workflow
  ↓
LLM
  ↓
Persistence
  ↓
Output
```

This provided the foundation for introducing relational persistence and explicit user/conversation modelling.

---

# v0.2.0 — PostgreSQL Persistence

## Objective

Replace the active JSON persistence mechanism with a relational database and establish the persistence model required for multiple users, conversations and messages.

---

## Implemented

* PostgreSQL persistence
* relational user/conversation/message model
* foreign-key relationships
* SQLAlchemy ORM
* Alembic migrations
* database-generated UUIDs and timestamps
* dedicated repositories
* `PersistenceService`
* runtime `Context`
* separation between domain and persistence models
* separation between persistent state and runtime state

The JSON repository remains as legacy v0.1 infrastructure but is no longer part of the active persistence workflow.

---

## Data Model

The relational model introduced in v0.2 is:

```text
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
```

The database consists of:

```text
users
conversations
messages
```

A message identifies its conversation rather than redundantly storing its user.

```text
Message
   ↓
Conversation
   ↓
User
```

---

## Persistence Architecture

The active persistence path is:

```text
Application
    ↓
PersistenceService
    ↓
Repositories
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

`PersistenceService` coordinates the workflow.

Repositories encapsulate database access.

SQLAlchemy provides the ORM layer.

PostgreSQL provides persistent storage.

---

## Runtime State

v0.2 introduced `Context` as the application's working state.

The distinction is:

```text
PostgreSQL
    │
    │ permanent source of truth
    ▼
Context
    │
    │ currently loaded state
    ▼
Application
```

For an already loaded user, the current conversation is reused.

For a user not currently loaded, the application retrieves or creates the user, creates a conversation and establishes the corresponding runtime state.

---

## Database Evolution

Alembic was introduced to manage schema changes through versioned migrations.

The initial migration creates:

```text
users
conversations
messages
```

Future database changes are intended to be introduced through additional migrations rather than manual schema modification.

---

## Result

v0.2 replaced local JSON persistence with a relational persistence architecture capable of representing multiple users, conversations and messages.

The project now has a persistent data foundation on which later memory, retrieval and user-specific capabilities can be built.

---

# v0.3.0 — Automated Testing

## Objective

Introduce automated testing to validate the behavior of the existing domain, application and persistence layers.

The objective was not to achieve complete test coverage or redesign the architecture, but to establish a reliable test suite and use testing to identify real defects and architectural issues.

---

## Implemented

* pytest-based automated test suite
* unit tests for domain objects
* unit tests for `PersistenceService` using test doubles
* integration tests for database repositories
* foreign-key constraint tests
* persistence workflow testing
* isolated PostgreSQL test database
* database cleanup between tests
* validation of database-generated identifiers and persisted relationships
* validation of in-memory runtime state alongside persistent state

External LLM communication is not part of the normal automated test suite. Tests do not make real API requests.

---

## Testing Scope

### Domain

Domain tests verify behavior such as:

* message creation
* username normalization
* optional conversation identifiers
* conversation initialization
* adding messages to conversations
* preservation of message order

These tests do not require PostgreSQL or external services.

### Application

`PersistenceService` is tested independently from the real database by using test doubles for its repositories.

The tests verify behaviors including:

* creating a user when necessary
* creating a conversation for a new user
* assigning the conversation identifier to messages
* reusing an existing runtime conversation
* persisting subsequent messages
* maintaining the current runtime context

### Persistence

Repository tests use a separate PostgreSQL test database.

The tests verify:

* user creation and retrieval
* conversation creation
* message creation and retrieval
* conversation ownership
* message ordering
* foreign-key constraints
* behavior when referenced records do not exist

The test database is isolated from the development database and its schema is created through the same migration system used by the application.

---

## Testing and Design

Testing exposed implementation issues that were not apparent during normal interactive use.

One example was unintended shared state caused by a mutable default argument in the `Conversation` constructor. Because the same default list was reused between instances, tests executed together could affect one another.

The issue was corrected by creating the conversation list for each `Conversation` instance.

This reinforced the role of the test suite as both a validation mechanism and a way of discovering defects in the existing implementation.

Testing did not result in a broad architectural refactor. The existing boundaries were retained where they remained sufficient for the current requirements.

---

## Result

v0.3 established the project's first automated validation layer.

The application now has tests covering:

The test suite provides a baseline for modifying the system with greater confidence as new capabilities are introduced.

The project remains a modular monolith, and no additional architectural abstractions were introduced.



# Future Development

Future versions will be defined as concrete requirements emerge.

Potential areas include:

* API access
* persistent memory
* semantic retrieval
* embeddings and RAG
* knowledge acquisition
* web research
* agent capabilities
* authentication and authorization
* asynchronous processing
* background workers
* machine-learning components
* additional interfaces
* containerisation
* CI/CD

These are potential development areas rather than commitments to a fixed implementation order.
