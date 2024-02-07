# csgen

<!-- start badges -->

[pypi]: https://pypi.org/project/csgen/

[![Build](https://github.com/ionite34/csgen/actions/workflows/build.yml/badge.svg)](https://github.com/ionite34/csgen/actions/workflows/build.yml)

[![PyPI](https://img.shields.io/pypi/v/csgen)][pypi]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/csgen)][pypi]

<!-- end badges -->

> Framework for writing generated C# code


## Example

- Usually you can inherit the `csgen.CSharpCodeGenerator` class to add your own helper methods for more specific code generation

```python
from csgen import CSharpCodeGenerator, ClassModifier, PropertyModifier

with open("Sample.g.cs", "w") as f:
    gen = CSharpCodeGenerator(f)
    
    gen.write_namespace("MyNamespace")
    
    with gen.enter_class("Foo", ClassModifier.PUBLIC | ClassModifier.PARTIAL):
        gen.write_comment("A comment")
        gen.write_auto_property("Id", "int", PropertyModifier.PUBLIC | PropertyModifier.REQUIRED)
        gen.write_auto_property("Name", "string", PropertyModifier.PROTECTED)
```

Output File:

```csharp
// <auto-generated/>
#pragma warning disable
#nullable enable

namespace MyNamespace;

[global::System.CodeDom.Compiler.GeneratedCode("csgen", "1.0.0")]
[global::System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public partial class MyClass
{
    public required int Id { get; set; }
    protected string Name { get; set; }
}
```
