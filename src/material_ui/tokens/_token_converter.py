from collections import defaultdict
from dataclasses import dataclass, replace
from functools import partial
from itertools import batched, product
import json
from pathlib import Path

import re
import tempfile
from typing import Callable
import httpx
import asyncio
from qtpy.QtGui import QColor

from material_ui.tokens._utils import TokenValue, to_python_name


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


def get_tree_context_score(token_table: dict, tree: dict, terms: set[str]) -> float:
    """Returns score of a tree based on context tags.

    Raises:
        RuntimeError: The tree does not have a context defined.
    """
    if "contextTags" not in tree:
        raise RuntimeError("Tree does not have a context defined")
    resolved_tags = map(partial(resolve_context_tag, token_table), tree["contextTags"])
    tree_tag_names = {tag["tagName"] for tag in resolved_tags}
    difference = tree_tag_names.difference(terms)
    return len(terms) - len(difference)


def resolve_context_tag(token_table: dict, name: str) -> dict | None:
    return next(
        (
            context_tag
            for context_tag in token_table["system"]["tags"]
            if context_tag["name"] == name
        ),
        None,
    )


def find_matching_ref_tree(
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
    score_fn = partial(get_tree_context_score, token_table, terms=terms)
    return next(iter(sorted(trees, key=score_fn, reverse=True)), None)


@dataclass
class ParsedToken:
    """Token that was parsed."""

    name: str
    value: TokenValue


ParsedTokens = list[ParsedToken]


def merge_parsed_tokens(list_a: ParsedTokens, list_b: ParsedTokens) -> ParsedTokens:
    """Update the first list with the second one."""
    list_b_token_names = {x.name for x in list_b}
    return list_b + [x for x in list_a if x.name not in list_b_token_names]


def parse_tokens(
    token_tables: list[dict], context_terms: set[str] | None = None
) -> ParsedTokens:
    """Parse the token tables into a merged list of tokens.

    Args:
        token_tables: The token tables to parse.
        context_terms: The context terms to use. If None, all contexts
            are merged together, ending with the default context.

    Returns:
        A list of parsed tokens.
    """
    ret_val: ParsedTokens = []

    # Recursive entry point to merge all contexts.
    if context_terms is None:
        # Collect all context terms from the token tables. Different
        # contexts will get combined with common keys replaced by the
        # last one.
        for context_terms in product(
            ["light", "dark"], ["3p", "1p"], ["dynamic", "non-dynamic"]
        ):
            ret_val = merge_parsed_tokens(
                ret_val, parse_tokens(token_tables, set(context_terms))
            )
        ret_val = merge_parsed_tokens(
            ret_val, parse_tokens(token_tables, DEFAULT_CONTEXT_TERMS)
        )
        return ret_val

    # A specific context.
    for token_table in token_tables:
        ret_val = merge_parsed_tokens(
            ret_val, parse_tokens_in_table(token_table, context_terms)
        )
    return ret_val


def parse_tokens_in_table(token_table: dict, context_terms: set[str]) -> ParsedTokens:
    ret_val: ParsedTokens = []
    tokens = token_table["system"]["tokens"]
    ref_trees = token_table["system"]["contextualReferenceTrees"]
    for token in tokens:
        name = token["name"]
        if name not in ref_trees:
            # Some tokens don't seem to have a reference tree.
            continue
        named_ref_tree = ref_trees[name]["contextualReferenceTree"]
        ref_tree = find_matching_ref_tree(token_table, named_ref_tree, context_terms)[
            "referenceTree"
        ]
        token_name = token["tokenName"]
        # Traverse the recursive tree structure to build a flat list.
        while True:
            reference_value = resolve_value(token_table, ref_tree)
            if reference_value is None:
                # Unable to resolve value - skip.
                break
            token_value = parse_token_value(reference_value)
            if token_value is None:
                # Reached an unsupported value - skip.
                break
            if any(x.name == token_name for x in ret_val):
                # Token already added - skip.
                # If an indirection, children will be the same too.
                break
            ret_val.append(ParsedToken(name=token_name, value=token_value))
            if "childNodes" in ref_tree:
                # Next iteration to go deeper.
                ref_tree = ref_tree["childNodes"][0]
                token_name = token_value
            else:
                # End of the chain.
                break
    return ret_val


def resolve_value(token_table: dict, reference_tree: dict) -> dict | None:
    """Resolve a value"""
    values = token_table["system"]["values"]
    return next(
        (x for x in values if x["name"] == reference_tree["value"]["name"]),
        None,
    )


def parse_token_value(value: dict) -> TokenValue | None:
    """Parse a token value from the token table.

    Args:
        value: The token value.

    Returns:
        The token value if a supported type, otherwise None.

    Raises:
        RuntimeError: Unexpected type of token.
    """

    def without_unit(unit_name: str) -> Callable[[dict], TokenValue]:
        def inner(value: dict) -> TokenValue:
            assert value["unit"] == unit_name
            return value.get("value", 0)

        return inner

    supported_values_transformations = {
        "tokenName": str,
        "color": lambda x: QColor.fromRgbF(
            x.get("red", 0.0),
            x.get("green", 0.0),
            x.get("blue", 0.0),
            x.get("alpha", 1.0),
        ),
        "length": lambda x: {
            # DIPS as int, PERCENT as float
            "PERCENT": x.get("value", 0) / 100,
            "DIPS": x.get("value", 0),
        }[x["unit"]],
        "opacity": float,
        "shape": lambda x: x["family"],
        "fontWeight": int,
        "lineHeight": without_unit("POINTS"),
        "fontTracking": without_unit("POINTS"),
        "fontSize": without_unit("POINTS"),
        "type": lambda _: None,  # unsupported type
        "fontNames": lambda x: x["values"][0],
        "elevation": without_unit("DIPS"),
    }
    for key, transform_fn in supported_values_transformations.items():
        inner_value = value.get(key)
        if inner_value is not None:
            return transform_fn(inner_value)
    raise RuntimeError("unexpected reference value", value)


def group_tokens_by_output_files(tokens: ParsedTokens) -> dict[str, ParsedTokens]:
    """Get the groups by first 3 parts from the tokens.

    Args:
        tokens: The parsed tokens.

    Returns:
        A dictionary mapping component group names to lists of token names.
    """
    ret_val = defaultdict(list)
    for token in tokens:
        match = re.search(r"^(md\.(comp|sys|ref)\..+?)\.", token.name)
        if match:
            group_name = match.group(1)
            ret_val[group_name].append(token)
    return ret_val


TOKENS_OUT_PATH = Path(__file__).parent


def to_var_line(token: ParsedToken) -> str:
    """Code generation for the token."""
    if isinstance(token.value, QColor):
        value = re.search("(QColor.*)$", repr(token.value))[1]
    else:
        value = repr(token.value)
    return f"{to_python_name(token.name)} = _define_token({value})\n"


def generate_py_files(tokens: ParsedTokens) -> None:
    """Generate the Python files for the tokens."""
    component_groups = group_tokens_by_output_files(tokens)
    for group_name, tokens in component_groups.items():
        if group_name == "md.ref.palette":
            # Skip this as the parsing leaves incomplete tokens. Better
            # to write this file manually.
            continue
        with open(TOKENS_OUT_PATH / f"{to_python_name(group_name)}.py", "w") as f:
            f.write(
                f'"""Design tokens for {group_name}."""\n'
                f"\n"
                f"# Auto generated by {Path(__file__).name}\n"
                f"# Do not edit this file directly.\n"
                f"\n"
                f"from material_ui.tokens._utils import define_token as _define_token\n"
                f"\n"
                f"\n"
            )
            for token in tokens:
                # Strip the group name as the file name already has the 'group'.
                token = replace(token, name=token.name[len(group_name) + 1 :])
                f.write(to_var_line(token))


def main() -> None:
    token_tables = asyncio.run(fetch_token_tables())
    tokens = parse_tokens(token_tables)
    # Sort so the files look neater.
    tokens = sorted(tokens, key=lambda x: x.name)
    generate_py_files(tokens)


if __name__ == "__main__":
    main()
