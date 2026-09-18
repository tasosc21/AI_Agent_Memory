
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

**Current version: v0.3.0 — Automated Testing**

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
* automated tests for domain, application and persistence behavior
* a separate PostgreSQL test database

The next development focus will be determined by the requirements that emerge from the existing system.

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
| `docs/ADR.md/`         | Significant architectural decisions         |

---

## Roadmap

The roadmap is directional rather than a fixed implementation schedule.

Potential future areas include:

1. HTTP / REST API
2. Persistent memory
3. Embeddings and RAG
4. Knowledge acquisition and web research
5. Agent architecture
6. Authentication and authorization
7. Asynchronous processing
8. Background workers and queues
9. Machine-learning components
10. Web interface
11. Containerisation
12. CI/CD
13. Additional systems programming and infrastructure work

Technologies and features will be introduced when they solve an identified problem or support a concrete requirement. Planned components may therefore change, be reordered or be removed.

---

## Development Principle

The project is developed incrementally, with an emphasis on clear boundaries, explicit design decisions and justified complexity.

The goal is to progressively evolve the system into a maintainable AI application rather than to implement its eventual architecture prematurely.
