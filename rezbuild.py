# rezbuild.py
# -*- coding: utf-8 -*-
"""
NumPy 2.2.6 빌드 스크립트
- PyPI에서 미리 빌드된 wheel 다운로드 후 설치
"""

import os, sys, shutil, subprocess, glob

def run_cmd(cmd, cwd=None, env=None):
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, shell=True, cwd=cwd, check=True, env=env)

def clean_build_dir(path):
    """build 디렉터리 내부만 삭제하되, *.rxt 및 variant.json 파일은 보존."""
    if os.path.isdir(path):
        print(f"Cleaning build dir (preserve *.rxt, variant.json): {path}")
        for item in os.listdir(path):
            if item.endswith(".rxt") or item == "variant.json":
                continue
            p = os.path.join(path, item)
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            else:
                os.remove(p)
    else:
        os.makedirs(path, exist_ok=True)

def clean_install_dir(path):
    """install 디렉터리 전체 삭제."""
    if os.path.isdir(path):
        print(f"Removing install dir: {path}")
        shutil.rmtree(path, ignore_errors=True)

def copy_license(src_dir, install_root):
    for fname in ("LICENSE", "COPYING", "COPYRIGHT", "LICENSE.txt"):
        p = os.path.join(src_dir, fname)
        if os.path.isfile(p):
            dst = os.path.join(install_root, "LICENSE")
            print(f"Copying {fname} -> {dst}")
            shutil.copy(p, dst)
            break

def write_build_marker(build_root):
    marker = os.path.join(build_root, "build.rxt")
    print(f"Touching build marker: {marker}")
    open(marker, "a").close()

def build(source_path, build_path, install_path, targets):
    version = os.environ["REZ_BUILD_PROJECT_VERSION"]
    # 1) build dir 초기화
    clean_build_dir(build_path)

    # 2) install 타겟이면 install_root override (variant 경로 포함)
    if "install" in targets:
        variant_subpath = os.environ.get("REZ_BUILD_VARIANT_SUBPATH", "")
        install_root = f"/core/Linux/APPZ/packages/numpy/{version}/{variant_subpath}"
        clean_install_dir(install_root)
        # 홈 packages 디렉토리도 삭제
        home_install = os.path.expanduser(f"~/packages/numpy/{version}/{variant_subpath}")
        clean_install_dir(home_install)
    else:
        variant_subpath = ""
        install_root = install_path

    # Python 버전 확인
    py_major = os.environ.get("REZ_PYTHON_MAJOR_VERSION", "3")
    py_minor = os.environ.get("REZ_PYTHON_MINOR_VERSION", "13")
    py_version = f"{py_major}.{py_minor}"
    print(f"Installing NumPy for Python {py_version}")

    # 3) 환경변수 설정
    build_env = os.environ.copy()
    # pip home/prefix 충돌 방지
    build_env.pop("PYTHONHOME", None)
    build_env.pop("PYTHONUSERBASE", None)
    build_env.pop("PIP_TARGET", None)

    # 4) wheel 다운로드 디렉토리 생성
    wheel_dir = os.path.join(build_path, "wheels")
    os.makedirs(wheel_dir, exist_ok=True)

    # 5) PyPI에서 wheel 다운로드 (미리 빌드된 바이너리)
    # numpy 2.2.x는 manylinux_2_17 플랫폼 사용
    pip_download_cmd = (
        f"pip download numpy=={version} "
        f"--dest={wheel_dir} "
        f"--only-binary=:all: "
        f"--no-deps "
        f"--python-version {py_major}.{py_minor} "
        f"--platform manylinux_2_17_x86_64 "
        f"-v"
    )
    run_cmd(pip_download_cmd, env=build_env)

    # 6) 다운로드된 wheel 파일 찾기
    wheel_files = glob.glob(os.path.join(wheel_dir, "numpy-*.whl"))
    if not wheel_files:
        raise FileNotFoundError(f"wheel 파일을 찾을 수 없습니다: {wheel_dir}")
    wheel_file = wheel_files[0]
    print(f"Downloaded wheel: {wheel_file}")

    # 7) wheel을 site-packages에 직접 설치 (unzip)
    site_packages = os.path.join(install_root, "lib", f"python{py_version}", "site-packages")
    os.makedirs(site_packages, exist_ok=True)

    # unzip으로 wheel 압축 해제 (wheel은 zip 파일)
    run_cmd(f"unzip -o {wheel_file} -d {site_packages}")

    # 8) 설치 완료 후 처리
    if "install" in targets:
        # LICENSE 복사 (wheel 내부 또는 소스에서)
        src_dir = os.path.join(source_path, "source", f"numpy-{version}")
        if os.path.isdir(src_dir):
            copy_license(src_dir, install_root)

        # package.py를 버전 루트에 복사 (variant 폴더가 아닌 상위 폴더)
        server_base = f"/core/Linux/APPZ/packages/numpy/{version}"
        os.makedirs(server_base, exist_ok=True)
        dst_pkg = os.path.join(server_base, "package.py")
        print(f"Copying package.py -> {dst_pkg}")
        shutil.copy(os.path.join(source_path, "package.py"), dst_pkg)
        # build.rxt 마커
        write_build_marker(build_path)

    print(f"numpy-{version} (Python {py_version}) install completed: {install_root}")

if __name__ == "__main__":
    build(
        source_path  = os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path   = os.environ["REZ_BUILD_PATH"],
        install_path = os.environ["REZ_BUILD_INSTALL_PATH"],
        targets      = sys.argv[1:]
    )
