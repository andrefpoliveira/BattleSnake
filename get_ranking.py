from requests_html import HTMLSession
from bs4 import BeautifulSoup

base_link = "https://play.battlesnake.com"

def get_snake_rank(snake_name: str, soup: BeautifulSoup):
    """ Parses the html page to get the ranking on the category """

    snake_row = soup.find_all('tr', {'class': 'ladder-row', 'data-snake-name': snake_name, 'data-author-name': 'andrefpoliveira'})
    if len(snake_row) == 0: return None

    ranking = int(snake_row[0].find_all('td', {'class': 'arena-leaderboard-rank'})[0].text.strip())
    return ranking

def get_idx_of_line(lines, match, after_line = 0):
    for idx, line in enumerate(lines):
        if idx < after_line: continue
        if match == line.strip(): return idx
    return None

def find_current_result(arena: str, results: dict):
    for k in results:
        if k in arena:
            return k, results[k][0], results[k][1]
    return None, None, None

session = HTMLSession()
r = session.get("https://play.battlesnake.com/arena/global/")
soup = BeautifulSoup(r.text, features="html.parser")

arenas_ul = soup.find_all('ul', {'class': 'arena-dropdown-list'})[0]
arenas = [(x["href"], x.text) for x in arenas_ul.find_all('a')]

results = {}
for url, arena in arenas:
    r = session.get(base_link + url)
    soup = BeautifulSoup(r.text, features="html.parser")
    trs = soup.find_all('tr', {'class': 'ladder-row'})
    results[arena] = (get_snake_rank("KoalaSnake2", soup), len(trs))

with open("README.md") as f:
    lines = f.readlines()

ranking_line = get_idx_of_line(lines, "## Ranking (Updated once a day)")
end_of_table = get_idx_of_line(lines, "", ranking_line)
for i in range(ranking_line+3, end_of_table):
    _, arena, _, best_rank, _, _ = lines[i].split("|")
    arena_name, arena_result, total_players = find_current_result(arena.strip(), results)
    
    if arena_name != None:
        lines[i] = f"| {arena_name} | {arena_result} | {arena_result if arena_result < int(best_rank.strip()) else best_rank.strip()} | {total_players} |\n"
        del results[arena_name]

counter = 0
for k in results:
    if results[k][0] != None:
        lines.insert(end_of_table + counter, f"| {k} | {results[k][0]} | {results[k][0]} | {results[k][1]} |\n")
        counter += 1

with open("README.md", "w") as f:
    for l in lines:
        f.write(l)