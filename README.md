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

## Caveats
This tool CAN'T identify function calls when they're an attribute like the example below. We are open to contributions, though, so if you know how to fix this, please do!

```python
import foo


value = foo._bar()
```