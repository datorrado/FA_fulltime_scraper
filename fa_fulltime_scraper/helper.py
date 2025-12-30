def first_text(parent, selectors):
    """
    returns text from the first selector that matches 
    """

    for sel in selectors:
        el = parent.select_one(sel)
        if el:
            return el.get_text(strip=True)
        
    return None

def clean_player_name(p):
    """
    Returns only the player's name,
    ignoring spans of events/minutes
    """
    return "".join(
        t for t in p.find_all(string=True, recursive=False)
    ).strip()