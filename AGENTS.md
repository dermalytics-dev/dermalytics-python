# Dermalytics Python SDK — agent guidance

## Purpose

This repository publishes the Python client for the Dermalytics API. The package's public methods, models, errors, and examples are a versioned developer contract.

## Work in this repository

- Read `README.md` and `pyproject.toml` before changing behavior. Verify API assumptions against the deployed service.
- Preserve backward compatibility unless a breaking release is explicitly requested. Update implementation, typing, tests, and examples together.
- Never embed API keys or real customer data in source, fixtures, examples, distributions, or logs.
- Do not hand-edit generated distribution artifacts or publish to PyPI unless explicitly requested.
- Keep support for the Python versions declared in `pyproject.toml`.

## Verify

```sh
pytest
mypy dermalytics
python -m build
```

