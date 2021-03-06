# `fitr.inference`

Methods for inferring the parameters of generative models for reinforcement learning data.



## OptimizationResult

```python
fitr.inference.optimization_result.OptimizationResult()
```

Container for the results of an optimization run on a generative model of behavioural data

Arguments:

- **subject_id**: `ndarray((nsubjects,))` or `None` (default). Integer ids for subjects
- **xmin**: `ndarray((nsubjects,nparams))` or `None` (default). Parameters that minimize objective function
- **fmin**: `ndarray((nsubjects,))` or `None` (default). Value of objective function at minimum
- **fevals**: `ndarray((nsubjects,))` or `None` (default). Number of function evaluations required to minimize objective function
- **niters**: `ndarray((nsubjects,))` or `None` (default). Number of iterations required to minimize objective function
- **lme**: `ndarray((nsubjects,))` or `None` (default). Log model evidence
- **bic**: `ndarray((nsubjects,))` or `None` (default). Bayesian Information Criterion
- **hess_inv**: `ndarray((nsubjects,nparams,nparams))` or `None` (default). Inverse Hessian at the optimum.
- **err**: `ndarray((nsubjects,nparams))` or `None` (default). Error of estimates at optimum.

---




### OptimizationResult.transform_xmin

```python
fitr.inference.optimization_result.transform_xmin(self, transforms, inplace=False)
```

Rescales the parameter estimates.

Arguments:

- **transforms**: `list`. Transformation functions where `len(transforms) == self.xmin.shape[1]`
- **inplace**: `bool`. Whether to change the values in `self.xmin`. Default is `False`, which returns an `ndarray((nsubjects, nparams))` of the transformed parameters.

Returns:

`ndarray((nsubjects, nparams))` of the transformed parameters if `inplace=False`

---



## mlepar

```python
fitr.inference.mle_parallel.mlepar(f, data, nparams, minstarts=2, maxstarts=10, init_sd=2, njobs=-1)
```

Computes maximum likelihood estimates using parallel CPU resources.

Wraps over the `fitr.optimization.mle_parallel.mle` function.

Arguments:

- **f**: Likelihood function
- **data**: A subscriptable object whose first dimension indexes subjects
- **optimizer**: Optimization function (currently only `l_bfgs_b` supported)
- **nparams**: `int` number of parameters to be estimated
- **minstarts**: `int`. Minimum number of restarts with new initial values
- **maxstarts**: `int`. Maximum number of restarts with new initial values
- **init_sd**: Standard deviation for Gaussian initial values

Returns:

`fitr.inference.OptimizationResult`

---



## l_bfgs_b

```python
fitr.inference.mle_parallel.l_bfgs_b(f, i, data, nparams, minstarts=2, maxstarts=10, init_sd=2)
```

Minimizes the negative log-probability of data with respect to some parameters under function `f` using the L-BFGS-B algorithm.

This function is specified for use with parallel CPU resources.

Arguments:

- **f**: Log likelihood function
- **i**: `int`. Subject being optimized (slices first dimension of `data`)
- **data**: Object subscriptable along first dimension to indicate subject being optimized
- **nparams**: `int`. Number of parameters in the model
- **minstarts**: `int`. Minimum number of restarts with new initial values
- **maxstarts**: `int`. Maximum number of restarts with new initial values
- **init_sd**: Standard deviation for Gaussian initial values

Returns:

- **i**: `int`. Subject being optimized (slices first dimension of `data`)
- **xmin**: `ndarray((nparams,))`. Parameter values at optimum
- **fmin**: Scalar objective function value at optimum
- **fevals**: `int`. Number of function evaluations
- **niters**: `int`. Number of iterations
- **lme_**: Scalar log-model evidence at optimum
- **bic_**: Scalar Bayesian Information Criterion at optimum
- **hess_inv**: `ndarray((nparams, nparams))`. Inv at optimum

---


