from importlib.metadata import PackageNotFoundError, version

try:
    version = version("sequana-chipseq")
except PackageNotFoundError:
    version = "unknown"
