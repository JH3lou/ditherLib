# Changelog

## [0.1.0] - 2025-04-15
### Added
- Initial release of DitherLib
- GUI built with `customtkinter`
- Classic dithering algorithms: Floyd-Steinberg, Burkes, Stucki, Sierra variants, Atkinson
- CustomAdaptiveDither with override parameters
- Unit tests for each algorithm
- Real-time image preview
- Gamma correction and downscale controls
- Loading overlay and threading for responsive UI

### Fixed
- Bug with algorithm name resolution for config-based dispatch

### Next Up
- Add histogram updates and live RGB analysis
- Implement tone zones and custom blue-noise patterns
