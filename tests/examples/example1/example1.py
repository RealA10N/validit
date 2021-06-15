from validit import Template, TemplateList, TemplateDict

__template__ = TemplateDict(
    title=Template(str),
    owner=TemplateDict(
        name=Template(str),
        dob=Template(str),
    ),
    database=TemplateDict(
        server=Template(str),
        ports=TemplateList(Template(int)),
        connection_max=Template(int),
        enabled=Template(bool),
    ),
    clients=TemplateDict(
        data=TemplateList(
            TemplateList(Template(str, int)),
        ),
        hosts=TemplateList(Template(str)),
    ),
)
