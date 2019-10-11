from workflow import Workflow, web
from datetime import date, timedelta, datetime
from pytz import timezone
from tzlocal import get_localzone
import sys


def get_yesterday_games():
    """
    :return: A list of dictionaries representing the games of yesterday.
    """
    yesterday = (date.today() - timedelta(1)).strftime("%Y%m%d")
    req = web.get("http://data.nba.net/json/cms/noseason/scoreboard/{}/games.json".format(yesterday))
    req.raise_for_status()
    games = req.json()["sports_content"]["games"]["game"]
    return games


def main(wf):
    games = get_yesterday_games()

    for game in games:
        title = "{} {} @ {} {}".format(game["visitor"]["city"], game["visitor"]["nickname"], game["home"]["city"], game["home"]["nickname"])
        game_date = datetime.strptime(game["date"] + game["time"], "%Y%m%d%H%M")
        game_date = timezone("US/Eastern").localize(game_date).astimezone(get_localzone())  # Convert to local timezone.
        wf.add_item(title=title, subtitle=game_date.strftime("%H:%M"), arg=game["game_url"], valid=True)

    if not games:
        wf.add_item(title="No Games Yesterday :(", valid=False)
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
