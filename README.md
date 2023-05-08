# raspunzel

Command-line tool to run cross-compiled Bazel targets on a Raspberry Pi.

```console
pi@raspi:~/my_bazel_dir$ raspunzel run //my/target -- --foo --bar
```

Raspunzel's syntax is the same as Bazel, but it runs even on systems where Bazel cannot be installed.

## Installation

```console
pip install raspunzel
```
