# ADR-0001: Use a Modular Monolith

**Status:** Accepted

## Context

AI_Agent_Memory is initially a single application with a small number of components and no requirement for independent deployment or scaling.

The project requires clear separation of responsibilities but does not currently require distributed services.

## Decision

Use a **layered modular-monolith architecture**.

The application remains a single deployable application while separating:

- Presentation
- Application
- Domain
- Infrastructure

## Rationale

This provides clear architectural boundaries without introducing the operational complexity of microservices.

The architecture can be decomposed later if independent deployment, scaling, or ownership becomes a genuine requirement.

## Consequences

### Positive

- simple deployment
- simple local development
- clear responsibility boundaries
- low operational overhead
- components can evolve behind defined boundaries within the application

### Negative

- components still share one application runtime
- components cannot be independently deployed or scaled
- future decomposition may require additional boundary work

## Revisit When

Consider decomposition only when concrete requirements justify independently deployable or independently scalable components.

---

# ADR-0002: Use PostgreSQL for Persistent Application Data

**Status:** Accepted

## Context

The initial v0.1 implementation used a JSON file for conversation persistence.

As the application developed, persistent state expanded to include:

- multiple users
- multiple conversations per user
- multiple messages per conversation
- meetings containing multiple conversations
- relationships between these entities
- persistent identifiers
- timestamps
- user and conversation summaries
- structured queries and updates

A flat JSON document is not an appropriate primary persistence model for these requirements.

## Decision

Use PostgreSQL as the primary persistent data store.

SQLAlchemy is used for ORM-based database access and Alembic is used for schema migrations.

## Rationale

A relational database provides:

- explicit relationships
- foreign-key constraints
- structured querying
- transaction support
- schema evolution
- a foundation for future persistence requirements

The relational model also provides a durable foundation for the application's future memory and retrieval capabilities.

## Consequences

The application gains a robust persistence foundation but also introduces database infrastructure, migrations, and session/transaction management.

The additional complexity is justified by the transition from a single-conversation prototype to a persistent application with multiple related entities.

The original JSON persistence implementation remains as legacy infrastructure but is no longer part of the active persistence workflow.

---

# ADR-0003: Separate Domain Models from Persistence Models

**Status:** Accepted

## Context

The application needs to represent concepts such as users, conversations, messages, meetings, and runtime context, while PostgreSQL requires its own persistence representation.

A direct dependency between domain objects and SQLAlchemy models would couple application concepts to the database implementation.

## Decision

Maintain separate domain objects and SQLAlchemy persistence models.

```text
Domain Object
      │
      │ mapping
      ▼
SQLAlchemy Model
      │
      ▼
PostgreSQL
```
