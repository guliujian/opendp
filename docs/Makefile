# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
CARGO         = cargo
SPHINXAPIDOC  = sphinx-apidoc
SPHINXOPTS    = -W
SPHINXBUILD   = sphinx-build
SPHINXMULTI   = sphinx-multiversion
PAPER         =
BUILDDIR      = build
VERSION       = $(shell cat ../VERSION)

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make HTML files for current workspace (FOR TESTING, NOT USED IN RELEASE BUILDS)"
	@echo "  versions   to make HTML files for all committed versions"

clean:
	rm -rf $(BUILDDIR)/* source/api/python source/api/rust

html:
	$(SPHINXAPIDOC) -f -F -e -H "OpenDP" -A "The OpenDP Project" -V $(VERSION) -o source/api/python ../python/src/opendp --templatedir source/_templates
	# TODO: Figure out how to link locally generated Rust docs into sphinx structure.
	# 	cd ../rust && $(CARGO) doc --no-deps --target-dir ../docs/source/api/rust
	$(SPHINXBUILD) $(SPHINXOPTS) -D version=$(VERSION) -D 'html_sidebars.**'=search-field.html,sidebar-nav-bs.html source $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

html-rustdoc:
	cd ../rust && cargo rustdoc --features untrusted,derive -- --html-in-header katex.html --document-private-items

doctest: doctest-rust doctest-python
	@echo
	@echo "Doctest finished. The output is in $(BUILDDIR)/doctest/output.txt."

doctest-rust:
	cd ../rust && $(CARGO) test --doc

doctest-python: html
	$(SPHINXBUILD) $(SPHINXOPTS) -b doctest source $(BUILDDIR)/doctest

versions:
	# "/en" is the default, but someday we might have translations
	$(SPHINXMULTI) $(SPHINXOPTS) source $(BUILDDIR)/html/en
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."
	cp redirect.html $(BUILDDIR)/html/index.html
	@echo "Redirect page copied into $(BUILDDIR)/html."

latex:
	rm -rf build/html/proofs
	@for file in `find ../rust/src -type f -name "*.tex"`; do \
		[ -f "$$file" ] || break; \
		echo test "$$file"; \
		# switch to dir && out folder must exist && prevent stale links && build latex  \
		(cd `dirname $$file` && mkdir -p out && rm -f out/rustdoc.txt && pdflatex --output-directory=out --shell-escape `basename $$file`); \
		output_path=`dirname "$$file"`/out/`basename "$${file%.tex}.pdf"`; \
		target_path=$(BUILDDIR)/html/proofs/`echo $${file%.tex}.pdf | sed 's|../rust/src/|rust/src/|'`; \
		mkdir -p `dirname "$$target_path"`; \
		cp "$$output_path" "$$target_path"; \
	done

sphinx-server:
	@if [[ -z "${OPENDP_SPHINX_PORT}" ]]; then \
		echo "OPENDP_SPHINX_PORT must be set!"; \
		exit 1; \
	fi
	@kill -9 `lsof -ti:${OPENDP_SPHINX_PORT}` 2> /dev/null || true
	@echo Starting Sphinx at: http://localhost:${OPENDP_SPHINX_PORT}
	@python3 -m http.server ${OPENDP_SPHINX_PORT} --directory build/html

rustdoc-server:
	@if [[ -z "${OPENDP_RUSTDOC_PORT}" ]]; then \
		echo "OPENDP_RUSTDOC_PORT must be set!"; \
		exit 1; \
	fi
	@kill -9 `lsof -ti:${OPENDP_RUSTDOC_PORT}` 2> /dev/null || true
	@echo Starting Rustdoc at: http://localhost:${OPENDP_RUSTDOC_PORT}/opendp
	@python3 -m http.server ${OPENDP_RUSTDOC_PORT} --directory ../rust/target/doc/

server:
	@echo "quit server with CTRL-C"
	@make sphinx-server &
	@sleep 0.5 && echo
	@make rustdoc-server
	@wait