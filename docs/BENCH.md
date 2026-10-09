# Does your AI reviewer catch them?

A fun, 10-minute protocol. Katas may already be in some models' training data, so treat results as
a signal, not science.

## Protocol

1. Pick a kata. Copy **only the code block** from its README. Don't include the tests, the hint or the spoiler.
2. Start a **fresh conversation** with the assistant you want to test and send:

   ```text
   You are reviewing a pull request. The author's task was:
   "<the prompt from the kata>"

   Review the code below. List every bug you find, most severe first. Be specific
   (function or line), and say how to fix it. If it is fine, answer exactly: LGTM.

   <paste the code>
   ```

3. Score the answer against the kata's spoiler:
   - ✅ **caught**: it names the planted bug and its consequence
   - 🟡 **vague**: it points near the bug, or says "add error handling" without the actual problem
   - ❌ **missed**: it says LGTM, or only finds style nits
   - **false alarms**: count findings that are not real bugs

4. Repeat for several katas (and ideally 2-3 runs per kata), then tally per assistant.

## Tips for a fairer comparison

- Same prompt, same settings, fresh chat each time. No hints.
- Test the assistant in the mode you actually use (chat, IDE review, PR bot).
- Try the *fixed* version from `solutions/` too: a good reviewer should say LGTM.
- Share what you find (a blog post, a thread, an issue). People love comparing reviewers.
