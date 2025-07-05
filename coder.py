"""
Expert-level Python code generator from semantic, structured instructions.

Now with advanced features:
- Async/await, pattern matching, global/nonlocal, del, variable/type annotations,
  shebang/encoding, dunder/module vars, magic methods, metaclasses, generator expressions,
  @dataclass.

Extend by adding new handlers to self.supported_operations.

Supports new Python features:
- Positional-only and keyword-only parameters
- Inline type alias definitions
- Future import statements
- Explicit __slots__ in class definitions
- F-string debugging (f"{x=}")
- contextlib decorators (e.g. @contextmanager)
- Unpacking in function arguments (*args, **kwargs)
- match/case “as” bindings and star patterns
- Walrus operator (:=)
- New PEP additions (e.g. Python 3.12–3.13 features)
- Exception chaining (raise ... from ...)
- yield from delegation
- Multiple contexts in a single with statement
- Decorator factories (decorators with arguments)
- Sequence unpacking in assignment targets (e.g. a, *rest, b = ...)
- Starred patterns inside match cases
- Chained comparisons and conditional expressions
- Dynamic imports or importlib usage
- Multiple-alias imports in one statement
- Parameterized @dataclass arguments
- Semantic handlers for exec and eval
- Specialized support for mypy-style pragmas (# type: ...)
"""

from typing import List, Dict, Any, Optional

class Coder:
    def __init__(self, indent_spaces: int = 4):
        self.indent_spaces = indent_spaces
        self.supported_operations = {
            # Basics
            "assign": self._handle_assign,
            "expr": self._handle_expr,
            "comment": self._handle_comment,
            "docstring": self._handle_docstring,
            "blank_line": self._handle_blank_line,
            # Control flow
            "if": self._handle_if,
            "elif": self._handle_elif,
            "else": self._handle_else,
            "for": self._handle_for,
            "while": self._handle_while,
            "break": self._handle_break,
            "continue": self._handle_continue,
            "pass": self._handle_pass,
            # Functions & calls
            "func_def": self._handle_func_def,
            "func_call": self._handle_func_call,
            "return": self._handle_return,
            "lambda": self._handle_lambda,
            "yield": self._handle_yield,
            "yield_from": self._handle_yield_from,  # NEW
            # Classes
            "class_def": self._handle_class_def,
            # Decorators
            "decorator": self._handle_decorator,
            "decorator_factory": self._handle_decorator_factory,  # NEW
            # Imports & modules
            "import": self._handle_import,
            "from_import": self._handle_from_import,
            "importlib_import": self._handle_importlib_import,  # NEW
            "multi_alias_import": self._handle_multi_alias_import,  # NEW
            # Data structures
            "list_comp": self._handle_list_comp,
            "dict_comp": self._handle_dict_comp,
            "set_comp": self._handle_set_comp,
            # Exception handling
            "try": self._handle_try,
            "raise": self._handle_raise,
            "raise_from": self._handle_raise_from,  # NEW
            "assert": self._handle_assert,
            # With/context managers
            "with": self._handle_with,
            "multi_with": self._handle_multi_with,  # NEW
            # Main guard
            "main_guard": self._handle_main_guard,
            # Advanced (NEW)
            "async_func_def": self._handle_async_func_def,
            "await": self._handle_await,
            "async_for": self._handle_async_for,
            "async_with": self._handle_async_with,
            "match": self._handle_match,
            "case": self._handle_case,
            "global": self._handle_global,
            "nonlocal": self._handle_nonlocal,
            "del": self._handle_del,
            "annotation": self._handle_annotation,
            "shebang": self._handle_shebang,
            "encoding": self._handle_encoding,
            "dunder": self._handle_dunder,
            "magic_method": self._handle_magic_method,
            "metaclass_class_def": self._handle_metaclass_class_def,
            "generator_expr": self._handle_generator_expr,
            "dataclass": self._handle_dataclass,
            "parameterized_dataclass": self._handle_parameterized_dataclass,  # NEW
            # NEW FEATURES
            "type_alias": self._handle_type_alias,
            "future_import": self._handle_future_import,
            "walrus": self._handle_walrus,
            "fstring_debug": self._handle_fstring_debug,
            "type_params": self._handle_type_params,  # Python 3.12/3.13 PEP695/PEP696 stub
            "exec": self._handle_exec,  # NEW
            "eval": self._handle_eval,  # NEW
            "mypy_pragma": self._handle_mypy_pragma,  # NEW
            "unpack_assign": self._handle_unpack_assign,  # NEW
            "chained_comparison": self._handle_chained_comparison,  # NEW
            "cond_expr": self._handle_cond_expr,  # NEW
        }

    def generate_code(self, steps: List[Dict[str, Any]], indent: int = 0) -> str:
        code_lines = []
        for step in steps:
            op_type = step.get("type")
            handler = self.supported_operations.get(op_type)
            if handler:
                lines = handler(step, indent)
                if isinstance(lines, str):
                    lines = [lines]
                code_lines.extend(lines)
            else:
                raise ValueError(f"Unsupported operation: {op_type}")
        return "\n".join(l for l in code_lines if l is not None)

    def _indent(self, level: int) -> str:
        return " " * (self.indent_spaces * level)

    # ---- Basic Handlers ----
    def _handle_assign(self, step, indent):
        targets = step["target"]
        if isinstance(targets, list):
            # Sequence unpacking, e.g. a, *rest, b = ...
            targets = ", ".join(targets)
        value = step["value"]
        # Specialized support for mypy-style pragma
        pragma = step.get("mypy_pragma")
        line = f"{self._indent(indent)}{targets} = {value}"
        if pragma:
            line += f"  # type: {pragma}"
        return line

    def _handle_unpack_assign(self, step, indent):
        # Explicit handler for assignment with unpacking/sequence targets
        targets = ", ".join(step["targets"])
        value = step["value"]
        pragma = step.get("mypy_pragma")
        line = f"{self._indent(indent)}{targets} = {value}"
        if pragma:
            line += f"  # type: {pragma}"
        return line

    def _handle_expr(self, step, indent):
        return f"{self._indent(indent)}{step['expr']}"

    def _handle_comment(self, step, indent):
        return f"{self._indent(indent)}# {step['text']}"

    def _handle_docstring(self, step, indent):
        doc = step["text"].replace('"""', r'\"\"\"')
        return f'{self._indent(indent)}"""{doc}"""'

    def _handle_blank_line(self, step, indent):
        return ""

    # ---- Control Flow ----
    def _handle_if(self, step, indent):
        lines = [f"{self._indent(indent)}if {step['condition']}:"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) or self._indent(indent+1) + "pass")
        for branch in ("elif", "else"):
            if branch in step:
                branch_step = step[branch]
                branch_handler = self.supported_operations[branch]
                branch_lines = branch_handler(branch_step, indent)
                lines.extend(branch_lines)
        return lines

    def _handle_elif(self, step, indent):
        lines = [f"{self._indent(indent)}elif {step['condition']}:"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) or self._indent(indent+1) + "pass")
        if "elif" in step:
            lines.extend(self._handle_elif(step["elif"], indent))
        if "else" in step:
            lines.extend(self._handle_else(step["else"], indent))
        return lines

    def _handle_else(self, step, indent):
        lines = [f"{self._indent(indent)}else:"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) or self._indent(indent+1) + "pass")
        return lines

    def _handle_for(self, step, indent):
        lines = [f"{self._indent(indent)}for {step['var']} in {step['iterable']}:"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) or self._indent(indent+1) + "pass")
        return lines

    def _handle_while(self, step, indent):
        lines = [f"{self._indent(indent)}while {step['condition']}:"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) or self._indent(indent+1) + "pass")
        return lines

    def _handle_break(self, step, indent):
        return f"{self._indent(indent)}break"

    def _handle_continue(self, step, indent):
        return f"{self._indent(indent)}continue"

    def _handle_pass(self, step, indent):
        return f"{self._indent(indent)}pass"

    # ---- Functions & Calls ----
    def _handle_func_def(self, step, indent):
        decorators = step.get("decorators", [])
        lines = []
        for deco in decorators:
            lines.append(f"{self._indent(indent)}@{deco}")
        # --- Argument signature construction with all modern features ---
        args_sig_parts = []
        po_args = step.get("positional_only", [])   # e.g. ['a', 'b']
        args = step.get("args", [])                 # e.g. ['c', 'd']
        vararg = step.get("vararg")                 # e.g. "args"
        ko_args = step.get("keyword_only", [])      # e.g. ['e', 'f']
        kwarg = step.get("kwarg")                   # e.g. "kwargs"

        # Positional-only
        if po_args:
            args_sig_parts.extend(po_args)
            args_sig_parts.append("/")  # positional marker

        # Regular args
        args_sig_parts.extend(args)

        # *args (vararg)
        if vararg:
            args_sig_parts.append(f"*{vararg}")
        else:
            # Insert * for keyword-only if present, but no *args
            if ko_args:
                args_sig_parts.append("*")
        # Keyword-only
        if ko_args:
            args_sig_parts.extend(ko_args)
        # **kwargs
        if kwarg:
            args_sig_parts.append(f"**{kwarg}")

        # Type hints
        if "type_hints" in step:
            hints = step["type_hints"]
            def hintify(a): return f"{a}: {hints[a]}" if a in hints else a
            def varhint(a): return f"*{a}: {hints[a]}" if a in hints else f"*{a}"
            def kwhint(a): return f"**{a}: {hints[a]}" if a in hints else f"**{a}"
            args_sig_parts = [
                hintify(a) if a not in ("*", "/") and not a.startswith("*") and not a.startswith("**")
                else varhint(a[1:]) if a.startswith("*") and not a.startswith("**")
                else kwhint(a[2:]) if a.startswith("**")
                else a
                for a in args_sig_parts
            ]
        args_sig = ", ".join(args_sig_parts)
        ret = f" -> {step['returns']}" if "returns" in step else ""
        lines.append(f"{self._indent(indent)}def {step['name']}({args_sig}){ret}:")
        if "docstring" in step:
            lines.append(self._handle_docstring({"text": step["docstring"]}, indent+1))
        body = step.get("body", [])
        if body:
            lines.append(self.generate_code(body, indent+1))
        else:
            lines.append(self._indent(indent+1) + "pass")
        return lines

    def _handle_func_call(self, step, indent):
        args = ", ".join(str(a) for a in step.get("args", []))
        call = f"{step['name']}({args})"
        target = step.get("target")
        if target:
            return f"{self._indent(indent)}{target} = {call}"
        return f"{self._indent(indent)}{call}"

    def _handle_lambda(self, step, indent):
        args = ", ".join(step.get("args", []))
        expr = step["expr"]
        target = step.get("target")
        lam = f"lambda {args}: {expr}"
        if target:
            return f"{self._indent(indent)}{target} = {lam}"
        return f"{self._indent(indent)}{lam}"

    def _handle_return(self, step, indent):
        value = step.get("value")
        return f"{self._indent(indent)}return {value}" if value is not None else f"{self._indent(indent)}return"

    def _handle_yield(self, step, indent):
        value = step.get("value")
        return f"{self._indent(indent)}yield {value}" if value is not None else f"{self._indent(indent)}yield"

    def _handle_yield_from(self, step, indent):
        # Delegation: yield from <expr>
        expr = step["expr"]
        return f"{self._indent(indent)}yield from {expr}"

    # ---- Classes ----
    def _handle_class_def(self, step, indent):
        bases = f"({', '.join(step.get('bases', []))})" if step.get("bases") else ""
        lines = []
        for deco in step.get("decorators", []):
            lines.append(f"{self._indent(indent)}@{deco}")
        lines.append(f"{self._indent(indent)}class {step['name']}{bases}:")
        if "docstring" in step:
            lines.append(self._handle_docstring({"text": step["docstring"]}, indent+1))
        # Explicit __slots__
        if "__slots__" in step:
            slots = step["__slots__"]
            slot_str = f"{self._indent(indent+1)}__slots__ = {slots}"
            lines.append(slot_str)
        body = step.get("body", [])
        if body:
            lines.append(self.generate_code(body, indent+1))
        else:
            lines.append(self._indent(indent+1) + "pass")
        return lines

    # ---- Decorators ----
    def _handle_decorator(self, step, indent):
        # Not used directly; handled in func_def/class_def
        return ""

    def _handle_decorator_factory(self, step, indent):
        # e.g., @deco(arg1, arg2)
        deco = step["deco"]
        args = ", ".join(str(a) for a in step.get("args", []))
        return f"{self._indent(indent)}@{deco}({args})"

    # ---- Imports & Modules ----
    def _handle_import(self, step, indent):
        alias = f" as {step['as']}" if "as" in step else ""
        return f"{self._indent(indent)}import {step['module']}{alias}"

    def _handle_from_import(self, step, indent):
        names = ", ".join(step["names"])
        alias = f" as {step['as']}" if "as" in step else ""
        return f"{self._indent(indent)}from {step['module']} import {names}{alias}"

    def _handle_importlib_import(self, step, indent):
        # Dynamic import using importlib
        module = step["module"]
        as_var = step.get("as")
        line = f"{self._indent(indent)}import importlib"
        import_line = f"{self._indent(indent)}{as_var or module} = importlib.import_module('{module}')"
        return [line, import_line]

    def _handle_multi_alias_import(self, step, indent):
        # Multiple modules, each with an alias
        # step: {type: multi_alias_import, "modules": [{"name":..., "as":...}, ...]}
        modstrs = [f"{m['name']} as {m['as']}" for m in step["modules"]]
        return f"{self._indent(indent)}import {', '.join(modstrs)}"

    # ---- Data Structures & Comprehensions ----
    def _handle_list_comp(self, step, indent):
        cond = f" if {step['cond']}" if "cond" in step else ""
        comp = f"[{step['expr']} for {step['var']} in {step['iterable']}{cond}]"
        target = step.get("target")
        return f"{self._indent(indent)}{target} = {comp}" if target else f"{self._indent(indent)}{comp}"

    def _handle_dict_comp(self, step, indent):
        cond = f" if {step['cond']}" if "cond" in step else ""
        comp = f"{{{step['key']}: {step['value']} for {step['var']} in {step['iterable']}{cond}}}"
        target = step.get("target")
        return f"{self._indent(indent)}{target} = {comp}" if target else f"{self._indent(indent)}{comp}"

    def _handle_set_comp(self, step, indent):
        cond = f" if {step['cond']}" if "cond" in step else ""
        comp = f"{{{step['expr']} for {step['var']} in {step['iterable']}{cond}}}"
        target = step.get("target")
        return f"{self._indent(indent)}{target} = {comp}" if target else f"{self._indent(indent)}{comp}"

    # ---- Exception Handling ----
    def _handle_try(self, step, indent):
        lines = [f"{self._indent(indent)}try:"]
        lines.append(self.generate_code(step.get("body", []), indent+1) or self._indent(indent+1) + "pass")
        excepts = step.get("except", [])
        if isinstance(excepts, dict):
            excepts = [excepts]
        for exc in excepts:
            exc_type = exc.get("exception", "")
            as_var = f" as {exc['as']}" if "as" in exc else ""
            lines.append(f"{self._indent(indent)}except {exc_type}{as_var}:")
            lines.append(self.generate_code(exc.get("body", []), indent+1) or self._indent(indent+1) + "pass")
        if "else" in step:
            lines.append(f"{self._indent(indent)}else:")
            lines.append(self.generate_code(step["else"], indent+1) or self._indent(indent+1) + "pass")
        if "finally" in step:
            lines.append(f"{self._indent(indent)}finally:")
            lines.append(self.generate_code(step["finally"], indent+1) or self._indent(indent+1) + "pass")
        return lines

    def _handle_raise(self, step, indent):
        return f"{self._indent(indent)}raise {step['exception']}"

    def _handle_raise_from(self, step, indent):
        # Exception chaining: raise ... from ...
        exc = step["exception"]
        cause = step["from"]
        return f"{self._indent(indent)}raise {exc} from {cause}"

    def _handle_assert(self, step, indent):
        msg = f", {step['msg']}" if "msg" in step else ""
        return f"{self._indent(indent)}assert {step['condition']}{msg}"

    # ---- With/context manager ----
    def _handle_with(self, step, indent):
        context = step["context"]
        lines = [f"{self._indent(indent)}with {context}:"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) or self._indent(indent+1) + "pass")
        return lines

    def _handle_multi_with(self, step, indent):
        # Multiple contexts in one with statement
        contexts = step["contexts"]  # List of context strings, e.g. ["open('a') as f", "lock"]
        ctx_str = ", ".join(contexts)
        lines = [f"{self._indent(indent)}with {ctx_str}:"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) or self._indent(indent+1) + "pass")
        return lines

    # ---- Main guard ----
    def _handle_main_guard(self, step, indent):
        lines = [f"{self._indent(indent)}if __name__ == '__main__':"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1))
        return lines

    # ====== ADVANCED HANDLERS ======

    # ---- Async/Await ----
    def _handle_async_func_def(self, step, indent):
        decorators = step.get("decorators", [])
        lines = []
        for deco in decorators:
            lines.append(f"{self._indent(indent)}@{deco}")
        # Same parameter logic as regular def
        args_sig_parts = []
        po_args = step.get("positional_only", [])
        args = step.get("args", [])
        vararg = step.get("vararg")
        ko_args = step.get("keyword_only", [])
        kwarg = step.get("kwarg")
        if po_args:
            args_sig_parts.extend(po_args)
            args_sig_parts.append("/")
        args_sig_parts.extend(args)
        if vararg:
            args_sig_parts.append(f"*{vararg}")
        else:
            if ko_args:
                args_sig_parts.append("*")
        if ko_args:
            args_sig_parts.extend(ko_args)
        if kwarg:
            args_sig_parts.append(f"**{kwarg}")
        if "type_hints" in step:
            hints = step["type_hints"]
            def hintify(a): return f"{a}: {hints[a]}" if a in hints else a
            def varhint(a): return f"*{a}: {hints[a]}" if a in hints else f"*{a}"
            def kwhint(a): return f"**{a}: {hints[a]}" if a in hints else f"**{a}"
            args_sig_parts = [
                hintify(a) if a not in ("*", "/") and not a.startswith("*") and not a.startswith("**")
                else varhint(a[1:]) if a.startswith("*") and not a.startswith("**")
                else kwhint(a[2:]) if a.startswith("**")
                else a
                for a in args_sig_parts
            ]
        args_sig = ", ".join(args_sig_parts)
        ret = f" -> {step['returns']}" if "returns" in step else ""
        lines.append(f"{self._indent(indent)}async def {step['name']}({args_sig}){ret}:")
        if "docstring" in step:
            lines.append(self._handle_docstring({"text": step["docstring"]}, indent+1))
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) if body else self._indent(indent+1) + "pass")
        return lines

    def _handle_await(self, step, indent):
        expr = step["expr"]
        target = step.get("target")
        if target:
            return f"{self._indent(indent)}{target} = await {expr}"
        return f"{self._indent(indent)}await {expr}"

    def _handle_async_for(self, step, indent):
        lines = [f"{self._indent(indent)}async for {step['var']} in {step['iterable']}:"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) if body else self._indent(indent+1) + "pass")
        return lines

    def _handle_async_with(self, step, indent):
        lines = [f"{self._indent(indent)}async with {step['context']}:"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) if body else self._indent(indent+1) + "pass")
        return lines

    # ---- Pattern Matching ----
    def _handle_match(self, step, indent):
        lines = [f"{self._indent(indent)}match {step['subject']}:"]
        for case in step.get("cases", []):
            lines.extend(self._handle_case(case, indent+1))
        return lines

    def _handle_case(self, step, indent):
        # Enhanced: supports pattern, as binding, guard, star etc.
        pattern = step["pattern"]
        # Support for starred patterns in match cases
        if isinstance(pattern, list):
            # e.g. ["a", "*rest", "b"]
            pattern_str = ", ".join(pattern)
        else:
            pattern_str = pattern
        guard = f" if {step['guard']}" if "guard" in step and step["guard"] else ""
        asbind = f" as {step['as']}" if "as" in step else ""
        lines = [f"{self._indent(indent)}case {pattern_str}{asbind}{guard}:"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) if body else self._indent(indent+1) + "pass")
        return lines

    # ---- Global/Nonlocal ----
    def _handle_global(self, step, indent):
        names = ", ".join(step["names"])
        return f"{self._indent(indent)}global {names}"

    def _handle_nonlocal(self, step, indent):
        names = ", ".join(step["names"])
        return f"{self._indent(indent)}nonlocal {names}"

    # ---- Del ----
    def _handle_del(self, step, indent):
        target = step["target"]
        return f"{self._indent(indent)}del {target}"

    # ---- Variable/Type Annotation ----
    def _handle_annotation(self, step, indent):
        target = step["target"]
        annotation = step["annotation"]
        value = step.get("value")
        if value is not None:
            return f"{self._indent(indent)}{target}: {annotation} = {value}"
        else:
            return f"{self._indent(indent)}{target}: {annotation}"

    # ---- Shebang/Encoding ----
    def _handle_shebang(self, step, indent):
        return f"#!{step['line']}"

    def _handle_encoding(self, step, indent):
        return f"# -*- coding: {step['encoding']} -*-"

    # ---- Dunder/Module Vars ----
    def _handle_dunder(self, step, indent):
        name = step["name"]
        value = step["value"]
        return f"{self._indent(indent)}{name} = {value}"

    # ---- Magic Methods ----
    def _handle_magic_method(self, step, indent):
        lines = [f"{self._indent(indent)}def {step['name']}({', '.join(step.get('args', []))}):"]
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) if body else self._indent(indent+1) + "pass")
        return lines

    # ---- Metaclass class ----
    def _handle_metaclass_class_def(self, step, indent):
        bases = f"({', '.join(step.get('bases', []))})" if step.get("bases") else ""
        metaclass = f", metaclass={step['metaclass']}" if "metaclass" in step else ""
        if bases and metaclass:
            bases = bases[:-1] + metaclass + ")"
        elif not bases and metaclass:
            bases = f"(metaclass={step['metaclass']})"
        lines = [f"{self._indent(indent)}class {step['name']}{bases}:"]
        if "docstring" in step:
            lines.append(self._handle_docstring({"text": step["docstring"]}, indent+1))
        body = step.get("body", [])
        lines.append(self.generate_code(body, indent+1) if body else self._indent(indent+1) + "pass")
        return lines

    # ---- Generator Expressions ----
    def _handle_generator_expr(self, step, indent):
        cond = f" if {step['cond']}" if "cond" in step else ""
        expr = f"({step['expr']} for {step['var']} in {step['iterable']}{cond})"
        target = step.get("target")
        return f"{self._indent(indent)}{target} = {expr}" if target else f"{self._indent(indent)}{expr}"

    # ---- Dataclass ----
    def _handle_dataclass(self, step, indent):
        lines = []
        if "args" in step:
            # Parameterized @dataclass
            argstr = ", ".join(f"{k}={v}" for k, v in step["args"].items())
            lines.append(f"{self._indent(indent)}@dataclass({argstr})")
        else:
            lines.append(f"{self._indent(indent)}@dataclass")
        lines.extend(self._handle_class_def(step, indent))
        return lines

    def _handle_parameterized_dataclass(self, step, indent):
        # Explicit handler for parameterized dataclass
        argstr = ", ".join(f"{k}={v}" for k, v in step["args"].items())
        lines = [f"{self._indent(indent)}@dataclass({argstr})"]
        lines.extend(self._handle_class_def(step, indent))
        return lines

    # ====== NEW PYTHON 3.8–3.13 FEATURES ======

    # -- Type Alias (Python 3.12+) --
    def _handle_type_alias(self, step, indent):
        # step: {"type": "type_alias", "name": "Vector", "expr": "list[float]"}
        return f"{self._indent(indent)}type {step['name']} = {step['expr']}"

    # -- Future Import --
    def _handle_future_import(self, step, indent):
        # step: {"type": "future_import", "names": ["annotations", "generator_stop"]}
        names = ", ".join(step["names"])
        return f"{self._indent(indent)}from __future__ import {names}"

    # -- Walrus Operator (:=) --
    def _handle_walrus(self, step, indent):
        # step: {"type": "walrus", "target": "x", "expr": "f()"}
        return f"{self._indent(indent)}({step['target']} := {step['expr']})"

    # -- F-string debugging (f"{x=}") --
    def _handle_fstring_debug(self, step, indent):
        # step: {"type": "fstring_debug", "expr": "x"}
        return f'{self._indent(indent)}f"{{{step["expr"]}=}}"'

    # -- Type Parameters (PEP 695/696 stub for Python 3.12/3.13) --
    def _handle_type_params(self, step, indent):
        # step: {"type": "type_params", "params": ["T", "U"]}
        params = ", ".join(step["params"])
        return f"{self._indent(indent)}[{params}]  # Type parameters (PEP 695/696)"

    # ---- Semantic handler for exec ----
    def _handle_exec(self, step, indent):
        expr = step["expr"]
        globals_ = f", {step['globals']}" if "globals" in step else ""
        locals_ = f", {step['locals']}" if "locals" in step else ""
        return f"{self._indent(indent)}exec({expr}{globals_}{locals_})"

    # ---- Semantic handler for eval ----
    def _handle_eval(self, step, indent):
        expr = step["expr"]
        globals_ = f", {step['globals']}" if "globals" in step else ""
        locals_ = f", {step['locals']}" if "locals" in step else ""
        return f"{self._indent(indent)}eval({expr}{globals_}{locals_})"

    # ---- Specialized support for mypy-style pragmas ----
    def _handle_mypy_pragma(self, step, indent):
        # # type: ignore/TYPE
        pragma = step["pragma"]
        return f"{self._indent(indent)}# type: {pragma}"

    # ---- Chained Comparisons ----
    def _handle_chained_comparison(self, step, indent):
        # e.g., a < b < c > d
        expr = " ".join(step["comparisons"])  # ["a", "<", "b", "<", "c", ">", "d"]
        target = step.get("target")
        result = f"{self._indent(indent)}{expr}"
        if target:
            result = f"{self._indent(indent)}{target} = {expr}"
        return result

    # ---- Conditional Expressions ----
    def _handle_cond_expr(self, step, indent):
        # e.g. x if cond else y
        expr = f"{step['then']} if {step['cond']} else {step['else']}"
        target = step.get("target")
        if target:
            return f"{self._indent(indent)}{target} = {expr}"
        return f"{self._indent(indent)}{expr}"
