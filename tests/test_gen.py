from io import StringIO
from textwrap import dedent

from csgen import CSharpCodeGenerator
from csgen.cs_access_modifiers import ClassModifier, PropertyModifier


def test_1():
    io = StringIO()
    gen = CSharpCodeGenerator(io)

    gen.write_namespace("MyNamespace")
    gen.write_line()

    with gen.enter_class("MyClass", ClassModifier.PUBLIC | ClassModifier.PARTIAL):
        gen.write_auto_property("MyProperty", "int", PropertyModifier.PROTECTED)

    result = io.getvalue()
    expected = dedent("""
    namespace MyNamespace;
    
    public partial class MyClass
    {
        protected int MyProperty { get; set; }
    }
    """).lstrip()

    assert result == expected
