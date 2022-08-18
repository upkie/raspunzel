# raspunzel

Command-line tool to run Bazel targets on Raspberry Pi.

## Installation

```console
pip install raspunzel
```

## Usage

Run ``raspunzel`` from a Bazel workspace deployed to your Raspberry Pi:

```
raspunzel run //my/target -- --foo --bar
```
