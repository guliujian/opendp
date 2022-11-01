#[cfg(feature = "ffi")]
mod ffi;

use std::ops::Shr;

use crate::core::{
    Domain, Function, Measure, Measurement, Metric, MetricSpace, Postprocessor, PrivacyMap,
    StabilityMap, Transformation,
};
use crate::error::Fallible;
use std::fmt::Debug;

const ERROR_URL: &str = "https://github.com/opendp/opendp/discussions/297";

fn mismatch_message<T1: Debug, T2: Debug>(mode: &str, struct1: &T1, struct2: &T2) -> String {
    let str1 = format!("{:?}", struct1);
    let str2 = format!("{:?}", struct2);
    let explanation = if str1 == str2 {
        format!("\n    The structure of the intermediate {mode}s are the same, but the parameters differ.\n    shared_{mode}: {str1}\n", mode=mode, str1=str1)
    } else {
        format!(
            "\n    output_{mode}: {struct1}\n    input_{mode}:  {struct2}\n",
            mode = mode,
            struct1 = str1,
            struct2 = str2
        )
    };
    return format!(
        "Intermediate {}s don't match. See {}{}",
        mode, ERROR_URL, explanation
    );
}

/// Construct the functional composition (`measurement1` ○ `transformation0`).
/// Returns a Measurement that when invoked, computes `measurement1(transformation0(x))`.
///
/// # Arguments
/// * `measurement1` - outer measurement/mechanism
/// * `transformation0` - inner transformation
///
/// # Generics
/// * `DI` - Input Domain.
/// * `DX` - Intermediate Domain.
/// * `DO` - Output Domain.
/// * `MI` - Input Metric.
/// * `MX` - Intermediate Metric.
/// * `MO` - Output Measure.
pub fn make_chain_mt<DI, DX, DO, MI, MX, MO>(
    measurement1: &Measurement<DX, DO, MX, MO>,
    transformation0: &Transformation<DI, DX, MI, MX>,
) -> Fallible<Measurement<DI, DO, MI, MO>>
where
    DI: 'static + Domain,
    DX: 'static + Domain,
    DO: 'static + Domain,
    MI: 'static + Metric,
    MX: 'static + Metric,
    MO: 'static + Measure,
    (DI, MI): MetricSpace,
    (DX, MX): MetricSpace,
{
    if transformation0.output_domain != measurement1.input_domain {
        return fallible!(
            DomainMismatch,
            mismatch_message(
                "domain",
                &transformation0.output_domain,
                &measurement1.input_domain
            )
        );
    }
    if transformation0.output_metric != measurement1.input_metric {
        return fallible!(
            MetricMismatch,
            mismatch_message(
                "metric",
                &transformation0.output_metric,
                &measurement1.input_metric
            )
        );
    }

    Ok(Measurement::new(
        transformation0.input_domain.clone(),
        measurement1.output_domain.clone(),
        Function::make_chain(&measurement1.function, &transformation0.function),
        transformation0.input_metric.clone(),
        measurement1.output_measure.clone(),
        PrivacyMap::make_chain(&measurement1.privacy_map, &transformation0.stability_map),
    ))
}

/// Construct the functional composition (`transformation1` ○ `transformation0`).
/// Returns a Measurement that when invoked, computes `transformation1(transformation0(x))`.
///
/// # Arguments
/// * `transformation1` - outer transformation
/// * `transformation0` - inner transformation
///
/// # Generics
/// * `DI` - Input Domain.
/// * `DX` - Intermediate Domain.
/// * `DO` - Output Domain.
/// * `MI` - Input Metric.
/// * `MX` - Intermediate Metric.
/// * `MO` - Output Metric.
pub fn make_chain_tt<DI, DX, DO, MI, MX, MO>(
    transformation1: &Transformation<DX, DO, MX, MO>,
    transformation0: &Transformation<DI, DX, MI, MX>,
) -> Fallible<Transformation<DI, DO, MI, MO>>
where
    DI: 'static + Domain,
    DX: 'static + Domain,
    DO: 'static + Domain,
    MI: 'static + Metric,
    MX: 'static + Metric,
    MO: 'static + Metric,
    (DI, MI): MetricSpace,
    (DX, MX): MetricSpace,
    (DO, MO): MetricSpace,
{
    if transformation0.output_domain != transformation1.input_domain {
        return fallible!(
            DomainMismatch,
            mismatch_message(
                "domain",
                &transformation0.output_domain,
                &transformation1.input_domain
            )
        );
    }
    if transformation0.output_metric != transformation1.input_metric {
        return fallible!(
            MetricMismatch,
            mismatch_message(
                "metric",
                &transformation0.output_metric,
                &transformation1.input_metric
            )
        );
    }

    Ok(Transformation::new(
        transformation0.input_domain.clone(),
        transformation1.output_domain.clone(),
        Function::make_chain(&transformation1.function, &transformation0.function),
        transformation0.input_metric.clone(),
        transformation1.output_metric.clone(),
        StabilityMap::make_chain(
            &transformation1.stability_map,
            &transformation0.stability_map,
        ),
    ))
}

/// Construct the functional composition (`postprocessor1` ○ `measurement0`).
/// Returns a Measurement that when invoked, computes `postprocessor1(measurement0(x))`.
/// Used to represent non-interactive postprocessing.
///
/// # Arguments
/// * `transformation1` - outer postprocessor
/// * `measurement0` - inner measurement/mechanism
///
/// # Generics
/// * `DI` - Input Domain.
/// * `DX` - Intermediate Domain.
/// * `DO` - Output Domain.
/// * `MMI` - Input Measurement Metric.
/// * `MMO` - Output Measurement Metric.
pub fn make_chain_pm<DI, DX, DO, MMI, MMO>(
    postprocessor0: &Postprocessor<DX, DO>,
    measurement0: &Measurement<DI, DX, MMI, MMO>,
) -> Fallible<Measurement<DI, DO, MMI, MMO>>
where
    DI: 'static + Domain,
    DX: 'static + Domain,
    DO: 'static + Domain,
    MMI: 'static + Metric,
    MMO: 'static + Measure,
    (DI, MMI): MetricSpace,
{
    if measurement0.output_domain != postprocessor0.input_domain {
        return fallible!(
            DomainMismatch,
            mismatch_message(
                "domain",
                &measurement0.output_domain,
                &postprocessor0.input_domain
            )
        );
    }

    Ok(Measurement::new(
        measurement0.input_domain.clone(),
        postprocessor0.output_domain.clone(),
        Function::make_chain(&postprocessor0.function, &measurement0.function),
        measurement0.input_metric.clone(),
        measurement0.output_measure.clone(),
        measurement0.privacy_map.clone(),
    ))
}

// UNIT TESTS
#[cfg(test)]
mod tests {
    use crate::core::*;
    use crate::domains::AllDomain;
    use crate::error::ExplainUnwrap;
    use crate::measures::MaxDivergence;
    use crate::metrics::AbsoluteDistance;

    use super::*;

    #[test]
    fn test_make_chain_mt() {
        let input_domain0 = AllDomain::<u8>::new();
        let output_domain0 = AllDomain::<i32>::new();
        let function0 = Function::new(|a: &u8| (a + 1) as i32);
        let input_metric0 = AbsoluteDistance::<i32>::default();
        let output_metric0 = AbsoluteDistance::<i32>::default();
        let stability_map0 = StabilityMap::new_from_constant(1);
        let transformation0 = Transformation::new(
            input_domain0,
            output_domain0,
            function0,
            input_metric0,
            output_metric0,
            stability_map0,
        );
        let input_domain1 = AllDomain::<i32>::new();
        let output_domain1 = AllDomain::<f64>::new();
        let function1 = Function::new(|a: &i32| (a + 1) as f64);
        let input_metric1 = AbsoluteDistance::<i32>::default();
        let output_measure1 = MaxDivergence::default();
        let privacy_map1 = PrivacyMap::new(|d_in: &i32| *d_in as f64 + 1.);
        let measurement1 = Measurement::new(
            input_domain1,
            output_domain1,
            function1,
            input_metric1,
            output_measure1,
            privacy_map1,
        );
        let chain = make_chain_mt(&measurement1, &transformation0).unwrap_test();

        let arg = 99_u8;
        let ret = chain.invoke(&arg).unwrap_test();
        assert_eq!(ret, 101.0);

        let d_in = 99_i32;
        let d_out = chain.map(&d_in).unwrap_test();
        assert_eq!(d_out, 100.);
    }

    #[test]
    fn test_make_chain_tt() {
        let input_domain0 = AllDomain::<u8>::new();
        let output_domain0 = AllDomain::<i32>::new();
        let function0 = Function::new(|a: &u8| (a + 1) as i32);
        let input_metric0 = AbsoluteDistance::<i32>::default();
        let output_metric0 = AbsoluteDistance::<i32>::default();
        let stability_map0 = StabilityMap::new_from_constant(1);
        let transformation0 = Transformation::new(
            input_domain0,
            output_domain0,
            function0,
            input_metric0,
            output_metric0,
            stability_map0,
        );
        let input_domain1 = AllDomain::<i32>::new();
        let output_domain1 = AllDomain::<f64>::new();
        let function1 = Function::new(|a: &i32| (a + 1) as f64);
        let input_metric1 = AbsoluteDistance::<i32>::default();
        let output_metric1 = AbsoluteDistance::<i32>::default();
        let stability_map1 = StabilityMap::new_from_constant(1);
        let transformation1 = Transformation::new(
            input_domain1,
            output_domain1,
            function1,
            input_metric1,
            output_metric1,
            stability_map1,
        );
        let chain = make_chain_tt(&transformation1, &transformation0).unwrap_test();

        let arg = 99_u8;
        let ret = chain.invoke(&arg).unwrap_test();
        assert_eq!(ret, 101.0);

        let d_in = 99_i32;
        let d_out = chain.map(&d_in).unwrap_test();
        assert_eq!(d_out, 99);
    }

    #[test]
    fn test_make_chain_pm() {
        let input_domain0 = AllDomain::<u8>::new();
        let output_domain0 = AllDomain::<i32>::new();
        let function0 = Function::new(|a: &u8| (a + 1) as i32);
        let input_metric0 = AbsoluteDistance::<i32>::default();
        let output_measure0 = MaxDivergence::<i32>::default();
        let privacy_map0 = PrivacyMap::new_from_constant(1);
        let measurement0 = Measurement::new(
            input_domain0,
            output_domain0,
            function0,
            input_metric0,
            output_measure0,
            privacy_map0,
        );
        let input_domain1 = AllDomain::<i32>::new();
        let output_domain1 = AllDomain::<f64>::new();
        let function1 = Function::new(|a: &i32| (a + 1) as f64);
        let postprocessor1 = Postprocessor::new(input_domain1, output_domain1, function1);
        let chain = make_chain_pm(&postprocessor1, &measurement0).unwrap_test();

        let arg = 99_u8;
        let ret = chain.invoke(&arg).unwrap_test();
        assert_eq!(ret, 101.0);

        let d_in = 99_i32;
        let d_out = chain.map(&d_in).unwrap_test();
        assert_eq!(d_out, 99);
    }
}

impl<DI, DX, DO, MI, MX, MO> Shr<Measurement<DX, DO, MX, MO>> for Transformation<DI, DX, MI, MX>
where
    DI: 'static + Domain,
    DX: 'static + Domain,
    DO: 'static + Domain,
    MI: 'static + Metric,
    MX: 'static + Metric,
    MO: 'static + Measure,
    (DI, MI): MetricSpace,
    (DX, MX): MetricSpace,
{
    type Output = Fallible<Measurement<DI, DO, MI, MO>>;

    fn shr(self, rhs: Measurement<DX, DO, MX, MO>) -> Self::Output {
        make_chain_mt(&rhs, &self)
    }
}

impl<DI, DX, DO, MI, MX, MO> Shr<Measurement<DX, DO, MX, MO>>
    for Fallible<Transformation<DI, DX, MI, MX>>
where
    DI: 'static + Domain,
    DX: 'static + Domain,
    DO: 'static + Domain,
    MI: 'static + Metric,
    MX: 'static + Metric,
    MO: 'static + Measure,
    (DI, MI): MetricSpace,
    (DX, MX): MetricSpace,
{
    type Output = Fallible<Measurement<DI, DO, MI, MO>>;

    fn shr(self, rhs: Measurement<DX, DO, MX, MO>) -> Self::Output {
        make_chain_mt(&rhs, &self?)
    }
}

impl<DI, DX, DO, MI, MX, MO> Shr<Transformation<DX, DO, MX, MO>> for Transformation<DI, DX, MI, MX>
where
    DI: 'static + Domain,
    DX: 'static + Domain,
    DO: 'static + Domain,
    MI: 'static + Metric,
    MX: 'static + Metric,
    MO: 'static + Metric,
    (DI, MI): MetricSpace,
    (DX, MX): MetricSpace,
    (DO, MO): MetricSpace,
{
    type Output = Fallible<Transformation<DI, DO, MI, MO>>;

    fn shr(self, rhs: Transformation<DX, DO, MX, MO>) -> Self::Output {
        make_chain_tt(&rhs, &self)
    }
}

impl<DI, DX, DO, MI, MX, MO> Shr<Transformation<DX, DO, MX, MO>>
    for Fallible<Transformation<DI, DX, MI, MX>>
where
    DI: 'static + Domain,
    DX: 'static + Domain,
    DO: 'static + Domain,
    MI: 'static + Metric,
    MX: 'static + Metric,
    MO: 'static + Metric,
    (DI, MI): MetricSpace,
    (DX, MX): MetricSpace,
    (DO, MO): MetricSpace,
{
    type Output = Fallible<Transformation<DI, DO, MI, MO>>;

    fn shr(self, rhs: Transformation<DX, DO, MX, MO>) -> Self::Output {
        make_chain_tt(&rhs, &self?)
    }
}

impl<DI, DX, DO, MMI, MMO> Shr<Postprocessor<DX, DO>> for Measurement<DI, DX, MMI, MMO>
where
    DI: 'static + Domain,
    DX: 'static + Domain,
    DO: 'static + Domain,
    MMI: 'static + Metric,
    MMO: 'static + Measure,
    (DI, MMI): MetricSpace,
{
    type Output = Fallible<Measurement<DI, DO, MMI, MMO>>;

    fn shr(self, rhs: Postprocessor<DX, DO>) -> Self::Output {
        make_chain_pm(&rhs, &self)
    }
}

impl<DI, DX, DO, MMI, MMO> Shr<Postprocessor<DX, DO>> for Fallible<Measurement<DI, DX, MMI, MMO>>
where
    DI: 'static + Domain,
    DX: 'static + Domain,
    DO: 'static + Domain,
    MMI: 'static + Metric,
    MMO: 'static + Measure,
    (DI, MMI): MetricSpace,
    (DX, MMO): MetricSpace,
    (DO, MMO): MetricSpace,
{
    type Output = Fallible<Measurement<DI, DO, MMI, MMO>>;

    fn shr(self, rhs: Postprocessor<DX, DO>) -> Self::Output {
        make_chain_pm(&rhs, &self?)
    }
}

#[cfg(test)]
mod tests_shr {
    use crate::measurements::make_base_discrete_laplace;
    use crate::transformations::{
        make_bounded_sum, make_cast_default, make_clamp, make_split_lines,
    };

    use super::*;

    #[test]
    fn test_shr() -> Fallible<()> {
        (make_split_lines()?
            >> make_cast_default()?
            >> make_clamp((0, 1))?
            >> make_bounded_sum((0, 1))?
            >> make_base_discrete_laplace(1.)?)
        .map(|_| ())
    }
}
