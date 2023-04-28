from glob import glob
from pathlib import Path
from textwrap import dedent

from parselpy import Function

ai = Function(
    dedent(
        """
        You are an large language model. This is your codebase:
        
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

paths = Path("parselpy").glob("**/*.py")
paths = filter(lambda path: path.is_file(), paths)
codebase = [(path, path.read_text()) for path in paths]

print(ai(codebase=codebase))
