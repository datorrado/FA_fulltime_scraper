from bs4 import BeautifulSoup
from helper import first_text

import re

def parse_score(container):
    """
    Extrae marcador desde el bloque fixture-teams-and-score.
    Devuelve (home_goals, away_goals) o (None, None)
    """
    score_box = container.select_one("div.score.played") or container.select_one("div.score")
    if not score_box:
        return None, None

    # Tomamos TODO el texto visible del score
    text = score_box.get_text(" ", strip=True)

    # Ejemplo de text:
    # "FT 1 2"
    # "1 2"
    # "FT 0 0"

    numbers = [int(n) for n in re.findall(r"\b\d+\b", text)]

    if len(numbers) >= 2:
        return numbers[0], numbers[1]

    return None, None
def parse_match_meta(soup: BeautifulSoup) -> dict:
    match = {}

    container = soup.select_one("div.fixture-teams-and-score")
    if not container:
        raise ValueError("Did not find the fixture")
    
    match["home_team"] = first_text(container, [
        ".home-team .team-name h2"
    ])

    match["away_team"] = first_text(container, [
        ".road-team .team-name h2"
    ])

    #score
    container = soup.select_one("div.fixture-teams-and-score")

    home_goals, away_goals = parse_score(container)

    match["home_goals"] = home_goals
    match["away_goals"] = away_goals
    
    dt_box = soup.select_one("div.fixture-date-time")
    if dt_box:
        parts = list(dt_box.stripped_strings)
        match["date"] = parts[0]
        match["time"] = parts[1]
        match["venue"] = "".join(parts[2:])
    else:
        match["date"] = match["time"] = match["venue"] = None
    
    header_texts = [" ".join(e.stripped_strings) for e in soup.select(".ft-container div")]
    match["competition"] = next((t for t in header_texts if "LEAGUE" in t.upper()), None)
    match["round"] = next((t for t in header_texts if "ROUND" in t.upper()), None)

    # --- match_id generado ---
    home_team_normalized = match['home_team'].replace(" ", "_") if match['home_team'] else ""
    away_team_normalized = match['away_team'].replace(" ", "_") if match['away_team'] else ""
    key = f"{match['date']}_H:{home_team_normalized}_A:{away_team_normalized}"
    match["match_id"] = key

    return match