#[cfg(feature = "ffi")]
mod ffi;

use std::collections::HashSet;

use opendp_derive::bootstrap;

use crate::core::{Function, Measurement, PrivacyMap};
use crate::domains::AllDomain;
use crate::error::Fallible;
use crate::measures::MaxDivergence;
use crate::metrics::DiscreteDistance;
use crate::traits::samplers::{SampleBernoulli, SampleUniformIntBelow};
use crate::traits::{Hashable, Float};

// There are two constructors:
// 1. make_randomized_response_bool
//    a simple implementation specifically for booleans
// 2. make_randomized_response
//    for any categorical type with t > 1 categories
//
// The general rule is eps = (p / p').ln(), where p' = (1 - p) / (t - 1), and t = # categories
// See paper for more details: http://csce.uark.edu/~xintaowu/publ/DPL-2014-003.pdf
//
// In the case of privatizing a balanced coin flip,
//     t = 2, p = .75, giving eps = ln(.75 / .25) = ln(3)


#[bootstrap(
    features("contrib"),
    arguments(
        prob(c_type = "void *"), 
        constant_time(default = false))
)]
/// Make a Measurement that implements randomized response on a boolean value.
///
/// # Arguments
/// * `prob` - Probability of returning the correct answer. Must be in `[0.5, 1)`
/// * `constant_time` - Set to true to enable constant time. Slower.
/// 
/// # Generics
/// * `QO` - Data type of probability and output distance.
pub fn make_randomized_response_bool<QO>(
    prob: QO,
    constant_time: bool,
) -> Fallible<Measurement<AllDomain<bool>, AllDomain<bool>, DiscreteDistance, MaxDivergence<QO>>>
    where bool: SampleBernoulli<QO>,
          QO: Float {

    // number of categories t is 2, and probability is bounded below by 1/t
    if !(QO::exact_int_cast(2)?.recip()..QO::one()).contains(&prob) {
        return fallible!(MakeTransformation, "probability must be within [0.5, 1)");
    }

    // d_out = min(d_in, 1) * ln(p / p')
    //             where p' = 1 - p
    //       = min(d_in, 1) * ln(p / (1 - p))
    let privacy_constant = prob.inf_div(&QO::one().neg_inf_sub(&prob)?)?.inf_ln()?;

    Ok(Measurement::new(
        AllDomain::new(),
        AllDomain::new(),
        Function::new_fallible(move |arg: &bool| {
            Ok(arg ^ !bool::sample_bernoulli(prob, constant_time)?)
        }),
        DiscreteDistance::default(),
        MaxDivergence::default(),
        PrivacyMap::new(move |d_in| {
            if *d_in == 0 {
                QO::zero()
            } else {
                privacy_constant
            }
        }),
    ))
}

#[bootstrap(
    features("contrib"),
    arguments(
        categories(rust_type = "Vec<T>"),
        prob(c_type = "void *"), 
        constant_time(default = false)),
    generics(
        T(example = "$get_first(categories)"))
)]
/// Make a Measurement that implements randomized response on a categorical value.
///
/// # Arguments
/// * `categories` - Set of valid outcomes
/// * `prob` - Probability of returning the correct answer. Must be in `[1/num_categories, 1)`
/// * `constant_time` - Set to true to enable constant time. Slower.
/// 
/// # Generics
/// * `T` - Data type of a category.
/// * `QO` - Data type of probability and output distance.
pub fn make_randomized_response<T, QO>(
    categories: HashSet<T>,
    prob: QO,
    constant_time: bool,
) -> Fallible<Measurement<AllDomain<T>, AllDomain<T>, DiscreteDistance, MaxDivergence<QO>>>
    where T: Hashable,
          bool: SampleBernoulli<QO>,
          QO: Float {

    let categories = categories.into_iter().collect::<Vec<_>>();
    if categories.len() < 2 {
        return fallible!(
            MakeTransformation,
            "length of categories must be at least two"
        );
    }
    let num_categories = QO::exact_int_cast(categories.len())?;

    if !(num_categories.recip()..QO::one()).contains(&prob) {
        return fallible!(
            MakeTransformation,
            "probability must be within [1/num_categories, 1)"
        );
    }

    // d_out = min(d_in, 1) * (p / p').ln()
    //              where p' = the probability of categories off the diagonal
    //                       = (1 - p) / (t - 1)
    //              where t  = num_categories
    //       = min(d_in, 1) * (p / (1 - p) * (t - 1)).ln()
    let privacy_constant = prob
        .inf_div(&QO::one().neg_inf_sub(&prob)?)?
        .inf_mul(&num_categories.inf_sub(&QO::one())?)?
        .inf_ln()?;

    Ok(Measurement::new(
        AllDomain::new(),
        AllDomain::new(),
        Function::new_fallible(move |truth: &T| {
            // find index of truth in category set, or None
            let index = categories.iter().position(|cat| cat == truth);

            // randomly sample a lie from among the categories with equal probability
            // if truth in categories, sample among n - 1 categories
            let mut sample = usize::sample_uniform_int_below(
                categories.len() - if index.is_some() { 1 } else { 0 },
            )?;
            // shift the sample by one if index is greater or equal to the index of truth
            if let Some(i) = index {
                if sample >= i {
                    sample += 1
                }
            }
            let lie = &categories[sample];

            // return the truth if we chose to be honest and the truth is in the category set
            let be_honest = bool::sample_bernoulli(prob, constant_time)?;
            let is_member = index.is_some();
            Ok(if be_honest && is_member { truth } else { lie }.clone())
        }),
        DiscreteDistance::default(),
        MaxDivergence::default(),
        PrivacyMap::new(move |d_in| {
            if *d_in == 0 {
                QO::zero()
            } else {
                privacy_constant
            }
        }),
    ))
}

#[cfg(test)]
mod test {
    use super::*;
    use std::iter::FromIterator;
    use num::Float as _;

    #[test]
    fn test_bool() -> Fallible<()> {
        let ran_res = make_randomized_response_bool(0.75, false)?;
        let res = ran_res.invoke(&false)?;
        println!("{:?}", res);
        assert!(ran_res.check(&1, &3.0.ln())?);
        assert!(!ran_res.check(&1, &2.99999.ln())?);
        Ok(())
    }
    #[test]
    fn test_bool_extremes() -> Fallible<()> {
        // 50% chance that the output is correct means all information is lost, query is 0-dp
        let ran_res = make_randomized_response_bool(0.5, false)?;
        assert!(ran_res.check(&1, &0.0)?);
        // 100% chance that the output is correct is inf-dp, so expect an error
        assert!(make_randomized_response_bool(1.0, false).is_err());
        Ok(())
    }
    #[test]
    fn test_cat() -> Fallible<()> {
        let ran_res = make_randomized_response(
            HashSet::from_iter(vec![2, 3, 5, 6].into_iter()),
            0.75,
            false,
        )?;
        let res = ran_res.invoke(&3)?;
        println!("{:?}", res);
        // (.75 * 3 / .25) = 9
        assert!(ran_res.check(&1, &9.0.ln())?);
        assert!(!ran_res.check(&1, &8.99999.ln())?);
        Ok(())
    }
    #[test]
    fn test_cat_extremes() -> Fallible<()> {
        let ran_res = make_randomized_response(
            HashSet::from_iter(vec![2, 3, 5, 7, 8].into_iter()),
            1. / 5.,
            false,
        )?;
        assert!(ran_res.check(&1, &1e-10)?);
        assert!(make_randomized_response(
            HashSet::from_iter(vec![2, 3, 5, 7].into_iter()),
            1.,
            false
        )
        .is_err());
        Ok(())
    }
}
