from datetime import datetime, date
from validit import Template, TemplateDict, TemplateList


__template__ = TemplateDict(
    posts=TemplateList(TemplateDict(
        title=Template(str),
        author=Template(str),
        posted=Template(datetime, date),
    )),
)
