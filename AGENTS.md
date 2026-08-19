# AGENTS.md — Good and Bad Behaviours for Autonomous Systems

## The Core Principle

**NEVER prompt an agent with what to validate. The agent must READ from the database and DECIDE what to do.**

---

## BAD BEHAVIOURS (DO NOT DO)

### 1. Don't tell Hermes what to verify
```
BAD:  "Verify that OpenAIRE prize is 500 euros"
GOOD: "Read the database, find what needs validation, validate it"
```

### 2. Don't hardcode data in prompts
```
BAD:  "Check these 5 specific facts: X, Y, Z..."
GOOD: "Query the database for unvalidated facts and verify them"
```

### 3. Don't run the same test twice
```
BAD:  Run the same validation suite every time
GOOD: Only validate facts that haven't been validated yet
```

### 4. Don't skip the database
```
BAD:  "Search the web for opportunities"
GOOD: "Read the database, identify gaps, search for what's missing"
```

### 5. Don't prompt with the answer
```
BAD:  "Is the OpenAIRE prize 500 euros?"
GOOD: "What is the OpenAIRE prize? Verify it from the source."
```

---

## GOOD BEHAVIOURS (ALWAYS DO)

### 1. Read first, act second
```
READ database → identify what needs work → execute skill → log result
```

### 2. Use skills, not prompts
```
opportunity-hunter: finds NEW things
opportunity-verify: validates existing data
opportunity-monitor: checks for changes
```

### 3. Let the agent decide
```
Don't: "Validate fact X"
Do:    "What facts in the database need validation?"
```

### 4. Log everything
```
Every action → database event
Every validation → validation_results table
Every discovery → opportunities table
```

### 5. Be autonomous
```
The system should run without human prompts.
Read DB → identify gaps → search → validate → store → repeat.
```

---

## The Pattern (from Dell)

```
sources.json → DB → poll → discover → DB → events → DB
```

**Everything reads from the database. Nothing is hardcoded in prompts.**

---

## Hermes Skill Usage

### When to use each skill
- **opportunity-hunter**: DB has < 50 opportunities, search for more
- **opportunity-verify**: DB has unvalidated facts, verify them
- **opportunity-monitor**: Check for deadline changes, URL liveness

### How Hermes should behave
1. Read the database first
2. Identify what's missing or unvalidated
3. Execute the appropriate skill
4. Store results back to database
5. Log all actions

### What NOT to do
- Don't ask "should I validate X?"
- Don't prompt with specific facts to check
- Don't skip the database read
- Don't run the same validation twice
