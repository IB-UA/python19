import re

UKR_CYRILLIC_SYMBOLS = (
    'а',    'б',    'в',    'г',    'ґ',    'д',    'е',    'є',    'ж',    'з',    'и',    'і',    'ї',    'й',    'к',
    'л',    'м',    'н',    'о',    'п',    'р',    'с',    'т',    'у',    'ф',    'х',    'ц',    'ч',    'ш',
    'щ',    'ь',    'ю',    'я',
    'Є',    'Ї',    'Й',    'Ю',    'Я'  # set of symbols that has other transliteration in case they start the word
)

UKR_CYRILLIC_SYMBOLS_TRANSLITERATION = (
    'a',    'b',    'v',    'h',    'g',    'd',    'e',    'ie',   'zh',   'z',    'y',    'i',    'i',    'i',    'k',
    'l',    'm',    'n',    'o',    'p',    'r',    's',    't',    'u',    'f',    'kh',   'ts',   'ch',   'sh',
    'shch', '',     'iu',   'ia',
    'Ye',   'Yi',   'Y',    'Yu',   'Ya'
)

TRANS = dict()

for cyrillic, latin in zip(UKR_CYRILLIC_SYMBOLS, UKR_CYRILLIC_SYMBOLS_TRANSLITERATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.capitalize()


def normalize(name: str) -> str:
    translate_name = re.sub(r'[^a-zA-Z0-9_]', '_', name.translate(TRANS))
    return translate_name
