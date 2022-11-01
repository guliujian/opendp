//! Various combinator constructors.

#[cfg(all(feature = "contrib", feature = "honest-but-curious"))]
mod amplify;
#[cfg(all(feature = "contrib", feature = "honest-but-curious"))]
pub use crate::combinators::amplify::*;

#[cfg(feature = "contrib")]
mod chain;
#[cfg(feature = "contrib")]
pub use crate::combinators::chain::*;

#[cfg(feature = "contrib")]
mod compose;
#[cfg(feature = "contrib")]
pub use crate::combinators::compose::*;

#[cfg(feature = "contrib")]
mod measure_cast;
#[cfg(feature = "contrib")]
pub use crate::combinators::measure_cast::*;

#[cfg(feature = "contrib")]
mod fix_delta;
#[cfg(feature = "contrib")]
pub use crate::combinators::fix_delta::*;

#[cfg(test)]
pub mod tests {
    use crate::core::{Function, Measurement, PrivacyMap, Transformation, Postprocessor};
    use crate::domains::{AllDomain, VectorDomain};
    use crate::error::*;
    use crate::measures::MaxDivergence;
    use crate::metrics::SymmetricDistance;
    use crate::traits::CheckNull;
    use crate::transformations;

    pub fn make_test_measurement<T: Clone + CheckNull>(
    ) -> Measurement<VectorDomain<AllDomain<T>>, AllDomain<T>, SymmetricDistance, MaxDivergence<f64>> {
        Measurement::new(
            VectorDomain::new_all(),
            AllDomain::new(),
            Function::new(|arg: &Vec<T>| arg[0].clone()),
            SymmetricDistance::default(),
            MaxDivergence::default(),
            PrivacyMap::new(|d_in| *d_in as f64 + 1.),
        )
    }

    pub fn make_test_transformation<T: Clone + CheckNull>(
    ) -> Transformation<VectorDomain<AllDomain<T>>, VectorDomain<AllDomain<T>>, SymmetricDistance, SymmetricDistance> {
        transformations::make_identity(VectorDomain::new_all(), SymmetricDistance::default())
            .unwrap_test()
    }

    pub fn make_test_postprocessor<T: Clone + CheckNull>(
    ) -> Postprocessor<AllDomain<T>, AllDomain<T>> {
        Postprocessor::new(
            AllDomain::new(),
            AllDomain::new(),
            Function::new(|arg: &T| arg.clone()),
        )
    }
}
