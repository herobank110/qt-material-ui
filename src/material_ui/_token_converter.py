from dataclasses import dataclass
from functools import partial
import json
from pathlib import Path


SELECTED_CONTEXT = {"light", "3p", "dynamic"}

with open(Path(__file__).parent / "TOKEN_TABLE_2.json") as f:
    token_table = json.load(f)

values = token_table["system"]["values"]
tokens = token_table["system"]["tokens"]
contextual_reference_trees = token_table["system"]["contextualReferenceTrees"]


def _get_tree_context_score(tree: dict, terms: set[str]) -> float:
    """Returns score of a tree based on context tags.

    Raises:
        RuntimeError: The tree does not have a context defined.
    """
    if "contextTags" not in tree:
        raise RuntimeError("Tree does not have a context defined")
    resolved_tags = map(_resolve_context_tag, tree["contextTags"])
    tree_tag_names = {tag["tagName"] for tag in resolved_tags}
    difference = tree_tag_names.difference(terms)
    return len(terms) - len(difference)


def _resolve_context_tag(name: str) -> dict | None:
    return next(
        (
            context_tag
            for context_tag in token_table["system"]["tags"]
            if context_tag["name"] == name
        ),
        None,
    )


def _find_matching_context_tree(trees: list[dict], terms: set[str]) -> dict:
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
    score_fn = partial(_get_tree_context_score, terms=terms)
    return next(iter(sorted(trees, key=score_fn, reverse=True)), None)


for token in tokens:
    name = token["name"]
    token_name = token.get("tokenName")
    if name not in contextual_reference_trees:
        continue
    print(token_name)
    contextual_reference_tree = contextual_reference_trees[name][
        "contextualReferenceTree"
    ]
    tree = _find_matching_context_tree(contextual_reference_tree, SELECTED_CONTEXT)
    indent = 1

    def output(value):
        print("  " * indent + str(value))

    reference_tree = tree["referenceTree"]
    while reference_tree:
        reference_value = next(
            v for v in values if v["name"] == reference_tree["value"]["name"]
        )
        if "tokenName" in reference_value:
            output(reference_value["tokenName"])
        elif "color" in reference_value:
            color_str = "#" + "".join(
                "%02x" % int(reference_value.get("color").get(c, 0) * 255)
                for c in ["red", "green", "blue"]
            )
            if reference_value["color"]["alpha"] != 1:
                color_str += "%02x" % int(255 * reference_tree["value"]["alpha"])
            output(color_str)
        elif "length" in reference_value:
            output(
                f"{reference_value['length']['value']} {reference_value['length']['unit']}"
            )
        elif "opacity" in reference_value:
            output(reference_value["opacity"])
        elif "shape" in reference_value:
            output(reference_value["shape"]["family"])
        reference_tree = (
            reference_tree["childNodes"][0] if "childNodes" in reference_tree else None
        )
        indent += 1
