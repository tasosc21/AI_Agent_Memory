# ADR-0001: Use a Modular Monolith

**Status:** Accepted

## Context

AI_Agent_Memory is initially a single application with a small number of components and no requirement for independent deployment or scaling.

The project requires clear separation of responsibilities but does not currently require distributed services.

## Decision

Use a **layered modular-monolith architecture**.

The application remains a single deployable application while separating:

* Presentation
* Application
* Domain
* Infrastructure

## Rationale

This provides clear architectural boundaries without introducing the operational complexity of microservices.

The architecture can be decomposed later if independent deployment, scaling or ownership becomes a genuine requirement.

## Consequences

### Positive

* simple deployment
* simple local development
* clear responsibility boundaries
* low operational overhead
* components can evolve independently within the application

### Negative

* components still share one application runtime
* future decomposition may require additional boundary work

## Revisit When

Consider decomposition only when concrete requirements justify independently deployable or independently scalable components.

---

# ADR-0002: Use PostgreSQL for Persistent Application Data

**Status:** Accepted

## Context

The initial v0.1 implementation used a JSON file for conversation persistence.

The system now needs to represent:

* multiple users
* multiple conversations per user
* multiple messages per conversation
* relationships between these entities
* persistent identifiers
* timestamps
* structured queries

A flat JSON document is not an appropriate long-term persistence model for these requirements.

## Decision

Use PostgreSQL as the primary persistent data store.

SQLAlchemy is used for ORM-based database access and Alembic is used for schema migrations.

## Rationale

A relational database provides:

* explicit relationships
* foreign-key constraints
* structured querying
* transaction support
* schema evolution
* a foundation for future persistence requirements

## Consequences

The application gains a more robust persistence foundation but also introduces database infrastructure, migrations and session/transaction management.

The additional complexity is justified by the transition from a single conversation prototype to a multi-user persistent application.

---

# ADR-0003: Separate Domain Models from Persistence Models

**Status:** Accepted

## Context

The application needs to represent concepts such as users, conversations and messages while PostgreSQL requires its own persistence representation.

A direct one-to-one dependency between domain objects and SQLAlchemy models would couple application concepts to the database implementation.

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

## Rationale

The domain model and database schema serve different purposes.

The domain represents concepts and behaviour required by the application.

The persistence model represents how those concepts are stored.

Keeping them separate allows either side to evolve without unnecessarily forcing changes onto the other.

## Consequences

### Positive

* reduced coupling to SQLAlchemy
* domain model remains persistence-independent
* database schema can evolve independently
* persistence concerns remain isolated

### Negative

* mapping between domain and persistence models introduces additional code

## Revisit When

The separation should be reconsidered if it creates significant unnecessary complexity relative to the actual domain requirements.
