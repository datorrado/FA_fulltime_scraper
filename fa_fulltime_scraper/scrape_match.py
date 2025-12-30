from fetch import fetch_html
from parse_lineups import parse_lineups_and_subs
from parse_stats import parse_additional_stats
from parse_match import parse_match_meta
from parse_events import parse_events

def scrape_match(url: str) -> dict:
    soup = fetch_html(url)

    match = parse_match_meta(soup)
    match_id = match["match_id"]

    return {
        "match": match,
        "lineups": parse_lineups_and_subs(soup, match_id),
        "events": parse_events(soup, match_id),
        "additional_stats": parse_additional_stats(soup, match_id),
    }