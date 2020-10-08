from datetime import datetime


import localizations.localization as lc
import api_requests as ar


def pretty_date(ugly_date) -> str:
    date = datetime.utcfromtimestamp(ugly_date)
    return date.strftime("%d.%m %H:%M")


def get_measure_list(manager_uid: int, companies_list: list) -> list:
    ans = []

    for company in companies_list:
        workers_stats = ar.get_workers_stats(manager_uid, company)

        for stat in workers_stats:
            if stat["last_temp"] is not None:
                measure_date = datetime.utcfromtimestamp(stat["date"]).strftime("%d.%m")
                current_date = datetime.today().strftime("%d.%m")
                if current_date != measure_date:
                    ans.append(stat)
            else:
                ans.append(stat)

    return ans


def get_key_from_stats(worker_stats: dict) -> float:
    if "date" in worker_stats:
        measure_date = datetime.utcfromtimestamp(worker_stats["date"]).strftime("%d.%m")
        current_date = datetime.today().strftime("%d.%m")
        if current_date == measure_date:
            return worker_stats["last_temp"]
        else:
            return 1.
    else:
        return 0.


def get_temp_stats(manager_uid: int, companies_list: list, lang: str) -> list:
    ans = ""
    flg = False

    first_block = []
    second_block = []
    third_block = []

    for company_guid in companies_list:
        workers_stats = ar.get_workers_stats(manager_uid, company_guid)

        for stat in workers_stats:
            if stat["last_temp"] is not None:
                measure_date = datetime.utcfromtimestamp(stat["date"]).strftime("%d.%m")
                current_date = datetime.today().strftime("%d.%m")
                if current_date == measure_date:
                    if stat["last_temp"] >= 37:
                        first_block.append(stat)
                    else:
                        second_block.append(stat)
                else:
                    third_block.append(stat)
            else:
                third_block.append(stat)

    first_block = sorted(first_block, key=get_key_from_stats, reverse=True)
    second_block = sorted(second_block, key=get_key_from_stats, reverse=True)
    third_block = sorted(third_block, key=get_key_from_stats, reverse=True)

    if len(first_block) != 0:
        ans += lc.translate(lang, "have_temp")
        for stat in first_block:
            ans += "\u2757\ufe0f\t_%s_\t\t*%s*\t\t%s\n" % (stat["initials"], str(stat["last_temp"]), pretty_date(stat["date"]))
        ans += "\\_" * 40 + "\n\n"

    if len(second_block) != 0:
        ans += lc.translate(lang, "no_temp")
        for stat in second_block:
            ans += "\u2705\t_%s_\t\t*%s*\t\t%s\n" % (stat["initials"], str(stat["last_temp"]), pretty_date(stat["date"]))
        ans += "\n"

    if len(third_block) != 0:
        flg = True
        ans += lc.translate(lang, "no_measurement")
        for stat in third_block:
            ans += "\u26a0\ufe0f\t_%s_" % (stat["initials"])
            if "date" in stat:
                ans += "\t\t*%s*\t\t%s\t\t%s\n" % (str(stat["last_temp"]), lc.translate(lang, "last_measurement"), pretty_date(stat["date"]))
            else:
                ans += "\t\t%s" % lc.translate(lang, "no_data")

        ans += "\n"

    if ans == "":
        return [lc.translate(lang, "no_employees"), False]

    ans += "%s\t\t%s." % (lc.translate(lang, "stats_message"), datetime.now().strftime('%d.%m.%Y %H:%M'))

    return [ans, flg]
