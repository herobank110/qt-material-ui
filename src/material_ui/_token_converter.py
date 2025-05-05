from dataclasses import dataclass
from functools import partial
from itertools import batched, product
import json
from pathlib import Path

import tempfile
import httpx
import asyncio


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


ParsedTokens = dict[str, str]


def parse_tokens(token_tables: list[dict], context_terms: set[str]) -> ParsedTokens:
    """Parse the token tables into a list of tokens."""
    ret_val: ParsedTokens = {}
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
                if "tokenName" in reference_value:
                    ret_val[token_name] = reference_value["tokenName"]
                elif "color" in reference_value:
                    color_str = "#" + "".join(
                        "%02x" % int(reference_value.get("color").get(c, 0) * 255)
                        for c in ["red", "green", "blue"]
                    )
                    if reference_value["color"]["alpha"] != 1:
                        color_str += "%02x" % int(
                            255 * reference_tree["value"]["alpha"]
                        )
                    ret_val[token_name] = color_str
                elif "length" in reference_value:
                    ret_val[token_name] = (
                        f"{reference_value['length'].get('value', 0)} {reference_value['length']['unit']}"
                    )
                elif "opacity" in reference_value:
                    ret_val[token_name] = reference_value["opacity"]
                elif "shape" in reference_value:
                    ret_val[token_name] = reference_value["shape"]["family"]
                elif "fontWeight" in reference_value:
                    ret_val[token_name] = reference_value["fontWeight"]
                elif "lineHeight" in reference_value:
                    ret_val[token_name] = (
                        f"{reference_value['lineHeight']['value']} {reference_value['lineHeight']['unit']}"
                    )
                elif "fontTracking" in reference_value:
                    ret_val[token_name] = (
                        f"{reference_value['fontTracking'].get('value', 0)} {reference_value['fontTracking']['unit']}"
                    )
                elif "fontSize" in reference_value:
                    ret_val[token_name] = (
                        f"{reference_value['fontSize']['value']} {reference_value['fontSize']['unit']}"
                    )
                elif "type" in reference_value:
                    ret_val[token_name] = reference_value["type"]
                    break
                elif "fontNames" in reference_value:
                    ret_val[token_name] = reference_value["fontNames"]["values"]
                elif "elevation" in reference_value:
                    ret_val[token_name] = (
                        f"{reference_value['elevation'].get('value', 0)} {reference_value['elevation']['unit']}"
                    )
                else:
                    raise RuntimeError("unexpected reference value", reference_value)
                reference_tree = (
                    reference_tree["childNodes"][0]
                    if "childNodes" in reference_tree
                    else None
                )
                token_name = ret_val[token_name]
    return ret_val


def main() -> None:
    token_tables = asyncio.run(fetch_token_tables())
    tokens = {}
    for context_terms in product(
        ["light", "dark"], ["3p", "1p"], ["dynamic", "non-dynamic"]
    ):
        tokens |= parse_tokens(token_tables, set(context_terms))
    tokens |= parse_tokens(token_tables, DEFAULT_CONTEXT_TERMS)
    print(tokens)


if __name__ == "__main__":
    main()
