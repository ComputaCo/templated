from typing import Literal

from parselpy.utils.determine_template_type import determine_template_type
from parselpy.utils.llms import LLM_CONSTRUCTORS


class Function:
    def __init__(
        self,
        template,
        template_format: Literal["Jinja2", "f-string"] = None,
        llm=None,
        verbose=False,
        **llm_kwargs,
    ):
        self.template_text = template
        self.template_format = template_format or determine_template_type(template)
        match self.template_format:
            case "Jinja2":
                from jinja2 import Template

                self.template = Template(template)
            case "f-string":
                self.template = template
            case _:
                raise ValueError(f"Invalid template format: {self.template_format}")
        self.llm = llm or self.make_default_llm(llm_kwargs=llm_kwargs)
        self.verbose = verbose

    def __call__(self, **kwargs):
        rendered_template = self._render_template(**kwargs)
        if self.verbose:
            print(f"Rendered template: {rendered_template}")
        return self.llm(rendered_template)

    def _render_template(self, **kwargs):
        match self.template_format:
            case "Jinja2":
                rendered_template = self.template.render(**kwargs)
            case "f-string":
                rendered_template = self.template.format(**kwargs)
            case _:
                raise ValueError(f"Invalid template format: {self.template_format}")
        if self.verbose:
            print(f"Rendered template: {rendered_template}")
        return rendered_template

    def make_default_llm(self, llm_kwargs={}):

        if "model" in llm_kwargs and llm_kwargs["model"] in LLM_CONSTRUCTORS:
            try:
                return LLM_CONSTRUCTORS[llm_kwargs["model"]](**llm_kwargs)
            except Exception as e:
                raise ValueError(f'Invalid LLM model: {llm_kwargs["model"]}') from e
        for model in LLM_CONSTRUCTORS:
            try:
                return LLM_CONSTRUCTORS[model](**llm_kwargs)
            except Exception as e:
                pass
        raise ValueError(f"No valid LLM model found")
