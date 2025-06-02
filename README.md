# Coder: Expert-level Python Code Generator

**Coder** is an advanced Python code generation engine that turns structured, semantic instructions (as dictionaries) into clean, idiomatic, and modern Python source code.  
It supports nearly every Python construct—including async, comprehensions, pattern matching, dataclasses, and more.  
Designed for AI coding tools, transpilers, and any project that needs robust Python code synthesis.

---

## Features

- **Full Python language support:**  
  All core syntax (assignments, control flow, loops, functions, classes, imports, exception handling, etc.)
- **Modern constructs:**  
  - `async`/`await`, `async for`, `async with`
  - Pattern matching (`match`/`case`, Python 3.10+)
  - Type/variable annotations, PEP 526
  - `@dataclass` and magic methods
  - Metaclasses, global/nonlocal, del
  - Docstrings, decorators, comprehensions, and more
- **Extensible:**  
  Add new handlers for new Python features or custom constructs easily.
- **Structured Input:**  
  Write algorithms as lists of semantic steps (dictionaries), not raw code.

---

## Installation

Clone or copy this repository.  
No external dependencies except Python 3.7+.

---

## Usage Example

### 1. Import and instantiate:

```python
from coder import Coder

coder = Coder()
```

### 2. Provide structured steps

```python
steps = [
    {"type": "func_def", "name": "greet", "args": ["name"], "body": [
        {"type": "expr", "expr": "print(f'Hello, {name}!')"}
    ]},
    {"type": "blank_line"},
    {"type": "main_guard", "body": [
        {"type": "func_call", "name": "greet", "args": ["'World'"]}
    ]}
]
```

### 3. Generate code

```python
code = coder.generate_code(steps)
print(code)
```

**Output:**
```python
def greet(name):
    print(f'Hello, {name}!')

if __name__ == '__main__':
    greet('World')
```

---

## Advanced Example

Handles async, pattern matching, dataclasses, etc.

```python
steps = [
    {"type": "shebang", "line": "/usr/bin/env python3"},
    {"type": "encoding", "encoding": "utf-8"},
    {"type": "dataclass", "name": "Item", "body": [
        {"type": "annotation", "target": "name", "annotation": "str"},
        {"type": "annotation", "target": "count", "annotation": "int", "value": 0}
    ]},
    {"type": "blank_line"},
    {"type": "async_func_def", "name": "fetch", "args": ["url"], "body": [
        {"type": "await", "expr": "http_get(url)", "target": "resp"},
        {"type": "return", "value": "resp"}
    ]},
    {"type": "blank_line"},
    {"type": "match", "subject": "action", "cases": [
        {"type": "case", "pattern": "'run'", "body": [
            {"type": "expr", "expr": "print('Running!')"}
        ]},
        {"type": "case", "pattern": "_", "body": [
            {"type": "expr", "expr": "print('Unknown!')"}
        ]}
    ]}
]
code = coder.generate_code(steps)
print(code)
```

---

## Extending Coder

To add a new Python construct, add a handler in the `Coder` class and register it in `self.supported_operations`.

---

## License

GPLv3

---

## Author

[Rifat-Rezwan-02](https://github.com/Rifat-Rezwan-02)

---
