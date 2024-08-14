# raspunzel

Command-line tool to run Bazel targets on systems where Bazel is not installed. For instance, we can run cross-compiled Bazel targets on a Raspberry Pi:

```console
pi@raspi:~/my_bazel_dir$ raspunzel run //my/target -- --foo --bar
```

Raspunzel's syntax is the same as Bazel, but it only supports the ``run`` command.

## Installation

### From PyPI

[![PyPI version](https://img.shields.io/pypi/v/raspunzel)](https://pypi.org/project/raspunzel/)

```console
$ pip install raspunzel
```

### Standalone script

Raspunzel is easy to ship in your own project as a [standalone script](https://github.com/tasts-robots/raspunzel/tree/main/standalone). Check out how it is done for instance in the [software of Upkie wheeled-biped robots](https://github.com/upkie/upkie).
