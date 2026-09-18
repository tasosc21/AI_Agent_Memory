
# AI_Agent_Memory

> A persistent AI assistant developed as a long-term software engineering and machine learning project.

## Overview

AI_Agent_Memory is an AI assistant developed as a software system rather than as a single LLM wrapper.

The long-term objective is to build a persistent assistant capable of:

* conversing with users
* maintaining long-term memory
* distinguishing between users and conversations
* acquiring knowledge from conversations, documents and external sources
* retrieving relevant knowledge and memories
* using external tools
* maintaining evolving internal state

Development is incremental. Each version introduces a specific capability or architectural improvement while keeping the system understandable and maintainable.

---

## Current Status

**Current version: v0.2 — PostgreSQL Persistence**

The project currently has:

* a layered modular-monolith architecture
* terminal-based interaction
* LLM integration
* PostgreSQL persistence
* users, conversations and messages
* SQLAlchemy ORM
* Alembic database migrations
* separation between domain and persistence models
* runtime application context

The next development focus is automated testing of the application and persistence layers.

---

## Architecture

The application uses a **layered modular-monolith architecture**.

```text
Presentation
     ↓
Application
     ↓
Domain
     ↑
Infrastructure
```

The application runs as a single application while separating presentation, application logic, domain concepts and infrastructure concerns.

See [`docs/architecture.md`](docs/architecture.md) for the current architecture and design principles.

---

## Development

Development is organized into incremental versions.

Each version has a specific objective and introduces only the complexity justified by the requirements at that stage.

See [`docs/development.md`](docs/development.md) for the development history.

---

## Documentation

| Document                 | Purpose                                     |
| ------------------------ | ------------------------------------------- |
| `README.md`            | Project overview and current status         |
| `docs/architecture.md` | Current architecture and system boundaries  |
| `docs/development.md`  | Version history and development progression |
| `docs/database.md`     | Database model and persistence architecture |
| `docs/decisions/`      | Significant architectural decisions         |

---

## Roadmap

The roadmap is directional rather than a fixed implementation schedule.

Potential future areas include:

1. Automated testing
2. HTTP / REST API
3. Persistent memory
4. Embeddings and RAG
5. Knowledge acquisition and web research
6. Agent architecture
7. Authentication and authorization
8. Asynchronous processing
9. Background workers and queues
10. Machine-learning components
11. Web interface
12. Containerisation
13. CI/CD
14. Additional systems programming and infrastructure work

Technologies and features will be introduced when they solve an identified problem or support a concrete requirement. Planned components may therefore change, be reordered or be removed.

---

## Development Principle

The project is developed incrementally, with an emphasis on clear boundaries, explicit design decisions and justified complexity.

The goal is to progressively evolve the system into a maintainable AI application rather than to implement its eventual architecture prematurely.
