# yamlfmt-pre-commit-mirror

Mirror of the `yamlfmt` pre-commit hook for `pre-commit`. Supports `pre-commit` versions 2.9.2 and later.

## Usage

Add this to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/PFCCLab/yamlfmt-pre-commit-mirror.git
  rev: v0.20.0
  hooks:
    - id: yamlfmt
```
