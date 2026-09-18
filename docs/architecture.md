
# Architecture

## Architectural Approach

AI_Agent_Memory uses a **layered modular-monolith architecture**.

The application runs as a single application while separating responsibilities into distinct layers.

This provides modularity and clear boundaries without introducing distributed-system complexity before it is justified.

The architecture is expected to evolve as requirements become more concrete.

---

## Layers

### Presentation

Responsible for interaction with the user and presentation of application output.

Current implementation:

```text
presentation/
└── terminal.py
```

The presentation layer should remain thin and delegate application behaviour to the application layer.

---

### Application

Coordinates application workflows and use cases.

Current implementation:

```text
application/
├── conversationservice.py
└── persistenceservice.py
```

`ConversationService` coordinates the conversation workflow.

`PersistenceService` coordinates persistence-related application workflows.

Application services should coordinate operations without containing infrastructure-specific implementation details.

---

### Domain

Contains concepts belonging to the application's problem domain.

Current implementation:

```text
domain/
├── context.py
├── conversation.py
└── message.py
```

The domain layer represents application concepts independently from persistence technology.

---

### Infrastructure

Contains implementations that interact with external systems.

Current infrastructure includes:

```text
infrastructure/
├── llm/
│   └── openai_provider.py
│
└── persistence/
    ├── json/
    │   └── json_repository.py
    │
    └── postgre/
        ├── database.py
        ├── models.py
        └── repositories/
            ├── user_repository.py
            ├── conversation_repository.py
            └── message_repository.py
```

Infrastructure contains the concrete implementations required to communicate with the LLM provider and persistent storage.

---

## Composition Root

`main.py` acts as the application's entry point and composition root.

It is responsible for creating concrete components and connecting them together.

This keeps dependency construction separate from the application components themselves.

---

## Runtime Architecture

The current runtime structure is:

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
┌──────────────┐  ┌──────────────────┐
│ LLMProvider  │  │PersistenceService│
│Infrastructure│  │  Application     │
└──────┬───────┘  └────────┬─────────┘
       │                   │
       ▼                   ▼
  OpenAI API          Repositories
                           │
                           ▼
                       PostgreSQL
```

The application therefore separates:

* user interaction
* application workflows
* domain state
* external services
* persistent storage

---

## Persistent State vs Runtime State

The system distinguishes between persistent state and working application state.

### Persistent State

PostgreSQL is the source of truth for persisted:

* users
* conversations
* messages

Persistent state survives application restarts.

### Runtime State

`Context` contains the subset of application state currently loaded and required during execution.

```text
PostgreSQL
    │
    │ persistent state
    ▼
Context
    │
    │ working state
    ▼
Application
```

`Context` is therefore not a replacement for the database.

This separation also allows future versions to load only the relevant portion of a user's history rather than keeping all persistent data in memory.

---

## Domain and Infrastructure Boundaries

Domain objects and persistence models are intentionally separate.

For example:

```text
domain.Message
       │
       │ mapping
       ▼
SQLAlchemy Message model
       │
       ▼
PostgreSQL
```

The domain model represents an application concept.

The SQLAlchemy model represents a persistence structure.

This prevents the database schema from unnecessarily determining the structure of the domain model.

---

## Persistence Boundary

Database access is encapsulated by dedicated repositories.

```text
Application
     │
     ▼
PersistenceService
     │
     ▼
Repositories
     │
     ▼
SQLAlchemy
     │
     ▼
PostgreSQL
```

Application services do not directly implement PostgreSQL queries.

---

## Testing

Automated tests validate the behavior of the existing architecture without becoming part of the runtime application.

Tests are organized according to the layer or boundary being validated.

```text
tests/
├── domain tests
├── application tests
├── repository/integration tests
└── workflow tests
```

Domain tests run independently of external systems.

Application tests can use test doubles to isolate application behavior from infrastructure.

Repository and persistence tests use a separate PostgreSQL test database to validate actual database behavior, relationships and constraints.

The test suite does not make real LLM API requests.

Testing is therefore a validation mechanism around the application rather than an additional runtime layer:

```text
                ┌─────────────────────┐
                │       Tests         │
                │     validation      │
                └──────────┬──────────┘
                           │
                           │ validates
                           ▼
Presentation → Application → Infrastructure
                    │              │
                    ▼              ▼
                  Domain       PostgreSQL
```

Test-specific components such as test doubles and fixtures are kept within the test environment rather than being introduced into the production architecture solely to support testing.

---

## Architectural Abstraction

Abstractions are introduced when there is a concrete reason for them.

The project does not currently maintain a generic repository inheritance hierarchy because the existing repositories do not share a sufficiently useful contract.

Similarly, infrastructure is not split into separate services unless independent deployment, scaling or operational requirements justify that complexity.

The architecture therefore follows a **modular monolith first** approach.

---

## Architecture Design Process

Architectural decisions are made around responsibilities, boundaries and dependencies.

Before implementing a feature, the following are considered:

1. What responsibility does the feature introduce?
2. Which component should own it?
3. What dependencies does it require?
4. Where should infrastructure enter the system?
5. What data crosses the boundary?
6. What is likely to change independently?
7. What complexity is justified by the current requirements?

Individual classes, methods and files are determined during implementation rather than being completely specified in advance.

This allows the architecture to evolve through actual requirements and implementation experience.

---

## Project Structure

The current project structure is:

```text
Project/
│
├── main.py
├── alembic.ini
├── .env
├── .gitignore
│
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│
├── application/
│   ├── conversationservice.py
│   └── persistenceservice.py
│
├── domain/
│   ├── context.py
│   ├── conversation.py
│   └── message.py
│
├── infrastructure/
│   ├── llm/
│   │   └── openai_provider.py
│   │
│   └── persistence/
│       ├── json/
│       │   └── json_repository.py
│       │
│       └── postgre/
│           ├── database.py
│           ├── models.py
│           └── repositories/
│               ├── conversation_repository.py
│               ├── message_repository.py
│               └── user_repository.py
│
├── presentation/
│   └── terminal.py
│
└── tests/
	├── conftest.py
    ├── test_conversation_repository.py
    ├── test_conversation.py
    ├── test_message_repository.py
    ├── test_message.py
    ├── test_openai_provider.py
    ├── test_persistence_service.py
    ├── test_user_repository.py
    └── test_persistence_workflow.py
```

Alembic is maintained outside the runtime application layers because it manages database schema evolution rather than application execution.

The JSON persistence implementation is retained as legacy infrastructure from v0.1.

The `tests/` directory is separate from the runtime application because tests validate the application but are not themselves part of its execution architecture.
