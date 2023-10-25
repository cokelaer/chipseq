import os
import subprocess
import sys

from . import test_dir
datadir = f"{test_dir}/data/"
genomedir = f"{test_dir}/data/ecoli_MG1655"

def test_standalone_subprocess(tmp_path):
    wkdir = tmp_path / "test"
    wkdir.mkdir()
    cmd = f"sequana_chipseq --input-directory {datadir} --working-directory {wkdir} --force --genome-directory {genomedir} --design-file {datadir}/design.csv"
    subprocess.call(cmd.split())
    assert os.path.exists(wkdir / "config.yaml")

def test_standalone_script(tmp_path):
    wkdir = tmp_path / "test"
    wkdir.mkdir()
    import sequana_pipelines.chipseq.main as m
    sys.argv = ["test", "--input-directory", datadir, "--genome-directory", str(genomedir),  "--working-directory",str(wkdir), "--force", "--design-file", f"{datadir}/design.csv"]
    m.main()
    assert os.path.exists(wkdir / "config.yaml")

def test_full(tmp_path):

    wkdir = tmp_path / "test"
    wkdir.mkdir()

    cmd = f"sequana_chipseq --input-directory {datadir} --genome-directory {genomedir} --working-directory {str(wkdir)} --force --design-file {datadir}/design.csv"

    print(cmd)
    subprocess.call(cmd.split())
    assert os.path.exists(wkdir / "config.yaml")

    stat = subprocess.call("sh chipseq.sh".split(), cwd=wkdir)

    assert os.path.exists(wkdir / "summary.html")

def test_version():
    cmd = "sequana_chipseq --version"
    subprocess.call(cmd.split())

