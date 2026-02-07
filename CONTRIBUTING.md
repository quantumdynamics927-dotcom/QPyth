# Contributing to QuantumPytho

Thanks for your interest in contributing! This project aims for scientific correctness and clean engineering. Please read this guide before submitting changes.

## Code of Conduct

By participating, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

1. Fork the repository and create a new branch.
2. Make your changes with tests or proofs where appropriate.
3. Run linting and tests locally.
4. Open a Pull Request with a clear description.

## Development Setup

```bash
git clone https://github.com/quantumdynamics927-dotcom/QPyth.git
cd QPyth
pip install -e .[dev]
```

## Lint and Test

```bash
ruff check .
ruff format .
pytest
```

## Guidelines

- Keep quantum/maths content physically correct and referenced when possible.
- Avoid fabricated results in examples or tests.
- Prefer readable, well-typed Python.
- Keep CLI UX stable.

## Pull Request Checklist

- [ ] Lint passes: `ruff check .`
- [ ] Format passes: `ruff format .`
- [ ] Tests pass: `pytest`
- [ ] Documentation updated if needed
