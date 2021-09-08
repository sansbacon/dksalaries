from dksalaries import Scraper, Parser
import cattr
import pandas as pd


def run():
    s = Scraper()
    p = Parser()

    # get the draft group of the main slate
    gcd = p.getcontests(s.getcontests(sport='NFL'))
    draft_group_id, game_set_key = gcd.find_main_slate()

    # download the player data
    # from main slate draftables
    ddoc = p.draftables(s.draftables(draft_group_id))
    salaries = ddoc.player_salaries()
    print(pd.DataFrame([cattr.unstructure(s) for s in salaries]).drop_duplicates(subset=['player_id', 'player_dk_id']))    


if __name__ == '__main__':
    run()
