from bs4 import BeautifulSoup
from helper import first_text, clean_player_name
import re

def detect_team_side(block):
    grid = block.find_parent("div", class_="lineup-statistics-grid")
    if not grid:
        return None

    home = grid.select_one(".home-team")
    away = grid.select_one(".road-team")

    if home and home in block.parents:
        return "home"
    if away and away in block.parents:
        return "away"

    return None
def parse_lineups_and_subs(soup: BeautifulSoup, match_id) -> list[dict]:
    
    records = []

    grid = soup.select_one(".lineup-statistics-grid")
    if not grid:
        return records

    for team_side, selector in {
        "home": ".home-team",
        "away": ".road-team"
    }.items():

        team_block = grid.select_one(selector)
        if not team_block:
            continue

        # titulares y suplentes
        for section, is_starting in {
            "lineup": True,
            "subs": False
        }.items():

            players = team_block.select(f".{section} div.player, .{section} li")
            for p in players:
                name = p.get_text("", strip=True)
                name = re.sub(r"\d+", "", name).strip()
                if not name:
                    continue

                # Extraer nombre del equipo del match_id según el formato: "FECHA_H:HOME_A:AWAY"
                if team_side == "home":
                    team = match_id.split("_H:")[1].split("_A:")[0].replace("_", " ")
                else:  # away
                    team = match_id.split("_A:")[1].replace("_", " ")

                records.append({
                    "match_id": match_id,
                    "team_side": team_side,
                    "team": team,
                    "player_name": name,
                    "name": name.split(" ")[0],
                    "last_name": " ".join(name.split(" ")[1:]),
                    "is_starting": is_starting
                })

    return records

    """ Otra versión alternativa   
    records = [] 

    for side in ["home", "road"]:
        team_block = soup.select_one(f".{side}-team")
        if not team_block:
            continue

        # Titulares
        for p in team_block.select(".starters .lineup p"):
            records.append({
                "match_id": match_id,
                "team_side": side,
                "player_name": clean_player_name(p),
                "is_starting": True
            })

        # Suplentes
        for p in team_block.select(".subs .lineup p"):
            records.append({
                "match_id": match_id,
                "team_side": side,
                "player_name": clean_player_name(p),
                "is_starting": False
            })

    return records

    """
