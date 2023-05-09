# raspunzel

Command-line tool to run Bazel targets on systems where Bazel is not installed. For instance, we can run cross-compiled Bazel targets on a Raspberry Pi:

```console
pi@raspi:~/my_bazel_dir$ raspunzel run //my/target -- --foo --bar
```

Raspunzel's syntax is the same as Bazel, but it only supports the ``run`` command.

## Installation

### PyPI

```console
$ pip install raspunzel
```

### Standalone script

Raspunzel is easy to ship in your own project as a [standalone script](https://github.com/tasts-robots/raspunzel/tree/main/standalone). Check out how it is done for instance in [upkie\_locomotion](https://github.com/tasts-robots/upkie_locomotion).
