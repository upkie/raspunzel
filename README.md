# raspunzel

Command-line tool to deploy and run cross-compiled Bazel targets on a Raspberry Pi.

## Installation

```console
pip install raspunzel
```

## Usage

The basic usage for ``raspunzel`` is to build all cross-compiled targets locally, then sync the repository by:

```console
raspunzel sync my_robot_host:some/path
```

Go to ``some/path`` on the robot host and run your target with the regular Bazel syntax:

```console
raspunzel run //my/target -- --foo --bar
```

## Tips

* If your cross-compilation stack is configured in ``.bazelrc``, name it ``"pi64"`` and use ``raspunzel build``, which is an alias for ``bazel build --config=pi64``.
