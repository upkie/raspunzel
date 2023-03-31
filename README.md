# raspunzel

Command-line tool to deploy and run cross-compiled Bazel targets on a Raspberry Pi.

## Installation

```console
pip install raspunzel
```

## Usage

Raspunzel's syntax is the same as Bazel. First, build your cross-compiled targets locally by:

```console
raspunzel build //my/target
```

Then, sync the repository to the Raspberry Pi host:

```console
raspunzel sync my_raspi:remote/directory
```

Finally, go to the remote directory on the Raspberry Pi and run the target by:

```console
raspunzel run //my/target -- --foo --bar
```

### Advanced

Raspunzel assumes you have a 64-bit Raspberry Pi cross-compilation stack configured in ``.bazelrc`` and named ``"pi64"`` (this is for instance the case in [``upkie_locomotion``](https://github.com/tasts-robots/upkie_locomotion)); ``raspunzel build`` is then a simple alias for ``bazel build --config=pi64``. If your cross-compilation configuration has a different name, you can use Bazel directly:

```console
bazel build --config=my_cross_compilation_stack //my/target
```
