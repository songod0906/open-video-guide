# ASD-STE100 Writing Guide

## 1. Requirement

Project technical text must obey ASD-STE100 Simplified Technical English, Issue 9.
Issue 9 became an international standard on January 15, 2025.

Use the official specification for the final language decision:
[ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf)

## 2. Project rules

Use these rules for all project technical text:

1. Use approved dictionary words with their approved meanings.
2. Use project terms only as technical terms.
3. Use active voice when the agent is known.
4. Use a maximum of 20 words in a procedural sentence.
5. Use a maximum of 25 words in a descriptive sentence.
6. Put only one instruction in each sentence.
7. Use the imperative form for an instruction.
8. Put one topic in each paragraph.
9. Use a maximum of six sentences in a descriptive paragraph.
10. Use a vertical list for complex information.
11. Define each abbreviation before you use it.
12. Use the same term for the same item.
13. Do not use slang, idioms, or unnecessary words.
14. Do not use a word-for-word replacement when it changes the meaning.

## 3. Technical terms

Software needs technical nouns and technical verbs.
Record approved project terms in `TERMINOLOGY.md`.

Do not add two terms for the same meaning.
Define a new term in the pull request that introduces it.

## 4. Procedures

Number steps in the necessary sequence.
Start each step with an approved command verb.

Put a condition before the command when the reader needs it first.
Use a comma between the condition and the command.

Do not put a requirement in a note.
Use a warning or caution only for a real safety condition.

## 5. Descriptions

Give one topic in each paragraph.
Use short sentences and explicit nouns.

Do not use an unclear pronoun.
Repeat the technical noun when repetition removes ambiguity.

## 6. Code and data

Do not change a program identifier only for language style.
Put identifiers in code formatting.

Do not change:

- Legal text
- License text
- Exact error text
- Exact source text
- Protocol field names
- Program identifiers
- User-provided text

Explain these items with STE text when an explanation is necessary.

## 7. Review process

Run the project checker:

```bash
python scripts/check_ste.py
```

The checker tests sentence length and a small word list.
It does not prove complete ASD-STE100 compliance.

A trained reviewer must check:

- Dictionary approval
- Approved meaning
- Part of speech
- Technical term category
- Sentence construction
- Procedure structure
- Consistent terminology

## 8. Pull request evidence

Mark the technical writing check in the pull request.
List each approved new project term.

When a rule exception is necessary, identify the exact text and reason.
