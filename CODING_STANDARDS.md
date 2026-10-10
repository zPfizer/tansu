# Coding standards

## Clarify first
State your assumptions. When several readings exist and the choice changes the result, list them and ask. Name a simpler approach when one exists, and push back when warranted.

## Smallest diff
Write the minimum code the request needs: no unrequested features, single-use abstractions, configurability, or error handling for impossible cases. Trace every changed line to the request. Match the existing style. Leave adjacent code, comments, and formatting unchanged, and refactor only what is broken. Report unrelated dead code and leave it in place. Remove only the imports, variables, and functions your change made unused.

## Verified goals
Turn each task into a checkable success criterion:
- Validation: write tests for invalid inputs, then make them pass.
- Bug: write a test that reproduces it, then make it pass.
- Refactor: tests pass before and after.

For multi-step work, write a plan as `1. [Step] → verify: [check]`. Loop until each check passes.
