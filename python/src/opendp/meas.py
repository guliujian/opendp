# Auto-generated. Do not edit.
from opendp._convert import *
from opendp._lib import *
from opendp.mod import *
from opendp.typing import *

__all__ = [
    "make_base_laplace",
    "make_base_gaussian",
    "make_base_analytic_gaussian",
    "make_base_geometric",
    "make_randomized_response_bool",
    "make_randomized_response",
    "make_base_ptr"
]


def make_base_laplace(
    scale,
    D: RuntimeTypeDescriptor = "AllDomain<T>"
) -> Measurement:
    """Make a Measurement that adds noise from the laplace(`scale`) distribution to a scalar value.
    Adjust D to noise vector-valued data.
    
    :param scale: Noise scale parameter for the laplace distribution. `scale` == sqrt(2) * standard_deviation.
    :param D: Domain of the data type to be privatized. Valid values are VectorDomain<AllDomain<T>> or AllDomain<T>
    :type D: :ref:`RuntimeTypeDescriptor`
    :return: A base_laplace step.
    :rtype: Measurement
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("floating-point", "contrib")
    
    # Standardize type arguments.
    D = RuntimeType.parse(type_name=D, generics=["T"])
    T = get_domain_atom_or_infer(D, scale)
    D = D.substitute(T=T)
    
    # Convert arguments to c types.
    scale = py_to_c(scale, c_type=ctypes.c_void_p, type_name=T)
    D = py_to_c(D, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_base_laplace
    function.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(scale, D), Measurement))


def make_base_gaussian(
    scale,
    D: RuntimeTypeDescriptor = "AllDomain<T>",
    MO: RuntimeTypeDescriptor = "SmoothedMaxDivergence<T>"
) -> Measurement:
    """Make a Measurement that adds noise from the gaussian(`scale`) distribution to the input.
    Adjust D to noise vector-valued data.
    The output epsilon may be no greater than one.
    Use make_base_analytic_gaussian for a tighter analysis that supports epsilon > 1.
    
    :param scale: noise scale parameter for the gaussian distribution. `scale` == standard_deviation.
    :param D: Domain of the data type to be privatized. Valid values are VectorDomain<AllDomain<T>> or AllDomain<T>
    :type D: :ref:`RuntimeTypeDescriptor`
    :param MO: Output measure. Valid values are SmoothedMaxDivergence<T> or ZeroConcentratedDivergence<T>
    :type MO: :ref:`RuntimeTypeDescriptor`
    :return: A base_gaussian step.
    :rtype: Measurement
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("floating-point", "contrib")
    
    # Standardize type arguments.
    D = RuntimeType.parse(type_name=D, generics=["T"])
    MO = RuntimeType.parse(type_name=MO, generics=["T"])
    T = get_domain_atom_or_infer(D, scale)
    D = D.substitute(T=T)
    MO = MO.substitute(T=T)
    
    # Convert arguments to c types.
    scale = py_to_c(scale, c_type=ctypes.c_void_p, type_name=T)
    D = py_to_c(D, c_type=ctypes.c_char_p)
    MO = py_to_c(MO, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_base_gaussian
    function.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(scale, D, MO), Measurement))


def make_base_analytic_gaussian(
    scale: float,
    D: RuntimeTypeDescriptor = "AllDomain<f64>"
) -> Measurement:
    """Make a Measurement that adds noise from the gaussian(`scale`) distribution to the input.
    Adjust D to noise vector-valued data.
    The privacy relation is based on the analytic gaussian mechanism.
    
    :param scale: noise scale parameter for the gaussian distribution. `scale` == standard_deviation.
    :type scale: float
    :param D: Domain of the data type to be privatized. Valid values are VectorDomain<AllDomain<f64>> or AllDomain<f64>
    :type D: :ref:`RuntimeTypeDescriptor`
    :return: A base_analytic_gaussian step.
    :rtype: Measurement
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("floating-point", "contrib")
    
    # Standardize type arguments.
    D = RuntimeType.parse(type_name=D)
    T = get_domain_atom_or_infer(D, scale)
    
    # Convert arguments to c types.
    scale = py_to_c(scale, c_type=ctypes.c_double)
    D = py_to_c(D, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_base_analytic_gaussian
    function.argtypes = [ctypes.c_double, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(scale, D), Measurement))


def make_base_geometric(
    scale,
    bounds: Any = None,
    D: RuntimeTypeDescriptor = "AllDomain<i64>",
    QO: RuntimeTypeDescriptor = None
) -> Measurement:
    """Make a Measurement that adds noise from the geometric(`scale`) distribution to the input.
    Adjust D to noise vector-valued data.
    
    :param scale: noise scale parameter for the geometric distribution. `scale` == sqrt(2) * standard_deviation.
    :param bounds: Set bounds on the count to make the algorithm run in constant-time.
    :type bounds: Any
    :param D: Domain of the data type to be privatized. Valid values are VectorDomain<AllDomain<T>> or AllDomain<T>
    :type D: :ref:`RuntimeTypeDescriptor`
    :param QO: Data type of the sensitivity, scale, and budget.
    :type QO: :ref:`RuntimeTypeDescriptor`
    :return: A base_geometric step.
    :rtype: Measurement
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # Standardize type arguments.
    D = RuntimeType.parse(type_name=D)
    QO = RuntimeType.parse_or_infer(type_name=QO, public_example=scale)
    T = get_domain_atom(D)
    OptionT = RuntimeType(origin='Option', args=[RuntimeType(origin='Tuple', args=[T, T])])
    
    # Convert arguments to c types.
    scale = py_to_c(scale, c_type=ctypes.c_void_p, type_name=QO)
    bounds = py_to_c(bounds, c_type=AnyObjectPtr, type_name=OptionT)
    D = py_to_c(D, c_type=ctypes.c_char_p)
    QO = py_to_c(QO, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_base_geometric
    function.argtypes = [ctypes.c_void_p, AnyObjectPtr, ctypes.c_char_p, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(scale, bounds, D, QO), Measurement))


def make_randomized_response_bool(
    prob,
    constant_time: bool = False,
    Q: RuntimeTypeDescriptor = None
) -> Measurement:
    """Make a Measurement that implements randomized response on a boolean value.
    
    :param prob: Probability of returning the correct answer. Must be in [0.5, 1)
    :param constant_time: Set to true to enable constant time
    :type constant_time: bool
    :param Q: Data type of probability and budget.
    :type Q: :ref:`RuntimeTypeDescriptor`
    :return: A randomized_response_bool step.
    :rtype: Measurement
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # Standardize type arguments.
    Q = RuntimeType.parse_or_infer(type_name=Q, public_example=prob)
    
    # Convert arguments to c types.
    prob = py_to_c(prob, c_type=ctypes.c_void_p, type_name=Q)
    constant_time = py_to_c(constant_time, c_type=ctypes.c_bool)
    Q = py_to_c(Q, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_randomized_response_bool
    function.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(prob, constant_time, Q), Measurement))


def make_randomized_response(
    categories: Any,
    prob,
    constant_time: bool = False,
    T: RuntimeTypeDescriptor = None,
    Q: RuntimeTypeDescriptor = None
) -> Measurement:
    """Make a Measurement that implements randomized response on a categorical value.
    
    :param categories: Set of valid outcomes
    :type categories: Any
    :param prob: Probability of returning the correct answer. Must be in [1/num_categories, 1)
    :param constant_time: Set to true to enable constant time
    :type constant_time: bool
    :param T: Data type of a category.
    :type T: :ref:`RuntimeTypeDescriptor`
    :param Q: Data type of probability and budget.
    :type Q: :ref:`RuntimeTypeDescriptor`
    :return: A randomized_response step.
    :rtype: Measurement
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # Standardize type arguments.
    T = RuntimeType.parse_or_infer(type_name=T, public_example=get_first(categories))
    Q = RuntimeType.parse_or_infer(type_name=Q, public_example=prob)
    
    # Convert arguments to c types.
    categories = py_to_c(categories, c_type=AnyObjectPtr, type_name=RuntimeType(origin='Vec', args=[T]))
    prob = py_to_c(prob, c_type=ctypes.c_void_p, type_name=Q)
    constant_time = py_to_c(constant_time, c_type=ctypes.c_bool)
    T = py_to_c(T, c_type=ctypes.c_char_p)
    Q = py_to_c(Q, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_randomized_response
    function.argtypes = [AnyObjectPtr, ctypes.c_void_p, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(categories, prob, constant_time, T, Q), Measurement))


def make_base_ptr(
    scale,
    threshold,
    TK: RuntimeTypeDescriptor,
    TV: RuntimeTypeDescriptor = None
) -> Measurement:
    """Make a Measurement that uses propose-test-release to privatize a hashmap of counts.
    
    :param scale: Noise scale parameter for the laplace distribution. `scale` == sqrt(2) * standard_deviation.
    :param threshold: Exclude counts that are less than this minimum value.
    :param TK: Type of Key. Must be hashable/categorical.
    :type TK: :ref:`RuntimeTypeDescriptor`
    :param TV: Type of Value. Must be float.
    :type TV: :ref:`RuntimeTypeDescriptor`
    :return: A base_ptr step.
    :rtype: Measurement
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("floating-point", "contrib")
    
    # Standardize type arguments.
    TK = RuntimeType.parse(type_name=TK)
    TV = RuntimeType.parse_or_infer(type_name=TV, public_example=scale)
    
    # Convert arguments to c types.
    scale = py_to_c(scale, c_type=ctypes.c_void_p, type_name=TV)
    threshold = py_to_c(threshold, c_type=ctypes.c_void_p, type_name=TV)
    TK = py_to_c(TK, c_type=ctypes.c_char_p)
    TV = py_to_c(TV, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_base_ptr
    function.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(scale, threshold, TK, TV), Measurement))
