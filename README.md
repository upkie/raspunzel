# raspunzel

Command-line tool to deploy and run cross-compiled Bazel targets on a Raspberry Pi.

## Installation

```console
pip install raspunzel
```

## Usage

The basic usage for ``raspunzel`` goes in three steps. First, build all cross-compiled targets locally:

```console
bazel build --config=my_cross_compilation_stack //my/target
```

Then, sync the repository to the Raspberry Pi host:

```console
raspunzel sync my_raspi:some/path
```

Finally, go to ``some/path`` on the Raspberry Pi and run your target using the regular Bazel syntax:

```console
raspunzel run //my/target -- --foo --bar
```

## Tips

* If you have a 64-bit Raspberry Pi cross-compilation stack configured in ``.bazelrc``, name it ``"pi64"`` and use ``raspunzel build``, which is shorthand for ``bazel build --config=pi64``.
