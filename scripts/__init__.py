import signal
import subprocess


def _get_project_dir() -> str:
    return (
        subprocess.check_output("git rev-parse --show-toplevel", shell=True)
        .decode("utf-8")
        .strip()
    )


def _run(script_name: str) -> None:
    try:
        project_dir = _get_project_dir()
        process = subprocess.Popen(
            f"cd {project_dir} && bash scripts/{script_name}.sh", shell=True
        )
        process.wait()
    except KeyboardInterrupt:
        process.send_signal(signal.SIGINT)
        process.wait()


def coverage() -> None:
    _run("tests-with-coverage")


def run_linter() -> None:
    _run("linter")
