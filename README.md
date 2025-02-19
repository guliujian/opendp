# OpenDP
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org/)
[![ci tests](https://github.com/opendp/opendp/actions/workflows/smoke-test.yml/badge.svg)](https://github.com/opendp/opendp/actions/workflows/smoke-test.yml?query=branch%3Amain)

The OpenDP Library is a modular collection of statistical algorithms that adhere to the definition of
[differential privacy](https://en.wikipedia.org/wiki/Differential_privacy).
It can be used to build applications of privacy-preserving computations, using a number of different models of privacy.
OpenDP is implemented in Rust, with bindings for easy use from Python.

The architecture of the OpenDP Library is based on a conceptual framework for expressing privacy-aware computations.
This framework is described in the paper [A Programming Framework for OpenDP](https://projects.iq.harvard.edu/files/opendp/files/opendp_programming_framework_11may2020_1_01.pdf).

The OpenDP Library is part of the larger [OpenDP Project](https://opendp.org), a community effort to build trustworthy,
open source software tools for analysis of private data.
(For simplicity in these docs, when we refer to “OpenDP,” we mean just the library, not the entire project.)

## Status

OpenDP is under development, and we expect to [release new versions](https://github.com/opendp/opendp/releases) frequently,
incorporating feedback and code contributions from the OpenDP Community.
It's a work in progress, but it can already be used to build some applications and to prototype contributions that will expand its functionality.
We welcome you to try it and look forward to feedback on the library! However, please be aware of the following limitations:

> OpenDP, like all real-world software, has both known and unknown issues.
> If you intend to use OpenDP for a privacy-critical application, you should evaluate the impact of these issues on your use case.
> 
> More details can be found in the [Limitations section of the User Guide](https://docs.opendp.org/en/stable/user/limitations.html).


## Installation

The easiest way to install OpenDP is using `pip` (the [package installer for Python](https://pypi.org/project/pip/)):

    $ pip install opendp

More information can be found in the [Getting Started section of the User Guide](https://docs.opendp.org/en/stable/user/getting-started.html).

## Documentation

The full documentation for OpenDP is located at https://docs.opendp.org. Here are some helpful entry points:

* [User Guide](https://docs.opendp.org/en/stable/user/index.html)
* [Python API Docs](https://docs.opendp.org/en/stable/api/python/index.html)
* [Developer Guide](https://docs.opendp.org/en/stable/developer/index.html)

## Getting Help

If you're having problems using OpenDP, or want to submit feedback, please reach out! Here are some ways to contact us:

* Ask questions on our [discussions forum](https://github.com/opendp/opendp/discussions)
* Open issues on our [issue tracker](https://github.com/opendp/opendp/issues)
* Join our [Slack](https://join.slack.com/t/opendp/shared_invite/zt-zw7o1k2s-dHg8NQE8WTfAGFnN_cwomA)
* Send general queries to [info@opendp.org](mailto:info@opendp.org)
* Reach us on Twitter at [@opendp_org](https://twitter.com/opendp_org)

## Contributing

OpenDP is a community effort, and we welcome your contributions to its development! 
If you'd like to participate, please contact us! We also have a [contribution process section in the Developer Guide](https://docs.opendp.org/en/stable/developer/contribution-process.html).
