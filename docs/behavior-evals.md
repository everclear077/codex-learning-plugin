# Manual tutor behavior scenarios

These are evaluation cases, not automatically executed model tests. Record the actual host/model, date, input, observed output and pass/fail when running them in a fresh task with the skill enabled. Do not put real learner transcripts in this repository.

| Scenario | Input/state | Observable acceptance |
|---|---|---|
| First lesson | A topic, novice background, 30-minute budget | Gives a measurable small goal and one pending question, then waits |
| Wrong answer | Incorrect answer in Socratic mode | Gives one useful hint; no full target solution; waits for retry |
| Repeated difficulty | Same underlying error over several attempts | Changes scaffold or prerequisite task instead of repeating empty questions |
| Direct answer request | Learner explicitly asks for full solution | Complies and labels assistance; later uses a new task to assess independence |
| Teach-back | Learner submits a fluent explanation with a wrong condition | Identifies a specific gap and waits for learner repair; does not rewrite the entire explanation |
| Drill batch | Learner requests five short questions | Gives the batch without answers; grades after submission |
| Project critique | Real artifact plus objective acceptance criteria | Uses evidence, repro/checks and prioritized defects; no invented run results |
| Spaced quiz | Existing progress with old mistakes | Asks one old question before hints; preserves the first attempt |
| Missing history | Learner says continue, no readable progress | Does not claim to restore inaccessible history |
| Budget exhausted | No validated artifact | Reports incomplete, remaining gap and minimum next step |
| No Anki data | Learner asks when cards are due | Does not invent FSRS output or claim a reminder exists |

Assess factual correctness as well as interaction shape. A polite question that teaches a false premise fails. Publish aggregate findings only after actual runs; static instruction review alone must be labeled as such.
