from typing import Literal

from locales import ru, uk
import logging

logger = logging.getLogger("localizer")
DEFAULT_LANGUAGE = "ru"


class Localizer:
    def __new__(cls, curr_lang: str | None = None):
        if not hasattr(cls, "instance"):
            cls.instance = super(Localizer, cls).__new__(cls)
            cls.instance.languages = {
                "ru": ru,
                "uk": uk,
            }
            cls.instance.current_language = DEFAULT_LANGUAGE
        if curr_lang in cls.instance.languages:
            cls.instance.current_language = curr_lang
        return cls.instance

    def translate(self, variable_name: str, *args, language: str | None = None):
        text = variable_name
        selected_language = language if language in self.languages else self.current_language
        for lang_name in (selected_language, DEFAULT_LANGUAGE, "uk"):
            lang = self.languages.get(lang_name)
            if lang and hasattr(lang, variable_name):
                text = getattr(lang, variable_name)
                break

        args = list(args)
        formats = text.count("{}")
        if len(args) < formats:
            args.extend(["{}"] * (formats - len(args)))
        try:
            return text.format(*args)
        except:
            logger.debug("TRACEBACK", exc_info=True)
            return text

    def add_translation(self, uuid: str, variable_name: str, value: str, language: Literal["ru", "uk"] = DEFAULT_LANGUAGE):
        if language not in self.languages:
            language = DEFAULT_LANGUAGE
        setattr(self.languages[language], f"{uuid}_{variable_name}", value)

    def plugin_translate(self, uuid: str, variable_name: str, *args, language: str | None = None):
        s = f"{uuid}_{variable_name}"
        result = self.translate(s, *args, language=language)
        if result != s:
            return result
        return self.translate(variable_name, *args, language=language)
