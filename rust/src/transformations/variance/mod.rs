#[cfg(feature = "ffi")]
mod ffi;

use num::{Float as _, Zero};
use opendp_derive::bootstrap;

use crate::core::Transformation;
use crate::metrics::{AbsoluteDistance, SymmetricDistance};
use crate::domains::{AllDomain, BoundedDomain, SizedDomain, VectorDomain};
use crate::error::Fallible;
use crate::traits::{AlertingSub, ExactIntCast, InfDiv, InfMul, InfPow, InfSub, Float};

use super::{
    make_lipschitz_float_mul, make_sized_bounded_sum_of_squared_deviations,
    LipschitzMulFloatDomain, LipschitzMulFloatMetric, Pairwise, UncheckedSum,
};

#[bootstrap(
    features("contrib"),
    arguments(
        bounds(rust_type = "(T, T)"),
        ddof(default = 1)),
    generics(S(default = "Pairwise<T>", generics = "T")),
    derived_types(T = "$get_atom_or_infer(S, get_first(bounds))")
)]
/// Make a Transformation that computes the variance of bounded data. 
/// 
/// This uses a restricted-sensitivity proof that takes advantage of known dataset size. 
/// Use `make_clamp` to bound data and `make_bounded_resize` to establish dataset size.
/// 
/// # Citations
/// * [DHK15 Differential Privacy for Social Science Inference](http://hona.kr/papers/files/DOrazioHonakerKingPrivacy.pdf)
/// 
/// # Arguments
/// * `size` - Number of records in input data.
/// * `bounds` - Tuple of lower and upper bounds for data in the input domain.
/// * `ddof` - Delta degrees of freedom. Set to 0 if not a sample, 1 for sample estimate.
/// 
/// # Generics
/// * `S` - Summation algorithm to use on data type `T`. One of `Sequential<T>` or `Pairwise<T>`.
pub fn make_sized_bounded_variance<S>(
    size: usize,
    bounds: (S::Item, S::Item),
    ddof: usize,
) -> Fallible<
    Transformation<
        SizedDomain<VectorDomain<BoundedDomain<S::Item>>>,
        AllDomain<S::Item>,
        SymmetricDistance,
        AbsoluteDistance<S::Item>,
    >,
>
where
    S: UncheckedSum,
    S::Item: 'static + Float,
    AllDomain<S::Item>: LipschitzMulFloatDomain<Atom = S::Item>,
    AbsoluteDistance<S::Item>: LipschitzMulFloatMetric<Distance = S::Item>,
{
    if ddof >= size {
        return fallible!(MakeTransformation, "size - ddof must be greater than zero");
    }

    let constant = S::Item::exact_int_cast(size.alerting_sub(&ddof)?)?.recip();
    let _2 = S::Item::exact_int_cast(2)?;
    let _4 = S::Item::exact_int_cast(4)?;
    let size_ = S::Item::exact_int_cast(size)?;

    // Using Popoviciu's inequality on variances:
    //     variance <= (U - L)^2 / 4
    // Therefore ssd <= variance * size <= (U - L)^2 / 4 * size
    let upper_var_bound = (bounds.1)
        .inf_sub(&bounds.0)?
        .inf_pow(&_2)?
        .inf_div(&_4)?
        .inf_mul(&size_)?;

    make_sized_bounded_sum_of_squared_deviations::<Pairwise<_>>(size, bounds)?
        >> make_lipschitz_float_mul(constant, (S::Item::zero(), upper_var_bound))?
}

#[cfg(test)]
mod tests {
    use crate::{error::ExplainUnwrap, transformations::Pairwise};

    use super::*;

    #[test]
    fn test_make_sized_bounded_variance() {
        let arg = vec![1., 2., 3., 4., 5.];

        let transformation_sample =
            make_sized_bounded_variance::<Pairwise<_>>(5, (0., 10.), 1).unwrap_test();
        let ret = transformation_sample.invoke(&arg).unwrap_test();
        let expected = 2.5;
        assert_eq!(ret, expected);
        assert!(transformation_sample.check(&1, &(100. / 5.)).unwrap_test());

        let transformation_pop =
            make_sized_bounded_variance::<Pairwise<_>>(5, (0., 10.), 0).unwrap_test();
        let ret = transformation_pop.invoke(&arg).unwrap_test();
        let expected = 2.0;
        assert_eq!(ret, expected);
        assert!(transformation_pop
            .check(&1, &(100. * 4. / 25.))
            .unwrap_test());
    }
}
