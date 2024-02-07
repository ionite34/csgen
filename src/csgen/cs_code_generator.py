import os
from abc import ABC
from contextlib import contextmanager
from io import StringIO, TextIOBase
from textwrap import dedent

from csgen._version import __version__
from csgen.cs_access_modifiers import ClassModifier, PropertyModifier


class BaseCSharpCodeGenerator(ABC):
    _stream: TextIOBase

    def __init__(self, io: TextIOBase | None = None, newline: str | None = None, generator_name: str | None = None, spaces_per_indent: int | None = None):
        super().__init__()
        self.generator_name = type(self).__qualname__
        self.spaces_per_indent = 4
        self.indent_level = 0

        self._newline = newline or ("\r\n" if os.name == "nt" else "\n")
        self._stream = io or StringIO()

    @contextmanager
    def indent(self):
        """Increase the current indent level by one for the duration of the context."""
        self.indent_level += 1
        yield
        self.indent_level = max(0, self.indent_level - 1)

    def write(self, code: str):
        """Write a line of code to the output stream. No newline is appended."""
        self._stream.write(code)

    def write_line(self, code: str = ""):
        """Write a line of code to the output stream. Indents to the current indent level. A newline is appended."""
        if self.indent_level > 0:
            self._stream.write(" " * self.spaces_per_indent * self.indent_level)

        self._stream.write(code)
        self._stream.write(self._newline)

    def write_lines(self, lines: str | list[str]):
        """Write multiple lines of code to the output stream. Indents to the current indent level."""
        if isinstance(lines, str):
            lines = dedent(lines).splitlines()

        for line in lines:
            self.write_line(line)

    def write_attribute(self, attribute: str):
        """Write an attribute (Surrounds argument with square brackets)."""
        if attribute.startswith("[") and attribute.endswith("]"):
            raise ValueError("Attribute should not be surrounded by square brackets")

        self.write_line(f"[{attribute}]")

    @contextmanager
    def enter_class(self, class_name: str, modifier: ClassModifier):
        """Enter a class definition block. Yields a context for writing the class body."""
        self.write_line(f"{modifier.to_cs()} class {class_name}")

        with self.enter_brace():
            yield

    def write_class(
            self, class_name: str, modifier: ClassModifier, inherits: str | None = None
    ):
        line = f"{modifier.to_cs()} class {class_name}"

        if inherits is not None:
            line += f" : {inherits}"

        line += ";"

        self.write_line(line)

    @contextmanager
    def enter_record(
        self, class_name: str, modifier: ClassModifier, inherits: str | None = None
    ):
        line = f"{modifier.to_cs()} record {class_name}"

        if inherits is not None:
            line += f" : {inherits}"

        self.write_line(line)

        with self.enter_brace():
            yield

    def write_record(
            self, class_name: str, modifier: ClassModifier, inherits: str | None = None
    ):
        line = f"{modifier.to_cs()} record {class_name}"

        if inherits is not None:
            line += f" : {inherits}"

        line += ";"

        self.write_line(line)

    @contextmanager
    def enter_brace(self):
        self.write_line("{")
        with self.indent():
            yield
        self.write_line("}")

    def write_comment(self, comment: str):
        """Write a single-line comment (e.g. // comment)."""
        self.write_line(f"// {comment}")

    def write_directive(self, directive: str):
        """Write a preprocessor directive (e.g. #nullable enable)."""
        self.write_line(f"#{directive}")

    def write_using(self, import_name: str):
        self.write_line(f"using {import_name};")

    def write_namespace(self, namespace: str):
        self.write_line(f"namespace {namespace};")

    def write_auto_property(
        self,
        property_name: str,
        type_name: str,
        modifier: PropertyModifier,
        get_stmt: str = "get",
        set_stmt: str = "set",
    ):
        line = f"{modifier.to_cs()} {type_name} {property_name} {{ {get_stmt}; {set_stmt}; }}"
        self.write_line(line)


class CSharpCodeGenerator(BaseCSharpCodeGenerator):
    def __init__(self, io: TextIOBase | None = None, newline: str | None = None):
        super().__init__(io, newline)

        self.default_class_attributes = [
            f'global::System.CodeDom.Compiler.GeneratedCode("{self.generator_name}", "{__version__}")',
            "global::System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage"
        ]

        self.write_default_header()

    def write_default_header(self):
        self.write_comment("<auto-generated/>")
        self.write_directive("pragma warning disable")
        self.write_directive("nullable enable")