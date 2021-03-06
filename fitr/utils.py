# -*- coding: utf-8 -*-
import numpy as np

def I(x):
    """ Identity transformation.

    Mainly for convenience when using `fitr.utils.transform` with some vector element that should not be transformed, despite changing the coordinates of other variables.

    Arguments:

        x: `ndarray`

    Returns:

        `ndarray(shape=x.shape)`

    """
    return x

def logsumexp(x):
    """ Numerically stable logsumexp.

    Computed as follows:

    $$
    \max x + \log \sum_x e^{x - \max x}
    $$

    Arguments:

        x: `ndarray(shape=(nactions,))``

    Returns:

        `float`
    """
    xmax = np.max(x)
    y = xmax + np.log(np.sum(np.exp(x-xmax)))
    return y

def relu(x, a_max=None):
    """ Rectified linearity

    $$
    \mathbf x' = \max (x_i, 0)_{i=1}^{|\mathbf x|}
    $$

    Arguments:

        x: Vector of inputs
        a_max: Upper bound at which to clip values of `x`

    Returns:

        Exponentiated values of `x`.

    """
    if a_max is None: a_max=np.inf
    x = x.clip(max=a_max)
    return np.greater(x, 0)*x

def scale_data(X, axis=0, with_mean=True, with_var=True):
    """ Rescales data by subtracting mean and dividing by variance

    $$
    \mathbf x' = \\frac{\mathbf x - \\frac{1}{n} \mathbf 1^\\top \mathbf x}{Var(\mathbf x)}
    $$

    Arguments:

        X: `ndarray((nsamples, [nfeatures]))`. Data. May be 1D or 2D.
        with_mean: `bool`. Whether to subtract the mean
        with_var: `bool`. Whether to divide by variance

    Returns:

        `ndarray(X.shape)`. Rescaled data.
    """
    if X.ndim == 1: X = X.reshape(-1, 1)
    if with_mean: X -= np.tile(np.mean(X, axis).reshape(1, -1), [X.shape[0], 1])
    if with_var: X /= np.tile(np.var(X, axis).reshape(1, -1), [X.shape[0], 1])
    return X

def sigmoid(x, a_min=-10, a_max=10):
    """ Sigmoid function

    $$
    \sigma(x) = \\frac{1}{1 + e^{-x}}
    $$

    Arguments:

        x: Vector
        a_min: Lower bound at which to clip values of `x`
        a_max: Upper bound at which to clip values of `x`

    Returns:

        Vector between 0 and 1 of size `x.shape`
    """
    expnx = np.exp(-np.clip(x, a_min=a_min, a_max=a_max))
    return 1/(1+expnx)

def softmax(x):
    """ Computes the softmax function

    $$
    p(\mathbf{x}) = \\frac{e^{\mathbf{x} - \max_i x_i}}{\mathbf{1}^\\top e^{\mathbf{x} - \max_i x_i}}
    $$

    Arguments:

        x: Softmax logits (`ndarray((N,))`)

    Returns:

        Vector of probabilities of size `ndarray((N,))`
    """
    xmax = np.max(x)
    expx = np.exp(x-xmax)
    return expx/np.sum(expx)

def stable_exp(x, a_min=-10, a_max=10):
    """ Clipped exponential function

    Avoids overflow by clipping input values.

    Arguments:

        x: Vector of inputs
        a_min: Lower bound at which to clip values of `x`
        a_max: Upper bound at which to clip values of `x`

    Returns:

        Exponentiated values of `x`.
    """
    return np.exp(np.clip(x, a_min=a_min, a_max=a_max))

def tanh(x, a_min=-10, a_max=10):
    """ Hyperbolic tangent function

    $$
    \tanh(x) = \\frac{e^x-e^{-x}}{e^x + e^{-x}}
    $$

    Arguments:

        x: Vector
        a_min: Lower bound at which to clip values of `x`
        a_max: Upper bound at which to clip values of `x`

    Returns:

        Vector between -1 and 1 of size `x.shape`
    """
    tanhvals = np.clip(x, a_min=a_min, a_max=a_max)
    return np.tanh(tanhvals)

def transform(x, f_list):
    """ Transforms parameters from domain in `x` into some new domain defined by `f_list`

    Arguments:

        x: `ndarray((nparams,))`. Parameter vector in some domain.
        f_list: `list` where `len(list) == nparams`. Functions defining coordinate transformations on each element of `x`.

    Returns:

        x_: `ndarray((nparams,))`. Parameter vector in new coordinates.

    Examples:

    Applying `fitr` transforms can be done as follows.

    ``` python
    import numpy as np
    from fitr.utils import transform, sigmoid, relu

    x = np.random.normal(0, 5, size=3)
    x_= transform(x, [sigmoid, relu, relu])
    ```

    You can also apply other functions, so long as dimensions are equal for input and output.

    ``` python
    import numpy as np
    from fitr.utils import transform

    x  = np.random.normal(0, 10, size=3)
    x_ = transform(x, [np.square, np.sqrt, np.exp])
    ```
    """
    if x.ndim == 1:
        x = np.stack(np.array([x_i]) for i, x_i in enumerate(x))
    x_ = np.stack(f_list[i](x_i) for i, x_i in enumerate(x))
    return x_
