from typing import TypeAlias

from docutils.nodes import Text, TextElement
from sphinx.addnodes import pending_xref
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.ext.intersphinx import missing_reference

from sphinx_refs_alias import __version__

T_REFS_ALIAS: TypeAlias = dict[str, str | tuple[str, str | None]]


def resolve_reference_aliases(app: Sphinx, env: BuildEnvironment, node: pending_xref, contnode: TextElement):
    """based on https://stackoverflow.com/a/62301461/18269227"""
    reference_aliases: T_REFS_ALIAS = app.config["reference_aliases"]

    alias = node.get("reftarget")
    if (value := reference_aliases.get(alias)) is not None:
        new_ref: str
        new_text: str | None
        if isinstance(value, str):
            new_ref = value
            new_text = None
        elif isinstance(value, tuple) and len(value) == 2:
            new_ref, new_text = reference_aliases[alias]
        else:
            raise ValueError("The values in 'reference_aliases' must be a str or a tuple[str, str | None]")

        node["reftarget"] = new_ref
        if new_text is not None:
            text_node = next(iter(node.findall(lambda n: n.tagname == "#text")))
            text_node.parent.replace(text_node, Text(new_text))
        return missing_reference(app, env, node, contnode)
    return None


def setup(app: Sphinx) -> dict:
    app.add_config_value("reference_aliases", dict, "env", T_REFS_ALIAS)
    app.connect("missing-reference", resolve_reference_aliases)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
