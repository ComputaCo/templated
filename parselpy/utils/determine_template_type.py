import re


def determine_template_type(string):
    fstring_regex = r'^f?[\'"](.*?)?[\'"]$'
    jinja_regex = r"{{.*?}}"

    if re.match(fstring_regex, string):
        return "f-string"
    elif re.search(jinja_regex, string):
        return "Jinja2"
    else:
        return "Unknown string type"
