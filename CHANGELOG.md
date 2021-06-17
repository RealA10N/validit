# Changelog

All notable changes to *validit* will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- If a default value is provided to the `Optional` object, it will be checks to
  see if it follows the template. If not, a `InvalidDefaultValue` exception will
  be raised.
  
  For example, `Optional(Template(str), default=123)` will raise an
  `InvalidDefaultValue` exception because the default value is an integer, but
  the template accepts only strings.

## [1.0.1] - 17.06.2021

### Added

- This changelog file!
- Option to import `BaseTemplate` using `from validit.templates import BaseTemplate`

[Unreleased]: https://github.com/reala10n/validit/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/reala10n/validit/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/reala10n/validit/releases/tag/v1.0.0
