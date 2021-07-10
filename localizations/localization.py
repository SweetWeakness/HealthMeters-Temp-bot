from localizations import russian

localization = {
    "ru": russian.all_text
}


def translate(language: str, method: str) -> str:
    return localization[language][method]
