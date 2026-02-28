# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask-based LLM Ops API project using dependency injection (injector). Entry point is `app/http/app.py`.

## Commands

```bash
# Run the Flask application
.venv/bin/python app/http/app.py

# Run tests (use .venv Python)
.venv/bin/python -m pytest

# Run a single test file
.venv/bin/python -m pytest test/internal/handler/test_app_handler.py -v

# Syntax check
.venv/bin/python -m py_compile <file_path>
```

## Architecture

```
app/http/app.py          # Application entry point
internal/
  server/http.py         # Flask Http engine with exception handling
  router/router.py       # Route registration using Blueprint
  handler/               # Request handlers (controllers)
  service/               # Business logic layer
  model/                 # Data models
  schema/                # WTForms validation schemas
  exception/exception.py # Custom exceptions (FailException, NotFoundException, etc.)
pkg/
  response/              # Response helpers (Response dataclass, json(), success/fail helpers)
config/                 # Configuration
test/                    # Test files, conftest.py at root
```

## Key Patterns

- **Routing**: Routes defined in `internal/router/router.py` using Flask Blueprint
- **Exception Handling**: `internal/server/http.py` registers handler for `CustomException` and its subclasses
- **Validation**: WTForms in `internal/schema/`
- **Response Format**: Uses `pkg.response.Response` dataclass with `code`, `message`, `data` fields
- **Dependency Injection**: Uses `injector` library with `@inject` and `@dataclass` decorators

## Testing

- Tests use pytest with fixtures defined in `conftest.py`
- Mock OpenAI responses in tests using `unittest.mock.patch`
