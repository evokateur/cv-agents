# Chat About Chat Context Size

An LMArena Battle

## The Prompt

I'm worried about the size of the context in a chat I've been having with GPT-5. I've tried "compacting" the chat by asking for a summary that I could paste into a new chat.

1. How worried should I be about the size of the context, and are there heuristics I could use to estimate when it might be getting too large?

2. What is a good prompt for obtaining a summary that includes all relevant information from the chat, filtering out stuff that's just taking up space in the context?

## Response A

Regarding context size concerns:

You should start being mindful when your conversation history approaches 50-75% of the model's context window. Most current models have context windows ranging from 8k to 128k tokens (roughly 6k-96k words). Performance typically degrades as you approach the limit - the model may:
- Start "forgetting" earlier parts of the conversation
- Become less coherent or accurate
- Take longer to respond
- Eventually hit a hard limit and refuse to continue

Some practical heuristics:
- Each exchange (your message + response) typically uses 200-500 tokens
- Code blocks and technical content use more tokens
- After 50+ exchanges, you're likely using significant context
- If responses seem to ignore earlier context, you're probably near the limit

For creating an effective summary, here's a prompt template:

"Please create a comprehensive summary of our entire conversation that preserves all essential information. Include:

- The main topic/goal and any sub-topics we've explored
- Key decisions made or conclusions reached
- Important technical details, specifications, or requirements discussed
- Any code, formulas, or specific examples that remain relevant
- Unresolved questions or next steps identified
- Context about my specific use case or constraints mentioned

Format this as a structured brief that I can paste into a new conversation to continue where we left off. Exclude pleasantries, redundant exchanges, and any failed attempts or dead ends unless they contain important lessons learned."

This approach helps maintain continuity while significantly reducing token usage.

## Response B

Okay, let's break down your concerns about context size and how to get a good summary.

First, a small clarification: As of my last update, the most advanced publicly accessible models are typically referred to as GPT-4, GPT-4 Turbo, or GPT-4o. While these have very large context windows, "GPT-5" isn't a widely released or confirmed designation yet. However, the principles for managing context size apply to whichever advanced model you are using.

---

**1. How Worried Should You Be About Context Size?**

*   **Current Models Have Large Context Windows:** Models like GPT-4 Turbo and GPT-4o have context windows of 128,000 tokens. A token is roughly ¾ of a word in English. So, 128k tokens is approximately 90,000-100,000 words. This is *very* large – enough for a substantial novel.
*   **When to Worry:** You likely only need to worry if:
    *   Your conversation is exceptionally long and detailed, spanning potentially dozens of densely packed interactions.
    *   You've pasted large amounts of text (like documents, articles, codebases) into the chat.
    *   You start noticing the AI "forgetting" things it should know from earlier in the conversation (e.g., forgetting instructions, user preferences, previously established facts, or the overall goal).
    *   The AI's responses become less coherent, less focused, or start repeating itself in ways that suggest it's losing the thread.
*   **Heuristics for Estimation:**
    *   **Token Count (Indirect):** Since you usually can't see the token count directly in the chat interface, use the word count approximation. If your chat history likely exceeds, say, 50,000 words of *dense* interaction or pasted text, you *might* be getting close to the limits of *older* models or potentially nearing the practical limits where performance *could* degrade, even with large windows. For 128k token models, you'd need significantly more.
    *   **Behavioral Clues:** This is the most practical heuristic. Pay attention to the AI's performance. If it starts making basic errors related to conversation history, that's the primary sign.
    *   **Action as Prevention:** Summarizing periodically is a good practice *regardless* of whether you're hitting the limit. It helps maintain focus, prune unnecessary details, and ensures the core information is always readily accessible to the model in a new session.

**In summary:** For most typical chat interactions, even spanning a few hours or days, you are unlikely to hit the context window limit of modern large-context models. However, summarizing is still a valuable technique for maintaining focus and efficiency.

---

**2. Good Prompt for Obtaining a Focused Summary**

The key is to tell the AI *what* constitutes "relevant information" and what to filter out. Here’s a prompt structure you can adapt:

**Prompt Example:**

"Please act as an expert summarizer. I need you to create a concise summary of our conversation history so far. The goal is to capture all essential information needed to continue this discussion effectively in a new chat session.

**Focus on including:**

*   **Key objectives and goals** we've discussed or are working towards.
*   **Crucial decisions** made during the conversation.
*   **Important facts, constraints, or user preferences** that have been established.
*   **Action items** assigned or agreed upon (who, what, when).
*   **The core problem/topic** we are addressing.
*   **Significant context or background information** provided.
*   **Any established persona, tone, or specific instructions** I've given you about how you should behave or respond.

**Please filter out and exclude:**

*   Casual greetings, farewells, and simple acknowledgments (like "Okay," "Got it").
*   Repetitive conversational filler or small talk.
*   Redundant explanations or examples unless they illustrate a key point uniquely.
*   Information that is no longer relevant or has been superseded by later details.

**Format:** Please present the summary in a clear, structured format, perhaps using bullet points or numbered lists, organized logically (e.g., chronologically or by topic). Aim for clarity and brevity while retaining all necessary context.

**[Optional: Add specific constraints if needed, e.g., "Keep the summary under 500 words" or "Focus especially on the technical details related to X."]**

Here is the conversation history to summarize:

[Paste the conversation history here]"

---

**Why this prompt works:**

*   **Clear Role & Goal:** Sets the stage ("expert summarizer," "continue effectively").
*   **Explicit Inclusion Criteria:** Tells the AI exactly what data points are valuable.
*   **Explicit Exclusion Criteria:** Tells the AI what to ignore, helping it filter efficiently.
*   **Format Guidance:** Helps ensure the output is usable.
*   **Optional Constraints:** Allows you to fine-tune the output length or focus.

By providing these guidelines, you significantly increase the chances of getting a summary that is both comprehensive in its coverage of essential information and efficient in its exclusion of noise. Remember to review the summary the AI provides to ensure it accurately captured what you needed!

## The Winner

Response B seemed, on first reading, more immediately relevant and actionable with regard to my concerns.

A: `claude-opus-4-20250514-thinking-16k`

B: `gemini-2.5-flash-lite-preview-06-17-thinking`

However, response A may actually be more factual and cohesive. Its prompt produced a better result.

[@summary-from-prompt-a.md](summary-from-prompt-a.md)

[@summary-from-prompt-b.md](summary-from-prompt-b.md)
