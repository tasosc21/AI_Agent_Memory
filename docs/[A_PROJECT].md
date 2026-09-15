# [A PROJECT]

> A persistent AI assistant built as a long-term software engineering and machine learning project.

## Overview

This project is an attempt to build an AI assistant from the ground up as a real software system rather than as a single LLM wrapper.

The long-term goal is a persistent assistant that can:

* converse with users
* maintain long-term memory
* distinguish between different users
* acquire knowledge through conversations, documents and external research
* retrieve relevant knowledge and memories
* use external tools
* maintain evolving internal state
* expose an API and support multiple interfaces

---

## Roadmap

The project will evolve through progressively more capable versions.

The roadmap is intentionally flexible. Features are added when the existing system provides a reason to build them rather than being implemented in advance.

### Planned development

1. Requirements and architecture
2. Core project structure
3. HTTP and REST APIs
4. PostgreSQL and data modelling
5. Automated testing
6. Persistent memory
7. Embeddings and RAG
8. Web research and knowledge acquisition
9. Agent architecture
10. Security
11. Async processing and concurrency
12. Redis, queues and background workers
13. Machine-learning pipeline
14. React and TypeScript interface
15. Docker and containerisation
16. CI/CD
17. Go
18. .......

The roadmap is a direction, not a contract. Requirements discovered during development may change the order or remove planned components entirely.

---

## Architecture

The project uses a **layered modular-monolith architecture**. The application runs as a single process/application, while responsibilities are separated into distinct layers.

### Layers

**Presentation**
Handles interaction with the user. T

**Application**
Coordinates application workflows.

**Domain**
Contains concepts and rules belonging to the problem being modeled.

**Infrastructure**
Contains implementations that interact with external systems.

`main.py` acts as the application entry point and composition root. It creates the concrete components and connects them together.

---

### Architecture Design Process

Architecture is designed at the level of important decisions rather than individual implementation details.

Before implementing a feature, the following questions are considered:

1. What responsibility does this feature introduce?
2. Which existing component should own that responsibility?
3. What does the component need from the rest of the system?
4. Should that dependency be direct or represented through an interface?
5. Where does external infrastructure enter the system?
6. What data needs to cross the boundary?
7. What is likely to change?
8. What complexity is actually justified?

The exact classes, methods and files are decided during implementation.

The architecture is therefore expected to be refined through development rather than completely specified beforehand.

---

## v0.1 — Send, Receive & Persist messages

### Objective

Build the smallest complete version of the system:

```text
User
 ↓
Terminal
 ↓
ConversationService
 ↓
LLM
 ↓
ConversationService
 ↓
Terminal
```

Receive a user message, generate an LLM response, display it, and persist the conversation locally using JSON.

---

### Delivered

v0.1 provides:

* terminal-based interaction
* LLM communication
* conversation history through JSON
* separation between application logic and infrastructure

---

## Architecture

```text
                   ┌────────────────────┐
                   │      Terminal      │
                   │   Presentation     │
                   └─────────┬──────────┘
                             │
                             ▼
                   ┌────────────────────┐
                   │ ConversationService│
                   │    Application     │
                   └───────┬─────┬──────┘
                           │     │
              ┌────────────┘     └─────────────┐
              ▼                                ▼
    ┌──────────────────┐             ┌────────────────────────┐
    │  **LLMProvider   │             │**ConversationRepository│
    │  Infrastructure  │             │      Infrastructure    │
    └────────┬─────────┘             └──────────┬─────────────┘
             │                                  │
             ▼                                  ▼
         OpenAI API                            JSON    
  
**Infostructure(abstractions) doesn't exist yet.
**Will be added as needed.
```

The application layer coordinates the conversation use case.

Infrastructure implements communication with external systems and persistence.

The terminal remains a thin presentation layer.

---

### Components & Responsibilities

```text
project/
├── main.py
├── presentation/
│   └── terminal.py
├── application/
│   └── conversationservice.py
├── domain/
│   └── ...
└── infrastructure/
    ├── llm/
    │   └── openai_provider.py
    └── persistence/
        └── json_repository.py
```

#### Presentation — Terminal

The terminal is responsible for interaction with the user.

It:

* receives user input
* displays the generated response

---

#### Application — ConversationService

`ConversationService` owns the **send-message workflow**.

Conceptually:

```text
send_message(...)
    │
    ├── retrieve conversation history
    │
    ├── request LLM response
    │
    ├── persist conversation
    │
    └── return response
```

It coordinates the operation but does not implement the details of external systems.

For example, it knows that a response must be generated, but it does not know how the OpenAI SDK works.

The service depends on `openai_provider` and `json_repository` .

---

#### Infrastructure — LLM — OpenAIProvider

`OpenAIProvider` is responsible for communicating with the OpenAI API.

It:

* manages the OpenAI client
* sends conversation messages to the model
* extracts and returns the generated response

---

#### Infrastructure — Persistence — JsonRepository

`JsonRepository` implements the conversation persistence required by the application.

It:

* saves user and AI messages
* loads conversation history during application startup
* reads and writes conversation data to `conversations.json`

The repository is responsible for persistence rather than deciding how conversation data should be used by the LLM.

---

### Data Model

For v0.1, conversation data is stored as JSON.

The persisted conversation consists of message objects containing:

```text
Message
──────────────
role
content
```

`role` identifies the source of the message:

```text
user
assistant
```

`content` contains the message text.

The JSON repository is responsible for reading and writing this data to the local persistence files.

The model is intentionally minimal at this stage. Additional metadata such as message IDs, timestamps, conversation IDs, summaries, and user-specific information will be introduced in future versions.

---

### Runtime Flow

A normal interaction follows this path:

```text
1. User enters a message through Terminal
           ↓
2. main.py receives the message
           ↓
3. main.py passes the message to ConversationService
           ↓
4. ConversationService retrieves the conversation
   from JsonRepository
           ↓
5. ConversationService passes the conversation
   to LLMProvider
           ↓
6. LLMProvider communicates with OpenAI
           ↓
7. OpenAI returns the response
           ↓
8. ConversationService persists the messages
   through JsonRepository
           ↓
9. ConversationService returns the response to main.py
           ↓
10. main.py passes the response to Terminal
           ↓
11. Terminal displays the response
```

---

## Limitations

v0.1 intentionally has very little intelligence beyond the underlying LLM.

It does not yet provide:

* semantic retrieval
* embeddings
* RAG
* knowledge acquisition
* web research
* tool use
* planning
* background processing
* multi-user identity resolution
* temporal knowledge
* authentication
* API access
* web interface
* automated testing beyond what is introduced during development
* production deployment

These are future requirements, not missing pieces of v0.1.

---

## Status

**v0.1 — Core Conversation**

The first complete application workflow is established.

The system can accept a message, communicate with an LLM, return a response and persist the conversation in JSON.

---

# v0.2 — [Next Version]
