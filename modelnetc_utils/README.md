# Utils for Loading and Evaluating ModelNet-C

## Install
```shell
pip install -e .
```
## Usage

- `eval_corrupt_wrapper`

    The wrapper helps to repeat the original testing function on all corrupted test sets. It also helps to compute metrics.

- `ModelNetC`

    ModelNet40-AC loader. The default path is set to `../../data/modelnet_c`. Please change the path in accordingly.