from ollama import chat
import re
SUPPORTED_LANGUAGES = ['ada', 'agda', 'alloy', 'antlr', 'applescript', 'assembly', 'augeas', 'awk', 'batchfile', 'bluespec', 'c', 'c-sharp', 'clojure', 'cmake', 'coffeescript', 'common-lisp', 'cpp', 'css', 'cuda', 'dart', 'dockerfile', 'elixir', 'elm', 'emacs-lisp', 'erlang', 'f-sharp', 'fortran', 'glsl', 'go', 'groovy', 'haskell', 'html', 'idris', 'isabelle', 'java', 'java-server-pages', 'javascript', 'json', 'julia', 'jupyter-notebook', 'kotlin', 'lean', 'literate-agda', 'literate-coffeescript', 'literate-haskell', 'lua', 'makefile', 'maple', 'markdown', 'mathematica', 'matlab', 'ocaml', 'pascal', 'perl', 'php', 'powershell', 'prolog', 'protocol-buffer', 'python', 'r', 'racket', 'restructuredtext', 'rmarkdown', 'ruby', 'rust', 'sas', 'scala', 'scheme', 'shell', 'smalltalk', 'solidity', 'sparql', 'sql', 'stan', 'standard-ml', 'stata', 'systemverilog', 'tcl', 'tcsh', 'tex', 'thrift', 'typescript', 'verilog', 'vhdl', 'visual-basic', 'xslt', 'yacc', 'yaml', 'zig']
PROMPT ="""
Based on the above code and the below conditions:
Code is obfuscated in any way shape or form
Code is malicious.
Code runs any commands.
Code runs any shellcode.
Code transmits any secrets, environment variables and passwords.
Code evades any defenses.
Code injects into other processes.
Code enumerates network.
Code does any anti-debugging.

Give me ONLY a Yes or No answer based on whether it fits ANY of the criteria;
    Do not recommend me improvements;
Answer in this format: **answer**:answer\n
GIVE ME ONLY A YES OR NO ANSWER.
"""

def ds_checkcode(code: str, verbose:bool = False, prompt: str = PROMPT) -> str:
    full_response = ""
    stream = chat(
        model='deepseek-r1:7b',
        messages=[{'role': 'user', 'content': code + "\n" + prompt}],
        stream=True,
    )
    for chunk in stream:
        full_response += chunk['message']['content']
        if verbose: print(chunk['message']['content'], end='', flush=True)
    resp = re.search(r"\*\*answer\*\*:\s?(\w+)", full_response, re.IGNORECASE)
    if resp:
        return resp.group(1).strip().capitalize() == 'Yes'
    return False
    

if __name__ == "__main__":
    with open('E:/Ollama/exclusions/virus.txt', 'r') as file:
        code = file.read()  # Read the entire content of the file]
    print(ds_checkcode(code))