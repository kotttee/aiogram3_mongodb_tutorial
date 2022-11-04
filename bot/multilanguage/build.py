from fluentogram import FluentTranslator, TranslatorHub
from fluent_compiler.bundle import FluentBundle
from bot.configuration import Configuration


async def build_translator_hub() -> TranslatorHub:
    translations = []
    for lang_code in Configuration.available_languages():
        translations.append(FluentTranslator(lang_code,
                                             translator=FluentBundle.from_files(lang_code, filenames=[f"translations/{lang_code}.ftl"])))
    lang_codes_dict = {}
    lang_codes_list = Configuration.available_languages()

    # ['en', 'uk', 'ru'] -> {'en': ('en', 'uk', 'ru'), 'uk': ('uk', 'ru'), 'ru': ('ru',)}
    for lang in Configuration.available_languages():
        lang_codes_dict[lang] = tuple(lang_codes_list)
        lang_codes_list.remove(lang)

    return TranslatorHub(
        {code: lang_codes_dict[code] for code in Configuration.available_languages()},
        translations
    )