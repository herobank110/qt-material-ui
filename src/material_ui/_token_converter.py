from collections import defaultdict
from dataclasses import dataclass, replace
from functools import partial
from itertools import batched, product
import json
from pathlib import Path

import re
import tempfile
import httpx
import asyncio
from qtpy.QtGui import QColor

from material_ui.tokens._core import TokenValue


TOKEN_TABLE_URL_FORMAT = (
    "https://m3.material.io/_dsm/data/dsdb-m3/latest/TOKEN_TABLE.json"
)


async def fetch_token_tables(no_cache: bool = False) -> list[dict]:
    """Fetch the token tables from the Material API.

    Args:
        no_cache: Results are cached to disk. If no_cache is True, the
            cache is cleared first.

    Returns:
        A list of dictionaries containing the token tables.
    """
    cache_path = Path(tempfile.gettempdir()) / "c28a72b4-37c2-448b-9bbf-c143a4186ffb"
    if no_cache:
        cache_path.unlink(missing_ok=True)
    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)
    token_table_ids = list(map("".join, batched(input("TOKEN_TABLE_IDS"), 16)))
    async with httpx.AsyncClient() as client:
        url_fn = TOKEN_TABLE_URL_FORMAT.replace("json", "{}.json").format
        responses = await asyncio.gather(*map(client.get, map(url_fn, token_table_ids)))
    ret_val = [x.json() for x in responses]
    with open(cache_path, "w") as f:
        json.dump(ret_val, f)
    return ret_val


DEFAULT_CONTEXT_TERMS = {"light", "3p", "dynamic"}


def _get_tree_context_score(token_table: dict, tree: dict, terms: set[str]) -> float:
    """Returns score of a tree based on context tags.

    Raises:
        RuntimeError: The tree does not have a context defined.
    """
    if "contextTags" not in tree:
        raise RuntimeError("Tree does not have a context defined")
    resolved_tags = map(partial(_resolve_context_tag, token_table), tree["contextTags"])
    tree_tag_names = {tag["tagName"] for tag in resolved_tags}
    difference = tree_tag_names.difference(terms)
    return len(terms) - len(difference)


def _resolve_context_tag(token_table: dict, name: str) -> dict | None:
    return next(
        (
            context_tag
            for context_tag in token_table["system"]["tags"]
            if context_tag["name"] == name
        ),
        None,
    )


def _find_matching_context_tree(
    token_table: dict, trees: list[dict], terms: set[str]
) -> dict:
    """Find the contextual reference tree matching a given context.

    Args:
        trees: List of contextual reference trees.
        terms: Context tag names to match on.

    Returns:
        Highest scoring tree based on tags. If no trees define a
        context, the first one is returned.
    """
    if trees and all("contextTags" not in x for x in trees):
        return trees[0]  # no contexts defined - return first one
    score_fn = partial(_get_tree_context_score, token_table, terms=terms)
    return next(iter(sorted(trees, key=score_fn, reverse=True)), None)


@dataclass
class ParsedToken:
    """Token that was parsed."""

    name: str
    value: TokenValue


ParsedTokens = list[ParsedToken]


def parse_tokens(
    token_tables: list[dict], context_terms: set[str] | None = None
) -> ParsedTokens:
    """Parse the token tables into a list of tokens."""
    ret_val: ParsedTokens = []

    if context_terms is None:
        # Collect all context terms from the token tables. Different
        # contexts will get combined with common keys replaced by the
        # last one.
        # for context_terms in product(
        #     ["light", "dark"], ["3p", "1p"], ["dynamic", "non-dynamic"]
        # ):
        #     ret_val |= parse_tokens(token_tables, set(context_terms))
        ret_val = parse_tokens(token_tables, DEFAULT_CONTEXT_TERMS)
        return ret_val

    for token_table in token_tables:
        values = token_table["system"]["values"]
        tokens = token_table["system"]["tokens"]
        contextual_reference_trees = token_table["system"]["contextualReferenceTrees"]
        for token in tokens:
            name = token["name"]
            token_name = token.get("tokenName")
            if name not in contextual_reference_trees:
                continue
            contextual_reference_tree = contextual_reference_trees[name][
                "contextualReferenceTree"
            ]
            tree = _find_matching_context_tree(
                token_table, contextual_reference_tree, context_terms
            )
            reference_tree = tree["referenceTree"]
            while reference_tree:
                reference_value = next(
                    (v for v in values if v["name"] == reference_tree["value"]["name"]),
                    None,
                )
                if reference_value is None:
                    break
                token_value = parse_token_value(reference_value)
                if token_value is None:
                    break
                ret_val.append(ParsedToken(name=token_name, value=token_value))
                reference_tree = (
                    reference_tree["childNodes"][0]
                    if "childNodes" in reference_tree
                    else None
                )
                if reference_tree:
                    token_name = token_value
    return ret_val


def parse_token_value(reference_value: dict) -> TokenValue:
    """Parse a token value."""
    if "tokenName" in reference_value:
        return reference_value["tokenName"]
    elif "color" in reference_value:
        color_str = "#" + "".join(
            "%02x" % int(reference_value.get("color").get(c, 0) * 255)
            for c in ["red", "green", "blue"]
        )
        if reference_value["color"]["alpha"] != 1:
            color_str += "%02x" % int(255 * reference_value["value"]["alpha"])
        return color_str
    elif "length" in reference_value:
        return f"{reference_value['length'].get('value', 0)} {reference_value['length']['unit']}"
    elif "opacity" in reference_value:
        return reference_value["opacity"]
    elif "shape" in reference_value:
        return reference_value["shape"]["family"]
    elif "fontWeight" in reference_value:
        return reference_value["fontWeight"]
    elif "lineHeight" in reference_value:
        return f"{reference_value['lineHeight']['value']} {reference_value['lineHeight']['unit']}"
    elif "fontTracking" in reference_value:
        return f"{reference_value['fontTracking'].get('value', 0)} {reference_value['fontTracking']['unit']}"
    elif "fontSize" in reference_value:
        return f"{reference_value['fontSize']['value']} {reference_value['fontSize']['unit']}"
    elif "type" in reference_value:
        # Type isn't very useful as it seems to just be a
        # combination of the other font properties.
        return None
    elif "fontNames" in reference_value:
        return reference_value["fontNames"]["values"]
    elif "elevation" in reference_value:
        return f"{reference_value['elevation'].get('value', 0)} {reference_value['elevation']['unit']}"
    raise RuntimeError("unexpected reference value", reference_value)


def group_tokens_by_component(tokens: ParsedTokens) -> dict[str, ParsedTokens]:
    """Get the component groups from the tokens.

    Args:
        tokens: The parsed tokens.

    Returns:
        A dictionary mapping component group names to lists of token names.
    """
    ret_val = defaultdict(list)
    for token in tokens:
        match = re.search(r"^(md\.comp\..+?)\.", token.name)
        if match:
            group_name = match.group(1)
            ret_val[group_name].append(token)
    return ret_val


TOKENS_OUT_PATH = Path(__file__).parent / "tokens"


to_python_name = partial(re.sub, r"[-\.]", "_")
"""Convert a token name to a valid Python identifier.

    Eg, md.comp.elevated-button.container-color ->
    md_comp_elevated_button_container_color
"""


def to_var_line(token: ParsedToken) -> str:
    """Code generation for the token."""
    if isinstance(token.value, QColor):
        value = re.search("(QColor.*$", repr(token.value))[1]
    else:
        value = repr(token.value)
    return f"{to_python_name(token.name)} = {value}\n"


def generate_component_py_files(tokens: ParsedTokens) -> None:
    """Generate the Python files for the md.comp.* tokens."""
    component_groups = group_tokens_by_component(tokens)
    for group_name, tokens in component_groups.items():
        with open(TOKENS_OUT_PATH / f"{to_python_name(group_name)}.py", "w") as f:
            f.write(
                f'"""Design tokens for {group_name}."""\n'
                f"\n"
                f"# Auto generated by {Path(__file__).name}\n"
                f"# Do not edit this file directly.\n"
                f"\n"
            )
            for token in tokens:
                # Strip the group name as the file name already has the 'group'.
                token = replace(token, name=token.name[len(group_name) + 1 :])
                f.write(to_var_line(token))


def main() -> None:
    token_tables = asyncio.run(fetch_token_tables())
    tokens = parse_tokens(token_tables)
    tokens = sorted(tokens, key=lambda x: x.name)
    # token_cache_path = (
    #     Path(tempfile.gettempdir()) / "78eb23ae-4a5a-4c98-af82-62405ff0d7fb"
    # )
    # with open(token_cache_path, "w") as f:
    #     json.dump(tokens, f, indent=2)

    generate_component_py_files(tokens)


if __name__ == "__main__":
    main()
