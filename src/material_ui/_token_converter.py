import json
from pathlib import Path

with open(Path(__file__).parent / "TOKEN_TABLE_2.json") as f:
    token_table = json.load(f)

values = token_table['system']['values']
tokens = token_table['system']['tokens']
contextual_reference_trees = token_table['system']['contextualReferenceTrees']
# contextual_reference_trees = tokens['system']['contextualReferenceTrees']

for token in tokens:
    name = token['name']
    token_name = token.get('tokenName')
    # contextual_reference_key = re.search(r"^(designSystems/\w+/tokenSets/\w+/tokens/\w+)/.*", name)[1]
    # if contextual_reference_key not in contextual_reference_trees:
    #     continue
    # contextual_reference_tree = contextual_reference_trees[contextual_reference_key]['contextualReferenceTree']
    if name not in contextual_reference_trees:
        continue
    print(token_name)
    contextual_reference_tree = contextual_reference_trees[name]['contextualReferenceTree']
    for tree_item in contextual_reference_tree:
        indent = 1
        def output(value):
            print("  " * indent + str(value))
        if 'contextTags' in tree_item:
            context_tags = tree_item['contextTags']
            resolved_context_tags = [
                next(
                    tag
                    for tag in token_table["system"]["tags"]
                    if tag["name"] == context_tag
                )
                for context_tag in context_tags
            ]
            output("context(" + ", ".join(tag['tagName'] for tag in resolved_context_tags) + ")")
            indent += 1
        reference_tree = tree_item['referenceTree']
        while reference_tree:
            reference_value = next(v for v in values if v['name'] == reference_tree['value']['name'])
            if 'tokenName' in reference_value:
                output(reference_value['tokenName'])
            elif 'color' in reference_value:
                color_str = "#" + "".join("%02x" % int(reference_value.get("color").get(c, 0) * 255) for c in ['red', 'green', 'blue'])
                if reference_value['color']['alpha'] != 1:
                    color_str += "%02x" % int(255 * reference_tree['value']['alpha'])
                output(color_str)
                # output(reference_value["color"])
            elif 'length' in reference_value:
                output(f"{reference_value["length"]["value"]} {reference_value["length"]["unit"]}")
            elif 'opacity' in reference_value:
                output(reference_value["opacity"])
            elif 'shape' in reference_value:
                output(reference_value["shape"]['family'])
            reference_tree = reference_tree['childNodes'][0] if 'childNodes' in reference_tree else None
            indent += 1
