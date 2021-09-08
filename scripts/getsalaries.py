from dksalaries import Scraper, Parser
from dksalaries.documents import GetContestsDocument


def run():
    s = Scraper()
    p = Parser()
    ms = None

    gcd = p.getcontests(s.getcontests(sport='NFL'))
    for cs in gcd.classic_slates:
        if cs.is_main_slate:
            ms = cs
            break

    if ms:
        print(ms)   
    

if __name__ == '__main__':
    run()
