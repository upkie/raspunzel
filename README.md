# raspunzel

Command-line tool to deploy and run cross-compiled Bazel targets on a Raspberry Pi.

## Installation

```console
pip install raspunzel
```

## Usage

Run ``raspunzel`` from a Bazel workspace deployed to your Raspberry Pi:

```
raspunzel run //my/target -- --foo --bar
```
