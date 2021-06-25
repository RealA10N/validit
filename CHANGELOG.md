# Changelog

All notable changes to *validit* will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.1] - 25.06.2021

### Fixed

- Fixed a bug that caused an unintentional error to raise when parsing of a
  configuration file failed.

## [1.3.0] - 25.06.2021

### Added

- Added the `Options` object template.

## [1.2.0] - 22.06.2021

### Added

- Added the `dump_errors` method in the `TemplateCheckErrorCollection` object.

### Changed

- Changed some validation methods to use the new `dump_errors` method.
  This is a purely internal change, and the user behavior should stay the same.

## [1.1.0] - 19.06.2021

### Added

- The `TemplateAny` template, that accepts any data.

## [1.0.2] - 18.06.2021

### Added

- If a default value is provided to the `Optional` object, it will be checks to
  see if it follows the template. If not, a `InvalidDefaultValue` exception will
  be raised. For example, `Optional(Template(str), default=123)` will raise an
  `InvalidDefaultValue` exception because the default value is an integer, but
  the template accepts only strings.

## [1.0.1] - 17.06.2021

### Added

- This changelog file!
- Option to import `BaseTemplate` using `from validit.templates import BaseTemplate`

[Unreleased]: https://github.com/reala10n/validit/compare/v1.3.1...HEAD
[1.3.1]: https://github.com/reala10n/validit/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/reala10n/validit/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/reala10n/validit/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/reala10n/validit/compare/v1.0.2...v1.1.0
[1.0.2]: https://github.com/reala10n/validit/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/reala10n/validit/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/reala10n/validit/releases/tag/v1.0.0
