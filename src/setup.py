from cx_Freeze import setup, Executable

NAME = "msaccess2"
VERSION = "0.1"

options = {
    "bdist_mac": {
        "bundle_name": f"{NAME}-mac",
    },
    "build_exe": {
        "excludes": [
            "html", "http", "unittest", "sqlite3", "tkinter", "logging",
            "collections", "concurrent"
        ],
        "optimize": 2,
        "silent_level": 1
    }
}

executable = Executable(
    script="src/main.py",
    base="console",
    target_name=NAME
)

setup(
    name=f"{NAME}-wip",
    version="0.1",
    description="wip",
    author="Pedro H Costa (ptrrr1)",
    author_email="ptrrrdev@gmail.com",
    url="https://github.com/ptrrr1/msaccess2",
    executables=[executable],
    options=options
)
