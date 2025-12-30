from bs4 import BeautifulSoup
from helper import clean_player_name
import re
def parse_events(soup: BeautifulSoup, match_id: int) -> list[dict]:
    events = []

    for player in soup.select(".lineup .player"):
        name_el = player.select_one(".name")
        stat_el = player.select_one(".stat")

        if not name_el or not stat_el:
            continue

        player_name = name_el.get_text(strip=True)

        icon = stat_el.select_one(".ft-icon")

        if not icon:
            continue

        icon_classes = icon.get("class", [])
        event_type = next(
            (c for c in icon_classes if c != "ft-icon"),
            None
        )
        if event_type == "ball":
            event_type = "goal"

        minute = None
        text = stat_el.get_text(" ", strip=True)
        nums = re.findall(r"\d+", text)
        if nums:
            try:
                minute = int(nums[0])
            except ValueError:
                pass

        events.append({
            "match_id": match_id,
            "player_name": player_name,
            "event_type": event_type,
            "minute": minute
        })

    return events
