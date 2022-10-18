# Imports
import os
import subprocess
import re




# Relative imports
from . import validate as v




# Shortcuts
from os.path import join




def format_private_key_hex(private_key_hex):
  # Example private_key_hex values:
  # '1234aabb'
  # '1234 aa bb'
  # '1234 AABB'
  private_key_hex = remove_whitespace(private_key_hex).lower()
  if len(private_key_hex) < 64:
    private_key_hex = private_key_hex.zfill(64)
  return private_key_hex




def remove_whitespace(text):
  return re.sub(r"\s+", "", text)




def shell_tool_exists(tool):
  if ' ' in tool:
    raise ValueError
  tool = 'command -v {}'.format(tool)
  output, exit_code = run_local_cmd(tool)
  return not exit_code




def run_local_cmd(cmd):
  proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = proc.communicate()
  exit_code = proc.wait()
  output = out.decode('ascii')
  err = err.decode('ascii')
  if err != '':
    msg = 'COMMAND FAILED\n' + '$ ' + cmd + '\n' + err
    stop(msg)
  return output, exit_code




def stop(msg=None):
  if msg is not None:
    print(msg)
  import sys
  sys.exit()
