# Debugging Power Automate Flows with OpenEnv

Modern AI is changing. Instead of just predicting things, AI is now becoming an "agent" that can look at a problem, take action, and learn from the results. Most AI projects focus on games or robots, but in this project, I wanted to focus on a real-world problem: **fixing broken Power Automate flows.**

I created a simple environment using **OpenEnv** to model a very common issue: **HTTP 400 BadRequest** errors caused by mistakes in "Condition" steps.

## Why Power Automate?

If you work with automation, you know that debugging is a slow and annoying task. Usually, it looks like this:

1. A flow fails with a vague "400 BadRequest" error.
2. The error is hidden inside a Condition step.
3. There is a small typo in the formula (expression).
4. An engineer has to find the mistake and fix it manually.

This "debug-fix-check" loop is perfect for an AI agent. The agent sees the failure, tries a fix, and keeps going until the flow works.

---

## How the Environment Works

I built this environment to be simple and clear. Each "episode" is basically one debugging session.

### The Task

The agent gets a failed flow run. The goal is simple: **Fix the broken expression so the flow succeeds.**

### What the Agent Sees (Observations)

The agent receives a JSON-like summary of the problem, including:

* The error message and status.
* Which step failed.
* The inputs and outputs of the flow.
* How many attempts are left.

### What the Agent Can Do (Actions)

To keep things simple for now, the agent has one job: **Send a patch.** It tells the system which step to change and provides the new, corrected expression. If the string matches the correct fix, the flow succeeds.

### The Reward System

I used a very simple scoring system:

* **+1.0:** The flow is fixed!
* **-0.1:** Wrong fix (but you can try again).
* **-0.2:** Out of attempts (failed).

---

## The Data and the Demo

* **The Dataset:** I created a set of JSON files with real-world bug examples. The agent has to figure out the fix based only on the error logs; it never sees the "correct answer" beforehand.
* **The Demo Agent:** I built a simple agent that uses basic rules to find typos. It solved all the cases, which proves that the environment works and the feedback loop is solid.

---

## Keeping it Simple (Limitations)

This is an MVP (Minimum Viable Product). To keep it fast and easy to use:

* It only focuses on **Condition** expressions.
* It doesn't actually connect to the real Power Automate website.
* It is deterministic (no random surprises).

---

## Why This Matters

Debugging is a huge part of real work, but it’s not often used in AI benchmarks. By turning Power Automate errors into an **OpenEnv** environment, I’m trying to bridge the gap between practical automation and AI research.

In the future, I want to add more complex errors (like "Filter array" issues) and try training smarter agents using LLMs.

**Conclusion:** AI agents need to learn how to handle messy, real-world systems. This project is a small step toward making AI more helpful in our daily office tasks.
