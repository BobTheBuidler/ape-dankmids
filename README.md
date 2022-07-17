# Ape Dank Mids Plugin

[Dank Middleware](https://github.com/BobTheBuidler/dank_mids) plugin for Ethereum-based networks

Dank Middleware is an async web3py middleware that collects async calls and batches them into multicalls in the background.

## Dependencies

* [python3](https://www.python.org/downloads) version 3.7 or greater, python3-dev

## Installation

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-dankmids
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/BobTheBuidler/ape-dankmids.git
cd ape-dankmids
python3 setup.py install
```

## Quick Usage

Use in most commands using the `--network` option:

```bash
ape console --network ethereum:goerli:dankmids
```

## Development

Please see the [contributing guide](CONTRIBUTING.md) to learn more how to contribute to this project.
Comments, questions, criticisms and pull requests are welcomed.

## License

This project is licensed under the [Apache 2.0](LICENSE).