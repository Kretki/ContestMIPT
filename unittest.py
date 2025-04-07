import subprocess


def make_executable(prog: str, lang: str):
  if (lang == "python"):
    file = open("program.py", "w")
    file.write(prog)
    file.close()
  elif (lang == "c++"):
    file = open("program.cpp", "w")
    file.write(prog)
    file.close()
    compiled = subprocess.run(["g++", "program.cpp"], capture_output=True)
    if (compiled.returncode != 0):
      return "CE"
    subprocess.run(["rm", "program.cpp"])
  elif (lang == "c"):
    file = open("program.c", "w")
    file.write(prog)
    file.close()
    compiled = subprocess.run(["gcc", "program.c"], capture_output=True)
    if (compiled.returncode != 0):
      return "CE"
    subprocess.run(["rm", "program.c"])
  return "OK"


def single_test(lang: str, inp: str, out: str, tl: float):
  file = open("input.txt", "w")
  file.write(inp)
  file.close()
  file = open("input.txt")
 
  try:
    if lang == "python":
      res = subprocess.run(["python3", "program.py"], stdin=file, timeout = tl, capture_output = True)
    elif lang == "c" or lang == "c++":
      res = subprocess.run(["./a.out"], stdin=file, timeout = tl, capture_output = True)
  except subprocess.TimeoutExpired:
    return "TL" 

  subprocess.run(["rm", "input.txt"])

  if res.returncode != 0:
    return "RE"

  prog_out = res.stdout.decode("utf-8")
  if (prog_out[-1] == "\n"):
    prog_out = prog_out[:-1]
  if out != prog_out:
    return "WA"

  return "OK"
    

def test(prog: str, lang: str, inputs: list, outputs: list, tl: float):
  res = make_executable(prog, lang)
  if res != "OK":
    return res
  for i in range(len(inputs)):
    res = single_test(lang, inputs[i], outputs[i], tl)
    if res != "OK":
      subprocess.run(["rm", "a.out" if lang != "python" else "program.py"])
      return res + " test #" + str(i+1)
  subprocess.run(["rm", "a.out" if lang != "python" else "program.py"])
  return "OK"
