from bs4 import BeautifulSoup
from helper import first_text

def parse_additional_stats(soup: BeautifulSoup, match_id: int) -> list[dict]:
    stats = []

    table = soup.select_one(".cell-dividers")
    if not table:
        return stats

    rows = table.select("tbody tr") or table.select("tr")
    for r in rows:
        cols = [c.get_text(strip=True) for c in r.find_all("td")]
        if len(cols) != 5   :
            continue

        time, team, player, stat, value = cols
        try:
            value = int(value)
        except ValueError:
            pass
        stats.append({
            "match_id": match_id,
            "team": team,
            "player_name": player,
            "stat": stat,
            "value": value
        })

    return stats
