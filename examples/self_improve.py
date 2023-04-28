from glob import glob
from pathlib import Path
from textwrap import dedent

from templated import Function

ai = Function(
    dedent(
        """
        You are an artificial intelligence system. This is your codebase:
        
        {% for path, code in codebase %}
        Path: {{ path }}
        {{ code }}
        ---
        
        {% endfor %}
        
        Based on your current codebase, please suggest a new function that will make you more capable. Then, implement it.
        """
    ),
    verbose=True,
)

paths = Path("templated").glob("**/*.py")
paths = filter(lambda path: path.is_file(), paths)
codebase = [(path, path.read_text()) for path in paths]

response = ai(codebase=codebase)

print(response)
