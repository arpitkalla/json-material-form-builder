from textwrap import indent

keys = {}


def to_hook(key):
    return f"""set{key.replace("_", " ").title().replace(" ", "")}"""


def add_keys(json_data):
    def add_key(k, options):
        if k in keys:
            raise ValueError(f"Duplicate key '{k}' found")
        keys[k] = options[0] if len(options) > 0 else ""

    for component in json_data:
        if component["type"] == "row":
            for c in component["columns"]:
                add_key(c["key"], c.get("options", []))
        else:
            add_key(component["key"], component.get("options", []))


def make_use_hooks(s, indent_lvl):
    for key, val in keys.items():
        s.append(
            indent(
                f"""const [{key}, {to_hook(key)}] = useState('{val}');""",
                "\t" * indent_lvl,
            )
        )


def make_on_submit(s, indent_lvl):
    s.append(indent("""const onSubmit = () => {""", "\t" * indent_lvl))
    indent_lvl += 1
    s.append(indent("""console.log({""", "\t" * indent_lvl))
    indent_lvl += 1
    for key, val in keys.items():
        s.append(indent(f""""{key}": {key},""", "\t" * indent_lvl))
    indent_lvl -= 1
    s.append(indent("""});""", "\t" * indent_lvl))
    indent_lvl -= 1
    s.append(indent("""}""", "\t" * indent_lvl))


def add_radio(s, component, indent_lvl):
    label, options, key = component["label"], component["options"], component["key"]
    s.append(
        indent(
            f"""<FormLabel component="legend">{label}</FormLabel>""", "\t" * indent_lvl
        )
    )
    s.append(
        indent(
            f"""<RadioGroup aria-label="{key}" name="{key}" onChange={{e => {to_hook(key)}(e.target.value)}} value={{{key}}}>""",
            "\t" * indent_lvl,
        )
    )
    indent_lvl += 1
    for option in options:
        s.append(
            indent(
                f"""<FormControlLabel value="{option}" control={{<Radio />}} label="{option}" />""",
                "\t" * indent_lvl,
            )
        )
    indent_lvl -= 1
    s.append(indent(f"""</RadioGroup>""", "\t" * indent_lvl))


def add_textfile(s, component, indent_lvl):
    label, key = component["label"], component["key"]
    s.append(
        indent(
            f"""<TextField id="standard-basic" label="{label}" onChange={{e => {to_hook(key)}(e.target.value)}} />""",
            "\t" * indent_lvl,
        )
    )


def add_component(s, component, indent_lvl, row=None):
    if row is not None:
        s.append(indent(f'<div class="row-{row}">', "\t" * indent_lvl))
        indent_lvl += 1

    if component["type"] == "row":
        for c in component["columns"]:
            add_component(s, c, indent_lvl)
    elif component["type"] == "text":
        add_textfile(s, component, indent_lvl)
    elif component["type"] == "radio":
        add_radio(s, component, indent_lvl)

    if row is not None:
        indent_lvl -= 1
        s.append(indent(f"</div>", "\t" * indent_lvl))


def parse_json(json_data):
    s = []
    indent_lvl = 0
    add_keys(json_data)
    make_use_hooks(s, indent_lvl)
    make_on_submit(s, indent_lvl)
    s.append(indent("return (", "\t" * indent_lvl))
    indent_lvl += 1

    # Add Form
    s.append(indent("<FormControl>", "\t" * indent_lvl))
    indent_lvl += 1
    # Add Components
    for i, component in enumerate(json_data):
        add_component(s, component, indent_lvl, row=i)
    # Add Submit Button
    s.append(
        indent(
            """<Button color="primary" onClick={onSubmit}>Submit</Button>""",
            "\t" * indent_lvl,
        )
    )
    indent_lvl -= 1
    s.append(indent("</FormControl>", "\t" * indent_lvl))
    indent_lvl -= 1
    s.append(indent(")", "\t" * indent_lvl))
    return "\n".join(s)