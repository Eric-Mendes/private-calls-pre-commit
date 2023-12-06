# private-calls-pre-commit
A pre-commit hook that checks whether a private function is being called outside of where it should be.

## Usage
```yaml
# .pre-commit-hooks.yaml
- id: private-calls-check
  name: private-calls-check
  description: Checks whether a private function is being called outside of where it should be.
  entry: private_calls_check
  language: python
```
