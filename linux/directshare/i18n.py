# SPDX-FileCopyrightText: 2026 5wHN28Dg
# SPDX-License-Identifier: GPL-3.0-or-later


"""
Internationalization (i18n) setup for Direct Share.

Responsibilities:
- Configure gettext domain and locale directory
- Discover available translations at runtime
- Provide mapping of localized language names → language codes

Assumptions:
- Translations are stored under ../po/<lang>/LC_MESSAGES/direct-share.mo
"""

import gettext
from pathlib import Path

_localedir = Path(__file__).parent.parent / "po"
gettext.bindtextdomain("direct-share", _localedir)
gettext.textdomain("direct-share")


def get_available_languages():
    languages = {"English": "en"}
    for lang_dir in _localedir.iterdir():
        mo_file = lang_dir / "LC_MESSAGES" / "direct-share.mo"
        if mo_file.exists():
            lang_code = lang_dir.name
            translation = gettext.translation(
                "direct-share", _localedir, languages=[lang_code]
            )
            # Get localized language name
            languages[translation.gettext(lang_code)] = lang_code
    return languages  # {"English": "en", "العربية": "ar"}


RTL_LANGUAGES = {"ar", "he", "fa", "ur", "yi"}
