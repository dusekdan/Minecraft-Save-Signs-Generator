import json

SIGNS_FILE = "./signs.json"

def is_empty_sign(sign):
    """
    Determines whether sign contains empty lines only. 
    """
    return (sign["line1"].strip() == "" and sign["line2"].strip() == "" and sign["line3"].strip() == "" and sign["line4"].strip() == "")

def is_plugin_sign(sign):
    """
    Checks whether sign matches known pattern indicating it is used by a plugin.
    """
    
    # Known pattern: First line contains [private]
    firstline = sign["line1"].lower().strip()
    if firstline == "[private]" or firstline == "[more users]" or firstline == "[WebAuction+]":
        return True

    return False


with open(SIGNS_FILE, 'r') as f:
    data = json.load(f)

# Enrich sign object with category data
for sign in data:
    if is_empty_sign(sign):
        sign["category"] = "empty"
    elif is_plugin_sign(sign):
        sign["category"] = "plugin-related"
    else:
        sign["category"] = "nonempty"

with open(SIGNS_FILE, 'w') as f:
    json.dump(data, f)