---
license: mit
tags:
  - openenv
  - reinforcement-learning
  - agentic-ai
  - debugging
  - power-automate
  - automation
  - llm
library_name: openenv
task_categories:
  - reinforcement-learning
  - reasoning
  - debugging
datasets:
  - custom
metrics:
  - success-rate
language:
  - en
pretty_name: OpenEnv Flow Debugger
---


# OpenEnv Flow Debugger (Just a Simple Version for Now!)

This project is a small, easy-to-use debugging tool built with OpenEnv. It's inspired by those tricky real-world problems we hit in tools like Power Automate.

Our environment focuses on a super common issue: those annoying '400 BadRequest' errors that pop up when a condition in your automation flow has a syntax mistake.

The main idea here isn't to build a perfect smart agent right away. Instead, we want to create a clear, realistic, and expandable way to test and improve how agents fix bugs.

---

## What You Need to Do

Imagine you have a Power Automate Flow that just failed.

It failed because of an "HTTP 400 BadRequest" error.
This error happened in a "Condition" step.
And the condition expression has a tiny syntax error.

Your job as the agent is to fix that broken condition expression so the flow can run perfectly.

Each time you play (each "episode"), it's like facing a real-life debugging puzzle that automation engineers deal with all the time.

---

## What You See (Observation Space)

At each step, you'll get some info in a JSON-like format. It includes:

-   `case_id`: A unique ID for this specific problem.
-   `run_status`: Tells you if the flow is still 'Failed' or 'Succeeded'.
-   `failed_step`: Which step caused the problem.
-   `error`: Details about the error, like the code and a message.
-   `steps`: A list of all the steps in the flow, showing their inputs and outputs.
-   `attempts_left`: How many more tries you have to fix it.

**Example observation (kept simple):**

```
case_id: CASE_001
run_status: Failed
failed_step: Condition_Check
error: code=400, message=BadRequest, details=InvalidTemplate: The expression is invalid
steps:
- Compose_Ext (Succeeded, outputs: xlsx)
- Condition_Check (Failed, expression: @equals(outputs('Compose_Ext'),'xlsx')
attempts_left: 3
```

---

## What You Can Do (Action Space - Just Starting!)

Right now, in this simple version, you can only do one type of action.

You can submit a `patch_step` action. This action targets the `Condition_Check` step and updates its `inputs.expression` field.

**Example action:**

```
action = patch_step
step = Condition_Check
field = inputs.expression
value = @equals(outputs('Compose_Ext'),'xlsx')
```

For now, your fix needs to be an *exact* match to what's expected for it to count as correct.

---

## How You Get Graded (Reward Function)

Our scoring system is pretty straightforward:

-   **+1.0** if you successfully fix the flow.
-   **-0.1** for trying an incorrect fix (but you still have tries left).
-   **-0.2** if you run out of tries without fixing it.

The game (episode) ends when the flow is fixed, or when you run out of chances.

---

## The Problems (Dataset)

The specific bugs we're trying to fix are stored in JSON files here:

`flow_debugger_env/data/cases.json`

Each problem includes the messed-up flow state, error details, and a hidden 'gold_fix' (the right answer) that the environment uses to check your work. You, the agent, never see this 'gold_fix'.

---

## How to Run the Example

Just run the `demo.py` file from the main project folder like this:

`python demo.py`

The demo will pick a random bug, use a basic rule-based agent to try and fix the condition expression, and then show you how it went.

---

## What This Can't Do Yet (Limitations)

This simple version is kept small on purpose:

-   It only deals with syntax errors in Condition expressions.
-   It doesn't actually run real Power Automate flows.
-   It doesn't connect to any outside services or APIs.
-   It's not doing fancy AI learning (like reinforcement learning) yet.

Keeping things simple means it's fast, predictable, and easy for us to build on later.

---

## What's Next?

We could add more cool stuff later, like:

-   Figuring out errors in 'filter array' settings.
-   Dealing with 'null' values or wrong data types.
-   Fixing multiple steps at once.
-   Using smarter, AI-powered agents.
-   Training AI using special tools like TRL or Unsloth.
-   Adding 'Green Agent' wrappers.

---

## Why We Made This

Debugging Power Automate is a real headache for many, and it's a big deal. This environment turns those everyday automation failures into a structured task for agents and a useful testbed for learning and experimenting with OpenEnv.
