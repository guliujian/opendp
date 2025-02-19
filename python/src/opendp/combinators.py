# Auto-generated. Do not edit.
from opendp._convert import *
from opendp._lib import *
from opendp.mod import *
from opendp.typing import *
from opendp.core import *

__all__ = [
    "make_basic_composition",
    "make_chain_mt",
    "make_chain_tm",
    "make_chain_tt",
    "make_default_user_measurement",
    "make_default_user_postprocessor",
    "make_default_user_transformation",
    "make_fix_delta",
    "make_population_amplification",
    "make_pureDP_to_fixed_approxDP",
    "make_pureDP_to_zCDP",
    "make_zCDP_to_approxDP"
]


def make_basic_composition(
    measurements: Any
) -> Measurement:
    """Construct the DP composition [`measurement0`, `measurement1`, ...]. 
    Returns a Measurement that when invoked, computes `[measurement0(x), measurement1(x), ...]`
    
    All metrics and domains must be equivalent, except for the output domain.
    
    [make_basic_composition in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_basic_composition.html)
    
    :param measurements: A vector of Measurements to compose.
    :type measurements: Any
    :rtype: Measurement
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_measurements = py_to_c(measurements, c_type=AnyObjectPtr, type_name=RuntimeType(origin='Vec', args=[AnyMeasurementPtr]))
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_basic_composition
    lib_function.argtypes = [AnyObjectPtr]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_measurements), Measurement))
    output._depends_on(get_dependencies_iterable(measurements))
    return output


def make_chain_mt(
    measurement1: Measurement,
    transformation0: Transformation
) -> Measurement:
    """Construct the functional composition (`measurement1` ○ `transformation0`).
    Returns a Measurement that when invoked, computes `measurement1(transformation0(x))`.
    
    [make_chain_mt in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_chain_mt.html)
    
    :param measurement1: outer mechanism
    :type measurement1: Measurement
    :param transformation0: inner transformation
    :type transformation0: Transformation
    :rtype: Measurement
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_measurement1 = py_to_c(measurement1, c_type=Measurement, type_name=None)
    c_transformation0 = py_to_c(transformation0, c_type=Transformation, type_name=None)
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_chain_mt
    lib_function.argtypes = [Measurement, Transformation]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_measurement1, c_transformation0), Measurement))
    output._depends_on(get_dependencies(measurement1), get_dependencies(transformation0))
    return output


def make_chain_tm(
    transformation1: Transformation,
    measurement0: Measurement
) -> Measurement:
    """Construct the functional composition (`transformation1` ○ `measurement0`).
    Returns a Measurement that when invoked, computes `transformation1(measurement0(x))`.
    Used to represent non-interactive postprocessing.
    
    [make_chain_tm in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_chain_tm.html)
    
    :param transformation1: outer postprocessing transformation
    :type transformation1: Transformation
    :param measurement0: inner measurement/mechanism
    :type measurement0: Measurement
    :rtype: Measurement
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_transformation1 = py_to_c(transformation1, c_type=Transformation, type_name=None)
    c_measurement0 = py_to_c(measurement0, c_type=Measurement, type_name=None)
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_chain_tm
    lib_function.argtypes = [Transformation, Measurement]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_transformation1, c_measurement0), Measurement))
    output._depends_on(get_dependencies(transformation1), get_dependencies(measurement0))
    return output


def make_chain_tt(
    transformation1: Transformation,
    transformation0: Transformation
) -> Transformation:
    """Construct the functional composition (`transformation1` ○ `transformation0`).
    Returns a Transformation that when invoked, computes `transformation1(transformation0(x))`.
    
    [make_chain_tt in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_chain_tt.html)
    
    :param transformation1: outer transformation
    :type transformation1: Transformation
    :param transformation0: inner transformation
    :type transformation0: Transformation
    :rtype: Transformation
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_transformation1 = py_to_c(transformation1, c_type=Transformation, type_name=None)
    c_transformation0 = py_to_c(transformation0, c_type=Transformation, type_name=None)
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_chain_tt
    lib_function.argtypes = [Transformation, Transformation]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_transformation1, c_transformation0), Transformation))
    output._depends_on(get_dependencies(transformation1), get_dependencies(transformation0))
    return output


def make_default_user_measurement(
    function,
    privacy_map,
    DI: RuntimeTypeDescriptor,
    DO: RuntimeTypeDescriptor,
    MI: RuntimeTypeDescriptor,
    MO: RuntimeTypeDescriptor
) -> Measurement:
    """Construct a Measurement from user-defined callbacks.
    
    **Supported Domains:**
    
    * `VectorDomain<AllDomain<_>>`
    * `AllDomain<_>`
    
    **Supported Metrics:**
    
    * `SymmetricDistance`
    * `InsertDeleteDistance`
    * `ChangeOneDistance`
    * `HammingDistance`
    * `DiscreteDistance`
    * `AbsoluteDistance<_>`
    * `L1Distance<_>`
    * `L2Distance<_>`
    
    **Supported Measures:**
    
    * `MaxDivergence<_>`
    * `FixedSmoothedMaxDivergence<_>`
    * `ZeroConcentratedDivergence<_>`
    
    [make_default_user_measurement in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_default_user_measurement.html)
    
    :param function: A function mapping data from `DI` to `DO`.
    :param privacy_map: A function mapping distances from `MI` to `MO`.
    :param DI: Input Domain. See Supported Domains
    :type DI: :py:ref:`RuntimeTypeDescriptor`
    :param DO: Output Domain. See Supported Domains
    :type DO: :py:ref:`RuntimeTypeDescriptor`
    :param MI: Input Metric. See Supported Metrics
    :type MI: :py:ref:`RuntimeTypeDescriptor`
    :param MO: Output Measure. See Supported Measures
    :type MO: :py:ref:`RuntimeTypeDescriptor`
    :rtype: Measurement
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib", "honest-but-curious")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_function = py_to_c(function, c_type=CallbackFn, type_name=domain_carrier_type(DO))
    c_privacy_map = py_to_c(privacy_map, c_type=CallbackFn, type_name=measure_distance_type(MO))
    c_DI = py_to_c(DI, c_type=ctypes.c_char_p, type_name=None)
    c_DO = py_to_c(DO, c_type=ctypes.c_char_p, type_name=None)
    c_MI = py_to_c(MI, c_type=ctypes.c_char_p, type_name=None)
    c_MO = py_to_c(MO, c_type=ctypes.c_char_p, type_name=None)
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_default_user_measurement
    lib_function.argtypes = [CallbackFn, CallbackFn, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_function, c_privacy_map, c_DI, c_DO, c_MI, c_MO), Measurement))
    output._depends_on(c_function, c_privacy_map)
    return output


def make_default_user_postprocessor(
    function,
    DI: RuntimeTypeDescriptor,
    DO: RuntimeTypeDescriptor
) -> Transformation:
    """Construct a Postprocessor from user-defined callbacks.
    
    **Supported Domains:**
    
    * `VectorDomain<AllDomain<_>>`
    * `AllDomain<_>`
    
    [make_default_user_postprocessor in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_default_user_postprocessor.html)
    
    :param function: A function mapping data from `DI` to `DO`.
    :param DI: Input Domain. See Supported Domains
    :type DI: :py:ref:`RuntimeTypeDescriptor`
    :param DO: Output Domain. See Supported Domains
    :type DO: :py:ref:`RuntimeTypeDescriptor`
    :rtype: Transformation
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_function = py_to_c(function, c_type=CallbackFn, type_name=domain_carrier_type(DO))
    c_DI = py_to_c(DI, c_type=ctypes.c_char_p, type_name=None)
    c_DO = py_to_c(DO, c_type=ctypes.c_char_p, type_name=None)
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_default_user_postprocessor
    lib_function.argtypes = [CallbackFn, ctypes.c_char_p, ctypes.c_char_p]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_function, c_DI, c_DO), Transformation))
    output._depends_on(c_function)
    return output


def make_default_user_transformation(
    function,
    stability_map,
    DI: RuntimeTypeDescriptor,
    DO: RuntimeTypeDescriptor,
    MI: RuntimeTypeDescriptor,
    MO: RuntimeTypeDescriptor
) -> Transformation:
    """Construct a Transformation from user-defined callbacks.
    
    **Supported Domains:**
    
    * `VectorDomain<AllDomain<_>>`
    * `AllDomain<_>`
    
    **Supported Metrics:**
    
    * `SymmetricDistance`
    * `InsertDeleteDistance`
    * `ChangeOneDistance`
    * `HammingDistance`
    * `DiscreteDistance`
    * `AbsoluteDistance<_>`
    * `L1Distance<_>`
    * `L2Distance<_>`
    
    [make_default_user_transformation in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_default_user_transformation.html)
    
    :param function: A function mapping data from `DI` to `DO`.
    :param stability_map: A function mapping distances from `MI` to `MO`.
    :param DI: Input Domain. See Supported Domains
    :type DI: :py:ref:`RuntimeTypeDescriptor`
    :param DO: Output Domain. See Supported Domains
    :type DO: :py:ref:`RuntimeTypeDescriptor`
    :param MI: Input Metric. See Supported Metrics
    :type MI: :py:ref:`RuntimeTypeDescriptor`
    :param MO: Output Metric. See Supported Metrics
    :type MO: :py:ref:`RuntimeTypeDescriptor`
    :rtype: Transformation
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib", "honest-but-curious")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_function = py_to_c(function, c_type=CallbackFn, type_name=domain_carrier_type(DO))
    c_stability_map = py_to_c(stability_map, c_type=CallbackFn, type_name=metric_distance_type(MO))
    c_DI = py_to_c(DI, c_type=ctypes.c_char_p, type_name=None)
    c_DO = py_to_c(DO, c_type=ctypes.c_char_p, type_name=None)
    c_MI = py_to_c(MI, c_type=ctypes.c_char_p, type_name=None)
    c_MO = py_to_c(MO, c_type=ctypes.c_char_p, type_name=None)
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_default_user_transformation
    lib_function.argtypes = [CallbackFn, CallbackFn, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_function, c_stability_map, c_DI, c_DO, c_MI, c_MO), Transformation))
    output._depends_on(c_function, c_stability_map)
    return output


def make_fix_delta(
    measurement: Measurement,
    delta: Any
) -> Measurement:
    """Fix the delta parameter in the privacy map of a `measurement` with a SmoothedMaxDivergence output measure.
    
    [make_fix_delta in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_fix_delta.html)
    
    :param measurement: a measurement with a privacy curve to be fixed
    :type measurement: Measurement
    :param delta: parameter to fix the privacy curve with
    :type delta: Any
    :rtype: Measurement
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_measurement = py_to_c(measurement, c_type=Measurement, type_name=None)
    c_delta = py_to_c(delta, c_type=AnyObjectPtr, type_name=get_atom(measurement_output_distance_type(measurement)))
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_fix_delta
    lib_function.argtypes = [Measurement, AnyObjectPtr]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_measurement, c_delta), Measurement))
    output._depends_on(get_dependencies(measurement))
    return output


def make_population_amplification(
    measurement: Measurement,
    population_size: int
) -> Measurement:
    """Construct an amplified measurement from a `measurement` with privacy amplification by subsampling.
    This measurement does not perform any sampling. 
    It is useful when you have a dataset on-hand that is a simple random sample from a larger population.
    
    The DIA, DO, MI and MO between the input measurement and amplified output measurement all match.
    
    Protected by the "honest-but-curious" feature flag 
    because a dishonest adversary could set the population size to be arbitrarily large.
    
    [make_population_amplification in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_population_amplification.html)
    
    :param measurement: the computation to amplify
    :type measurement: Measurement
    :param population_size: the size of the population from which the input dataset is a simple sample
    :type population_size: int
    :rtype: Measurement
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib", "honest-but-curious")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_measurement = py_to_c(measurement, c_type=Measurement, type_name=AnyMeasurement)
    c_population_size = py_to_c(population_size, c_type=ctypes.c_size_t, type_name=usize)
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_population_amplification
    lib_function.argtypes = [Measurement, ctypes.c_size_t]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_measurement, c_population_size), Measurement))
    output._depends_on(get_dependencies(measurement))
    return output


def make_pureDP_to_fixed_approxDP(
    measurement: Measurement
) -> Measurement:
    """Constructs a new output measurement where the output measure
    is casted from `MaxDivergence<QO>` to `FixedSmoothedMaxDivergence<QO>`.
    
    [make_pureDP_to_fixed_approxDP in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_pureDP_to_fixed_approxDP.html)
    
    :param measurement: a measurement with a privacy measure to be casted
    :type measurement: Measurement
    :rtype: Measurement
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_measurement = py_to_c(measurement, c_type=Measurement, type_name=AnyMeasurement)
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_pureDP_to_fixed_approxDP
    lib_function.argtypes = [Measurement]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_measurement), Measurement))
    
    return output


def make_pureDP_to_zCDP(
    measurement: Measurement
) -> Measurement:
    """Constructs a new output measurement where the output measure
    is casted from `MaxDivergence<QO>` to `ZeroConcentratedDivergence<QO>`.
    
    [make_pureDP_to_zCDP in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_pureDP_to_zCDP.html)
    
    **Citations:**
    
    - [BS16 Concentrated Differential Privacy: Simplifications, Extensions, and Lower Bounds](https://arxiv.org/pdf/1605.02065.pdf#subsection.3.1)
    
    :param measurement: a measurement with a privacy measure to be casted
    :type measurement: Measurement
    :rtype: Measurement
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_measurement = py_to_c(measurement, c_type=Measurement, type_name=AnyMeasurement)
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_pureDP_to_zCDP
    lib_function.argtypes = [Measurement]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_measurement), Measurement))
    
    return output


def make_zCDP_to_approxDP(
    measurement: Measurement
) -> Measurement:
    """Constructs a new output measurement where the output measure
    is casted from `ZeroConcentratedDivergence<QO>` to `SmoothedMaxDivergence<QO>`.
    
    [make_zCDP_to_approxDP in Rust documentation.](https://docs.rs/opendp/latest/opendp/combinators/fn.make_zCDP_to_approxDP.html)
    
    :param measurement: a measurement with a privacy measure to be casted
    :type measurement: Measurement
    :rtype: Measurement
    :raises TypeError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    assert_features("contrib")
    
    # No type arguments to standardize.
    # Convert arguments to c types.
    c_measurement = py_to_c(measurement, c_type=Measurement, type_name=AnyMeasurement)
    
    # Call library function.
    lib_function = lib.opendp_combinators__make_zCDP_to_approxDP
    lib_function.argtypes = [Measurement]
    lib_function.restype = FfiResult
    
    output = c_to_py(unwrap(lib_function(c_measurement), Measurement))
    output._depends_on(get_dependencies(measurement))
    return output
