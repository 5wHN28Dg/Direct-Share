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

Implementation note:
    Runtime language switching in GTK/libadwaita is not officially supported.
    glibc's gettext reads the LANGUAGE environment variable lazily — on the
    first translation lookup per domain, it loads the matching catalog into
    memory and caches it. Subsequent lookups serve from cache regardless of
    environment variable changes, making naive runtime switching unreliable.

    Python's gettext module exposes enough API to invalidate its own cache
    (via bindtextdomain()), which is why Direct Share's own strings switch
    cleanly. libadwaita's internal domain ("libadwaita") has no Python-level
    handle, so its cache persists after the first lookup — causing built-in
    strings to switch to a new language but never revert.

    The fix is to call the C-level bindtextdomain() and textdomain() directly
    via ctypes for libadwaita domain after changing LANGUAGE. This triggers glibc
    to re-evaluate which catalog to serve on the next lookup, effectively
    invalidating the cache. This relies on an implementation detail of glibc's
    caching behavior and is not a guaranteed public API.
"""

import ctypes
import ctypes.util
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

libc = ctypes.CDLL(ctypes.util.find_library("c"))

libc.bindtextdomain.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
libc.bindtextdomain.restype = ctypes.c_char_p

libc.textdomain.argtypes = [ctypes.c_char_p]
libc.textdomain.restype = ctypes.c_char_p


def invalidate_gettext_cache(domain: str, locale_dir: str) -> None:
    if not libc.bindtextdomain(domain.encode(), locale_dir.encode()):
        raise RuntimeError("bindtextdomain failed")

    libc.textdomain(domain.encode())
