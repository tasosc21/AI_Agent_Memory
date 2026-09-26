
# AI_Agent_Memory Prompts

Prompt files define AI_Agent's identity, behavior, application context, and instructions for maintaining persistent user and conversation state.

The prompt files are divided into two groups.

## Runtime Prompts

These prompts are used during normal conversation:

- `system.txt` — AI_Agent's identity, personality, conversational behavior, continuity, and general behavioral rules.
- `developer.txt` — application-level instructions describing how AI_Agent should interpret and use the context supplied by the application.

## State and Summary Prompts

These prompts are used to summarize conversations and update persistent information:

- `summarise_user.txt` — creates or updates a user's current conversation summary.
- `summarise_all_users.txt` — creates or updates a summary of the current meeting involving multiple users.
- `update_user_profile.txt` — updates a user's important and relatively durable profile information based on their conversation.
- `update_user_summary.txt` — updates a user's secondary persistent information, such as preferences, recurring interests, or other useful context.

The prompt files are kept separate from application code so that AI_Agent's behavior and state-management instructions can be modified without changing application logic.

These prompt files are intentionally excluded from version control.
