import subprocess
import os
import sys

def make_executable(prog: str, lang: str) -> str:
    """
    Write source code to a file and compile if needed.
    Returns:
        "OK" if compilation (or setup) succeeded,
        "CE" if there was a compile error.
    """
    if lang == "python":
        src = "program.py"
        with open(src, "w") as f:
            f.write(prog)
    elif lang in ("c++", "c"):  # C and C++
        ext = "cpp" if lang == "c++" else "c"
        src = f"program.{ext}"
        exe = "program_exec"
        with open(src, "w") as f:
            f.write(prog)
        compiler = "g++" if lang == "c++" else "gcc"
        compiled = subprocess.run([compiler, src, "-o", exe], capture_output=True)
        if compiled.returncode != 0:
            # Clean up source on compile error
            os.remove(src)
            return "CE"
        # Remove source file, keep executable
        os.remove(src)
        return "OK"
    else:
        return "CE"
    return "OK"


def single_test(lang: str, inp: str, expected: str, tl: float) -> str:
    """
    Run a single test case by feeding inp to the executable and comparing its output to expected.
    Returns status code strings: "OK", "TL", "RE", or "WA".
    """
    # Write input to temporary file
    in_file = "input.txt"
    with open(in_file, "w") as f:
        f.write(inp)

    cmd = []
    if lang == "python":
        cmd = [sys.executable, "program.py"]
    else:
        cmd = ["./program_exec"]

    try:
        proc = subprocess.run(cmd, stdin=open(in_file, "r"), timeout=tl, capture_output=True)
    except subprocess.TimeoutExpired:
        os.remove(in_file)
        return "TL"

    os.remove(in_file)

    if proc.returncode != 0:
        return "RE"

    out = str(proc.stdout.decode().rstrip("\n")).strip()
    if out != str(expected).strip():
        return "WA"
    return "OK"


def test(prog: str, lang: str, inputs: list, outputs: list, tl: float) -> str:
    """
    Run a sequence of tests on the given prog string in the specified language.
    Returns:
        "OK" if all tests pass,
        Otherwise, an error code with test number (e.g., "WA test #2").
    """
    status = make_executable(prog, lang)
    if status != "OK":
        return status

    for idx, (inp, expected) in enumerate(zip(inputs, outputs), start=1):
        status = single_test(lang, inp, expected, tl)
        if status != "OK":
            # Clean up executable or script
            if lang == "python":
                os.remove("program.py")
            else:
                os.remove("program_exec")
            return f"{status} test #{idx}"

    # Cleanup after all tests
    if lang == "python":
        os.remove("program.py")
    else:
        os.remove("program_exec")
    return "OK"

# Example usage when running this file directly:
if __name__ == "__main__":
    # Placeholder: replace these with actual program and tests
    sample_prog = sys.stdin.read()
    # Parse arguments or integrate with a higher-level runner
    print("This module defines 'test'. Use it within your own harness.")
