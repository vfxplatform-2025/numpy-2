#!/usr/bin/env bash
set -e
set -x

# 1) 버전 결정
if [ -n "$REZ_BUILD_PROJECT_VERSION" ]; then
    version="$REZ_BUILD_PROJECT_VERSION"
else
    dirname=$(basename "$PWD")
    version="${dirname#numpy-}"
    echo "REZ_BUILD_PROJECT_VERSION 미설정, dirname에서 버전 추출: $version"
fi

# 2) 경로 설정
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$script_dir/source"
target_dir="$source_dir/numpy-$version"

# 3) Git 검사
command -v git >/dev/null || { echo "git 필요"; exit 1; }

# 4) 기존 소스 제거 후 재클론 (서브모듈 포함)
rm -rf "$target_dir"
mkdir -p "$source_dir"
git clone --depth 1 --branch "v$version" --recurse-submodules \
    https://github.com/numpy/numpy.git "$target_dir"

# 5) 확인
echo "클론 및 서브모듈 초기화 완료:"
ls -1 "$target_dir/vendored-meson/meson" 2>/dev/null || echo "(vendored-meson 없음 - wheel 설치 방식이므로 무관)"

echo "NumPy ${version} 소스 준비 완료: $target_dir"
