# numpy 2.2.6 (Major v2)

VFX Platform 2025 compatible build package for numpy.

## Package Information

- **Package Name**: numpy
- **Version**: 2.2.6
- **Major Version**: 2
- **Repository**: vfxplatform-2025/numpy-2
- **Description**: NumPy는 Python을 위한 고성능 수치 배열 라이브러리입니다.

## Build Instructions

```bash
rez-build -i
```

## Package Structure

```
numpy/
├── 2.2.6/
│   ├── package.py      # Rez package configuration
│   ├── rezbuild.py     # Build script
│   ├── get_source.sh   # Source download script (if applicable)
│   └── README.md       # This file
```

## Installation

When built with `install` target, installs to: `/core/Linux/APPZ/packages/numpy/2.2.6`

## Version Strategy

This repository contains **Major Version 2** of numpy. Different major versions are maintained in separate repositories:

- Major v2: `vfxplatform-2025/numpy-2`

## VFX Platform 2025

This package is part of the VFX Platform 2025 initiative, ensuring compatibility across the VFX industry standard software stack.
