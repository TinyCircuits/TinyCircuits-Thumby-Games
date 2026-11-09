# Sraosha Vanish - standalone MicroPython script.
# Install this file, catalog_text.dat and packaged BINs in /Games/SraoshaVanish/.
import gc
import time
import thumby

# Update this single value for each release; title and logs share it.
VERSION = "v0.11.1"

_base = "/Games/SraoshaVanish"
_cache = []
_fallback = None
_fallback_checked = False
_CACHE_LIMIT = 5


def clear_cache():
    global _fallback, _fallback_checked
    del _cache[:]
    _fallback = None
    _fallback_checked = False


def set_asset_directory(directory):
    global _base
    clear_cache()
    _base = directory


def _load(path, width, height):
    # Only one screen-sized frame may be allocated. BMP is not raw VLSB.
    if width < 1 or height < 1 or width > 72 or height > 40:
        raise ValueError("Invalid sprite dimensions")
    if path.endswith(".bmp"):
        path = path[:-4] + ".bin"
    if not path.endswith(".bin"):
        raise ValueError("Expected a VLSB .bin file")
    if not path.startswith("/"):
        path = _base + "/" + path
    size = width * ((height + 7) // 8)
    with open(path, "rb") as source:
        source.seek(0, 2)
        if source.tell() != size:
            raise ValueError("Sprite byte count does not match dimensions")
        source.seek(0)
        data = bytearray(size)
        if source.readinto(data) != size:
            raise ValueError("Incomplete sprite data")
    return thumby.Sprite(width, height, data)


def _get(path, width, height):
    for entry in _cache:
        if entry[0] == path and entry[1] == width and entry[2] == height:
            return entry[3]
    if len(_cache) >= _CACHE_LIMIT:
        del _cache[0]
    try:
        sprite = _load(path, width, height)
    except (OSError, ValueError) as error:
        print("Image unavailable:", path, error)
        sprite = None
    # Cache misses too: no repeated file access for an unfinished asset.
    _cache.append((path, width, height, sprite))
    return sprite


def safe_blit(x, y, bitmapData, width=72, height=40, key=0,
              mirrorX=0, mirrorY=0):
    global _fallback, _fallback_checked
    if isinstance(bitmapData, str):
        sprite = _get(bitmapData, width, height)
    else:
        sprite = thumby.Sprite(width, height, bitmapData)
    present = sprite is not None
    if sprite is None:
        if not _fallback_checked:
            try:
                _fallback = _load("assets_ui_error.bin", 12, 12)
            except (OSError, ValueError) as error:
                print("Fallback unavailable:", error)
            _fallback_checked = True
        sprite = _fallback
    if sprite is None:
        # Last resort when even the existing error asset is absent.
        thumby.display.drawRectangle(x, y, 12, 12, 1)
        return False
    sprite.x = x
    sprite.y = y
    sprite.key = key
    sprite.mirrorX = mirrorX
    sprite.mirrorY = mirrorY
    thumby.display.drawSprite(sprite)
    return present



import random

ENEMIES = (
    ('Trinar Obscuritas', 'SLSH', 'ILL', 'assets_enemy_TrinarObscuritas.bin', 'Trinar Obscuritas'),
    ('Aurel Morpheus', 'COND', 'SLP', 'assets_enemy_AurelMorpheus.bin', 'Aurel Morpheus'),
    ('Feulan Thanatos', 'MAG', 'CTOX', 'assets_enemy_FeulanThanatos.bin', 'Feulan Thanatos'),
    ('Hydros Helios', 'COOL', 'LABS', 'assets_enemy_HydrosHelios.bin', 'Hydros Helios'),
    ('SacrosDagonis', 'ISO', 'COMP', 'assets_enemy_SacrosDagonis.bin', 'Sacros Dagonis'),
    ('Nephan Lux', 'ILL', 'PUR', 'assets_enemy_NephanLux.bin', 'Nephan Lux'),
    ('Chlor Seraphis', 'LABS', 'ACT', 'assets_enemy_ChlorSeraphis.bin', 'Chlor Seraphis'),
    ('Ramus Mnemosyne', 'MEM', 'SAC', 'assets_enemy_RamusMnemosyne.bin', 'Ramus Mnemosyne'),
    ('Obtenebr Kali', 'SLSH', 'CTOX', 'assets_enemy_ObtenebrKali.bin', 'Obtenebr Kali'),
    ('Limen Amateras', 'PUR', 'STB', 'assets_enemy_LimenAmateras.bin', 'Limen Amateras'),
    ('Fervor Apep', 'HE', 'TOXM', 'assets_enemy_FervorApep.bin', 'Fervor Apep'),
    ('Cryon Hermes', 'LT', 'INT', 'assets_enemy_CryonHermes.bin', 'Cryon Hermes'),
    ('Gravus Enlil', 'MAG', 'EXP', 'assets_enemy_GravusEnlil.bin', 'Gravus Enlil'),
    ('Antra Soma', 'ACT', 'CALM', 'assets_enemy_AntraSoma.bin', 'Antra Soma'),
    ('Rubra Baal', 'ACID', 'HE', 'assets_enemy_RubraBaal.bin', 'Rubra Baal'),
    ('Tenebri Izanami', 'CTOX', 'SLP', 'assets_enemy_TenebriIzanami.bin', 'Tenebri Izanami'),
    ('Vallis Hypnos', 'SLP', 'CALM', 'assets_enemy_VallisHypnos.bin', 'Vallis Hypnos'),
    ('Aethon Camael', 'HE', 'SLSH', 'assets_enemy_AethonCamael.bin', 'Aethon Camael'),
    ('Albus Vishnu', 'PUR', 'STB', 'assets_enemy_AlbusVishnu.bin', 'Albus Vishnu'),
    ('Noctar Odin', 'MEM', 'INT', 'assets_enemy_NoctarOdin.bin', 'Noctar Odin'),
    ('Virel Typhon', 'ACT', 'EXP', 'assets_enemy_VirelTyphon.bin', 'Virel Typhon'),
    ('Fractus Yama', 'COOL', 'CTOX', 'assets_enemy_FractusYama.bin', 'Fractus Yama'),
    ('Atrum Uriel', 'LABS', 'SLSH', 'assets_enemy_AtrumUriel.bin', 'Atrum Uriel'),
    ('Tellas Haniel', 'SAC', 'PUR', 'assets_enemy_TellasHaniel.bin', 'Tellas Haniel'),
    ('Gelida Leviathan', 'LT', 'STB', 'assets_enemy_GelidaLeviathan.bin', 'Gelida Leviathan'),
    ('Demiurg Seth', 'STB', 'TOXM', 'assets_enemy_DemiurgSeth.bin', 'Demiurg Seth'),
    ('Vitrum Freyja', 'EXP', 'MEM', 'assets_enemy_VitrumFreyja.bin', 'Vitrum Freyja'),
    ('Keraunos Indra', 'HE', 'ACT', 'assets_enemy_KeraunosIndra.bin', 'Keraunos Indra'),
    ('Occlus Eresh', 'ISO', 'ACID', 'assets_enemy_OcclusEresh.bin', 'Occlus Eresh'),
    ('Vesper Samael', 'SAC', 'ILL', 'assets_enemy_VesperSamael.bin', 'Vesper Samael'),
)

AMMO = (
    ('H', 'A', 'HE', 'assets_ammo_H.bin', 'H'),
    ('He', 'A', 'LT', 'assets_ammo_He.bin', 'He'),
    ('O', 'A', 'EXP', 'assets_ammo_O.bin', 'O'),
    ('C', 'A', 'STB', 'assets_ammo_C.bin', 'C'),
    ('Fe', 'A', 'MAG', 'assets_ammo_Fe.bin', 'Fe'),
    ('Au', 'A', 'COND', 'assets_ammo_Au.bin', 'Au'),
    ('CO2', 'M', 'COMP', 'assets_ammo_CO2.bin', 'CO2'),
    ('SA', 'M', 'ACID', 'assets_ammo_H2SO4.bin', 'H2SO4'),
    ('NH3', 'M', 'TOXM', 'assets_ammo_NH3.bin', 'NH3'),
    ('H2O', 'M', 'COOL', 'assets_ammo_H2O.bin', 'H2O'),
    ('Chl', 'O', 'LABS', 'assets_ammo_Chl.bin', 'Chl'),
    ('Adr', 'O', 'ACT', 'assets_ammo_Adr.bin', 'Adr'),
    ('Trp', 'O', 'CALM', 'assets_ammo_Trp.bin', 'Trp'),
    ('Am', 'G', 'ILL', 'assets_ammo_Am.bin', 'Am'),
    ('LL', 'G', 'INT', 'assets_ammo_LL.bin', 'LL'),
    ('Ob', 'G', 'SLSH', 'assets_ammo_Ob.bin', 'Ob'),
    ('RH', 'P', 'CTOX', 'assets_ammo_RH.bin', 'RH'),
    ('RM', 'P', 'MEM', 'assets_ammo_RM.bin', 'RM'),
    ('Lv', 'P', 'SLP', 'assets_ammo_Lv.bin', 'Lv'),
    ('L', 'S', 'ISO', 'assets_ammo_L.bin', 'L'),
    ('D', 'S', 'SAC', 'assets_ammo_D.bin', 'D'),
    ('Lg', 'S', 'PUR', 'assets_ammo_Lg.bin', 'Lg'),
)

CHARACTERS = (('Baraqiel', 'whale1.bmp', 'assets_ang_Baraqiel_whale1.bmp', 0.06), ('Baraqiel', 'whale0.bmp', 'assets_ang_Baraqiel_whale0.bmp', 0.04), ('Baraqiel', '0.bmp', 'assets_ang_Baraqiel_0.bmp', 0.1125), ('Baraqiel', '._whale1.bmp', 'assets_ang_Baraqiel_._whale1.bmp', 0.1125), ('Baraqiel', '._whale0.bmp', 'assets_ang_Baraqiel_._whale0.bmp', 0.1125), ('Baraqiel', '._0.bmp', 'assets_ang_Baraqiel_._0.bmp', 0.1125), ('Raziel', '0.bmp', 'assets_ang_Raziel_0.bmp', 0.1285714285714286), ('Raziel', 'owl.bmp', 'assets_ang_Raziel_owl.bmp', 0.1), ('Raziel', '._0.bmp', 'assets_ang_Raziel_._0.bmp', 0.1285714285714286), ('Raziel', '._owl.bmp', 'assets_ang_Raziel_._owl.bmp', 0.1285714285714286), ('Sraosha', '2s.bmp', 'assets_ang_Sraosha_2s.bmp', 0.04736842105263158), ('Sraosha', 'fish.bmp', 'assets_ang_Sraosha_fish.bmp', 0.1), ('Sraosha', '0.bmp', 'assets_ang_Sraosha_0.bmp', 0.04736842105263158), ('Sraosha', '1.bmp', 'assets_ang_Sraosha_1.bmp', 0.04736842105263158), ('Sraosha', '3ss.bmp', 'assets_ang_Sraosha_3ss.bmp', 0.04736842105263158), ('Sraosha', '._2s.bmp', 'assets_ang_Sraosha_._2s.bmp', 0.04736842105263158), ('Sraosha', '._fish.bmp', 'assets_ang_Sraosha_._fish.bmp', 0.04736842105263158), ('Sraosha', '._0.bmp', 'assets_ang_Sraosha_._0.bmp', 0.04736842105263158), ('Sraosha', '._1.bmp', 'assets_ang_Sraosha_._1.bmp', 0.04736842105263158), ('Sraosha', '._3ss.bmp', 'assets_ang_Sraosha_._3ss.bmp', 0.04736842105263158), ('VohuManah', '0.bmp', 'assets_ang_VohuManah_0.bmp', 0.1285714285714286), ('VohuManah', 'fish.bmp', 'assets_ang_VohuManah_fish.bmp', 0.1), ('VohuManah', '._0 2.bmp', 'assets_ang_VohuManah_._0 2.bmp', 0.1285714285714286), ('VohuManah', '._fish.bmp', 'assets_ang_VohuManah_._fish.bmp', 0.1285714285714286), ('Taat', '0.bin', 'assets_ang_Taat_0.bin', 1.0), ('Zairic', '0.bin', 'assets_ang_Zairic_0.bin', 1.0), ('Taurvi', '0.bin', 'assets_ang_Taurvi_0.bin', 1.0), ('Xsathra', '0.bin', 'assets_ang_Xsathra_0.bin', 1.0), ('Sarva', '0.bin', 'assets_ang_Sarva_0.bin', 1.0), ('Zadkiel', '0.bin', 'assets_ang_Zadkiel_0.bin', 1.0), ('Zadkiel', '1.bin', 'assets_ang_Zadkiel_1.bin', 1.0), ('Azazel', '0.bin', 'assets_ang_Azazel_0.bin', 1.0))

ACTION_PATHS = ('assets_ang_Baraqiel_0_act.bmp', 'assets_ang_Baraqiel_._0_act.bmp', 'assets_ang_Raziel_0_act.bmp', 'assets_ang_Raziel_._0_act.bmp', 'assets_ang_Sraosha_2s_act.bmp', 'assets_ang_Sraosha_3ss_act.bmp', 'assets_ang_Sraosha_0_act.bmp', 'assets_ang_Sraosha_1_act.bmp', 'assets_ang_Sraosha_._2s_act.bmp', 'assets_ang_Sraosha_._3ss_act.bmp', 'assets_ang_Sraosha_._0_act.bmp', 'assets_ang_Sraosha_._1_act.bmp', 'assets_ang_VohuManah_0_act.bmp', 'assets_ang_VohuManah_._0_act.bmp', 'assets_ang_Azazel_0_act.bin', 'assets_ang_Sarva_0_act.bin', 'assets_ang_Taat_0_act.bin', 'assets_ang_Taurvi_0_act.bin', 'assets_ang_Xsathra_0_act.bin', 'assets_ang_Zadkiel_0_act.bin', 'assets_ang_Zairic_0_act.bin')

COURSE_SECONDS = (60, 180, 300, 600)
COURSE_LABELS = ("1min", "3min", "5min", "10min")
BGM_NAMES = ("fuzennokami", "whdrmcrasha")
FOLDERS = ('Sraosha', 'VohuManah', 'Raziel', 'Baraqiel', 'Taat', 'Zairic', 'Taurvi', 'Xsathra', 'Sarva', 'Zadkiel', 'Azazel')
FOLDER_WEIGHTS = (30, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7)
TITLE, SELECT, ENEMY, PICK, SCORE, END = range(6)


def randbelow(n):
    # getrandbits is available on MicroPython; no random.sample dependency.
    bits = 1
    while (1 << bits) < n:
        bits += 1
    value = random.getrandbits(bits)
    while value >= n:
        value = random.getrandbits(bits)
    return value


RESCUE_IMAGES = (('Sraosha', 'assets_ang_Sraosha_0_act.bin'), ('Sraosha', 'assets_ang_Sraosha_1.bin'), ('Sraosha', 'assets_ang_Sraosha_1_act.bin'), ('Sraosha', 'assets_ang_Sraosha_2s_act.bin'), ('Sraosha', 'assets_ang_Sraosha_3ss.bin'), ('Sraosha', 'assets_ang_Sraosha_3ss_act.bin'), ('Sraosha', 'assets_ang_Sraosha_rslt.bin'), ('VohuManah', 'assets_ang_VohuManah_0.bin'), ('VohuManah', 'assets_ang_VohuManah_0_act.bin'), ('VohuManah', 'assets_ang_VohuManah_fish.bin'), ('VohuManah', 'assets_ang_VohuManah_rslt.bin'), ('Raziel', 'assets_ang_Raziel_0.bin'), ('Raziel', 'assets_ang_Raziel_0_act.bin'), ('Raziel', 'assets_ang_Raziel_owl.bin'), ('Raziel', 'assets_ang_Raziel_rslt.bin'), ('Baraqiel', 'assets_ang_Baraqiel_0.bin'), ('Baraqiel', 'assets_ang_Baraqiel_0_act.bin'), ('Baraqiel', 'assets_ang_Baraqiel_rslt.bin'), ('Baraqiel', 'assets_ang_Baraqiel_whale1.bin'), ('Azazel', 'assets_ang_Azazel_0.bin'), ('Azazel', 'assets_ang_Azazel_0_act.bin'), ('Azazel', 'assets_ang_Azazel_0_rslt.bin'), ('Sarva', 'assets_ang_Sarva_0.bin'), ('Sarva', 'assets_ang_Sarva_0_act.bin'), ('Sarva', 'assets_ang_Sarva_0_rslt.bin'), ('Taat', 'assets_ang_Taat_0.bin'), ('Taat', 'assets_ang_Taat_0_act.bin'), ('Taat', 'assets_ang_Taat_0_rslt.bin'), ('Taurvi', 'assets_ang_Taurvi_0.bin'), ('Taurvi', 'assets_ang_Taurvi_0_act.bin'), ('Taurvi', 'assets_ang_Taurvi_0_rslt.bin'), ('Xsathra', 'assets_ang_Xsathra_0.bin'), ('Xsathra', 'assets_ang_Xsathra_0_act.bin'), ('Xsathra', 'assets_ang_Xsathra_0_rslt.bin'), ('Zadkiel', 'assets_ang_Zadkiel_0.bin'), ('Zadkiel', 'assets_ang_Zadkiel_0_act.bin'), ('Zadkiel', 'assets_ang_Zadkiel_0_rslt.bin'), ('Zadkiel', 'assets_ang_Zadkiel_1_rslt.bin'), ('Zairic', 'assets_ang_Zairic_0.bin'), ('Zairic', 'assets_ang_Zairic_0_act.bin'), ('Zairic', 'assets_ang_Zairic_0_rslt.bin'))

def valid_normal(row):
    filename = row[1]
    return (not filename.startswith("._") and
            "_act" not in filename and "rslt" not in filename)


def weighted_image(rows):
    total = 0
    for row in rows:
        total += row[3]
    value = random.getrandbits(24) / 16777216 * total
    chosen = rows[-1]
    for row in rows:
        value -= row[3]
        if value < 0:
            chosen = row
            break
    return chosen


def choose_character():
    value = randbelow(100)
    folder = FOLDERS[-1]
    for i in range(len(FOLDERS)):
        if value < FOLDER_WEIGHTS[i]:
            folder = FOLDERS[i]
            break
        value -= FOLDER_WEIGHTS[i]
    rows = [row for row in CHARACTERS if row[0] == folder and valid_normal(row)]
    # Retain the selected identity even if its catalog has no normal images.
    return weighted_image(rows) if rows else (folder, "", "", 0)


def resolve_character_image(folder, preferred):
    # The prefix check prevents a malformed reference crossing characters.
    prefix = "assets_ang_" + folder + "_"
    if (preferred.startswith(prefix) and
            not preferred[len(prefix):].startswith("._") and
            _get(preferred, 24, 24) is not None):
        return preferred
    # Missing numbered normal poses use this character's zero pose first.
    if preferred.startswith(prefix) and preferred[len(prefix):-4].isdigit():
        zero = prefix + "0.bin"
        if _get(zero, 24, 24) is not None:
            return zero
    valid = []
    for row in CHARACTERS:
        if (row[0] == folder and valid_normal(row) and
                row[2].startswith(prefix) and _get(row[2], 24, 24) is not None):
            valid.append(row)
    if valid:
        path = weighted_image(valid)[2]
        print("CHAR fallback:", folder, preferred, "->", path)
        return path
    # Last resort: known real files of this same character, including action
    # and result images. No invented normal-image weights are assigned here.
    for owner, path in RESCUE_IMAGES:
        if owner == folder and path.startswith(prefix) and _get(path, 24, 24) is not None:
            print("CHAR rescue:", folder, preferred, "->", path)
            return path
    print("CHAR unavailable:", folder)
    return None


def resolve_result_image(character):
    folder = character[0]
    prefix = "assets_ang_" + folder + "_"
    # Legacy characters use their shared result; new numbered forms keep theirs.
    for path in (prefix + "rslt.bin", prefix + character[1][:-4] + "_rslt.bin",
                 prefix + "0_rslt.bin"):
        if _get(path, 24, 24) is not None:
            return path
    return resolve_character_image(folder, prefix + "rslt.bin")


def resolve_action_image(folder, path):
    action = path[:-4] + "_act.bin"
    if _get(action, 24, 24) is not None:
        return action
    prefix = "assets_ang_" + folder + "_"
    if path.startswith(prefix) and path[len(prefix):-4].isdigit():
        zero = prefix + "0_act.bin"
        if _get(zero, 24, 24) is not None:
            return zero
    return path


def draw_character(path, x, y):
    # Generic proxy only after the same-character search was exhausted.
    safe_blit(x, y, path if path is not None else "__missing_character__.bin", 24, 24, -1)


def matches(enemy, ammo):
    return ammo[2] == enemy[1] or ammo[2] == enemy[2]


def make_candidates(enemy):
    # Preserve the existing helper's rule: one matching ammo if available,
    # then four distinct other ammo, and shuffle the five positions.
    matching = [i for i in range(len(AMMO)) if matches(enemy, AMMO[i])]
    selected = []
    if matching:
        selected.append(matching[randbelow(len(matching))])
    while len(selected) < 5:
        i = randbelow(len(AMMO))
        if i not in selected:
            selected.append(i)
    for i in range(4, 0, -1):
        j = randbelow(i + 1)
        selected[i], selected[j] = selected[j], selected[i]
    return selected


def round_score(enemy, chosen):
    hits = 0
    for i in chosen:
        if matches(enemy, AMMO[i]):
            hits += 1
    points = hits * 200 + (3 - hits) * 50
    return (points * 2 if hits >= 2 else points), hits


def padded(number, digits):
    value = str(number)
    return "0" * max(0, digits - len(value)) + value


def time_text(ms):
    seconds = (ms + 999) // 1000
    return padded(seconds // 60, 2) + ":" + padded(seconds % 60, 2)


BGM_FUZEN = b'\x00\x00\x10\x00\x06\x01\x90\x00\x0b\x02\xa0\x01\x10\x03(\x02\xe4\x02\x90\x00\xba\x02\xa0\x01n\x02\x8c\x00\x0b\x02\xa0\x01&\x01\x8c\x00K\x02\xa0\x01n\x02\x8c\x00\xba\x02\x18\x01]\x01\x88\x00n\x02\x14\x01\xdd\x04\x8c\x00n\x02\x8c\x007\x01\x14\x01n\x02\xc8\x00\x00\x00H\x00\x06\x01\x90\x00\x0b\x02\x8c\x00\x17\x04\x8c\x00\x0b\x02\x88\x00\x10\x03,\x02\xe4\x02\x8c\x00\xba\x02\x90\x00]\x01\x84\x00\xba\x02\x90\x00\x15\x01\x88\x00\x0b\x02\x8c\x00\x06\x01\x88\x00\x0b\x02\x8c\x00&\x01\x8c\x00K\x02\x8c\x00\x0b\x02\x8c\x00\x88\x01\x14\x01\xd2\x01\x14\x01\x0b\x02\x00\x03\x00\x00\xdc\x01\x06\x01\x90\x00\x0b\x02\xa0\x01\x10\x03,\x02\xe4\x02\x8c\x00\xba\x02\xa4\x01n\x02\x88\x00\x0b\x02\xa4\x01&\x01\x88\x00K\x02\xa4\x01n\x02\x88\x00\xba\x02\xa0\x01n\x02\x14\x01\xdd\x04\x8c\x00n\x02\x8c\x007\x01\x14\x01\xdd\x04\x8c\x00\x0b\x02\x88\x00\x10\x03\x1c\x01\x88\x01\x84\x00\x10\x03\xa8\x01\x88\x01\x84\x00\x10\x03\x8c\x00\xba\x02\x90\x00n\x02(\x02\xd2\x01\x18\x01\x0b\x02\xe0\x04\x17\x04\x8c\x00\x06\x01\x80\x00\xf7\x00\x10\x00\x06\x01\x84\x00\x17\x04\x8c\x00\x06\x01\x88\x00\x0b\x02\x90\x00\x17\x04\x88\x00\x0b\x02\xd0\x00\x00\x00@\x00\x0b\x02\xa4\x01K\x02\x1c\x01n\x02\x80\x00K\x02\x0c\x00n\x02\x8c\x00K\x02\x14\x01n\x02\x14\x01\xa4\x03\x88\x00\x10\x03\x18\x01\xba\x02\x8c\x00\x10\x03X\x04\x17\x04\x94\x04\x00\x00D\x00\x0b\x02\xa4\x01K\x02\x1c\x01n\x02\x80\x00K\x02\x0c\x00n\x02\x88\x00\xba\x02\x8c\x00n\x02\x8c\x00K\x02\x8c\x00n\x02\x8c\x00K\x02\x88\x00\xd2\x01\x14\x01]\x01\x8c\x00\x88\x01\x14\x01r\x01\x80\x00\x88\x01\x0c\x00]\x01\x8c\x00\x88\x01\x14\x01\x9f\x010\x02\x88\x01`\x02\x00\x00H\x00\x88\x01\x94\x00]\x01\x14\x01\x88\x01\x18\x017\x01\x88\x00]\x01\x0c\x00J\x01x\x00]\x01\x94\x007\x01\x0c\x00J\x01\x0c\x007\x01l\x00&\x01\x0c\x00\x15\x01\x0c\x00&\x01\x00\x01J\x01\x0c\x007\x01|\x00&\x01\x0c\x00\x15\x01\x0c\x00&\x01x\x00\x15\x01\x1c\x00\x06\x01t\x00\xf7\x00\x18\x00\xe9\x00\x80\x00\xd0\x00 \x00\xc4\x00T\x00\xf7\x00\x14\x00\xe9\x00\x80\x00\xf7\x00\x14\x00\x06\x01\xf4\x00\x15\x01\x10\x00\x06\x01\x08\x01\x15\x01\x0c\x00\x06\x01|\x00\xf7\x00\x10\x00\x06\x01\x88\x00\x0b\x02\x18\x01\x17\x04\x88\x00\x0b\x02\x90\x00\x06\x01\x84\x00\x17\x04\x90\x00\x06\x01|\x00\xf7\x00\x10\x00\x06\x01\x84\x00\x0b\x02\xd0\x00\x00\x00\x88\x00'
BGM_WHDRM = b'\x00\x00\x0c\x00\xba\x02,\x01\x00\x00\x80\x00\xba\x02\xb8\x01n\x02\xd8\x00K\x02\xd4\x00\x0b\x02\xd4\x00\xd2\x01\xd8\x00\x17\x04\xd8\x00\x0b\x02\xd4\x00K\x02\xd8\x00\xd2\x01\xec\x01\x00\x00\x8c\x00]\x01\xb4\x01\xba\x02 \x01\x00\x00\x88\x00\xba\x02\xb4\x01n\x02\xd8\x00K\x02\xd4\x00\x0b\x02\xd4\x00\xd2\x01\xd8\x00\x0b\x02\xd8\x00K\x02\xd8\x00\xd2\x01\xd4\x00K\x02\xec\x01\x00\x00\x90\x00]\x01\xb0\x01\xba\x02`\x03n\x02\xd0\x00K\x02\xd8\x00\x0b\x02\xd4\x00\xd2\x01\xd8\x00\x0b\x02\xd8\x00K\x02\xd8\x00\xd2\x01\xd8\x00]\x01\xd0\x00\xd2\x01\x1c\x01\x00\x00\x8c\x00]\x01\xdc\x00\xd2\x01\x18\x01\x00\x00\x8c\x00\xd2\x01\x8c\x02n\x02\xdc\x00K\x02\xd0\x00\x0b\x02\xd4\x00\xd2\x01\xd8\x00\x0b\x02\xf4\x01\x00\x00\x88\x00\xd2\x01\xb8\x01\xa4\x03\xd4\x00\xd2\x01\x18\x01\x00\x00\x8c\x00]\x01\xb4\x01\xd2\x01\xac\x01\x0b\x02\xb0\x01K\x02\xac\x01]\x01\xa8\x01\xd2\x01\xac\x01\x0b\x02\xb0\x01K\x02\xac\x01\xd2\x01\xac\x01\xba\x02\xb0\x01\xd2\x01\xa8\x01\xba\x02\xb0\x01n\x02l\x00K\x02h\x00\x0b\x02l\x00\xd2\x01h\x00\x0b\x02\xdc\x00K\x02\x14\x01\x00\x00d\x01\xd2\x01t\x00\xa4\x03p\x00\xe9\x00d\x00\xa4\x03\xb4\x00\x00\x00\x92\x00'
SE_BP0 = b'\x00\x00\x0c\x00\x17\x04D\x00\x0b\x02\x84\x00\x00\x00:\x00'
SE_BP1 = b'\x00\x00\x0c\x00]\x01D\x00\xba\x02<\x00u\x05|\x00\x00\x007\x00'
SE_CLEAR = b'\x00\x00\x0c\x00\xa4\x03\xcc\x01\x00\x00(\x00\xa4\x03\x88\x00]\x01\xb8\x00\x00\x008\x00\xa4\x03\xd0\x00\x00\x00,\x00\xa4\x03\x84\x00\xba\x02\xc8\x00\x00\x00(\x00\xa4\x03\xd0\x00\x00\x00,\x00u\x05\xc0\x00\x00\x008\x00\x0b\x02\xcc\x00\x00\x00\xac\x00\x0b\x02\xc8\x00\x00\x004\x00\x0b\x02\x84\x00K\x02\xc0\x00\x00\x000\x00n\x02\x04\x017\x01|\x00n\x02|\x00\xdd\x04\x00\x017\x014\x01\x00\x00;\x00'
BGM_TRACKS = (BGM_FUZEN, BGM_WHDRM)

# Tone records: unsigned little-endian frequency Hz + duration ms (4 bytes).
# Frequency 0 is a rest. No PCM buffers and no blocking calls.
class ToneTrack:
    def __init__(self):
        self.data = None
        self.offset = 0
        self.remaining = 0
        self.frequency = 0
        self.loop = False
        self.total = 0
        self.version = 0

    def read_note(self):
        d = self.data
        i = self.offset
        self.frequency = d[i] | (d[i + 1] << 8)
        self.remaining += d[i + 2] | (d[i + 3] << 8)
        self.version += 1

    def start(self, data, loop=False):
        self.data = data
        self.loop = loop
        self.offset = 0
        self.remaining = 0
        self.total = 0
        for i in range(0, len(data), 4):
            self.total += data[i + 2] | (data[i + 3] << 8)
        self.read_note()

    def stop(self):
        self.data = None
        self.remaining = 0
        self.frequency = 0
        self.version += 1

    def tick(self, elapsed):
        if self.data is None:
            return
        if self.loop:
            if elapsed >= self.total:
                self.version += 1
            elapsed %= self.total
        self.remaining -= elapsed
        while self.remaining <= 0:
            self.offset += 4
            if self.offset >= len(self.data):
                if not self.loop:
                    self.stop()
                    return
                self.offset = 0
            self.read_note()


class Sound:
    def __init__(self, now):
        self.bgm = ToneTrack()
        self.effect = ToneTrack()
        self.last = now
        self.output_track = None
        self.output_version = -1

    def advance(self, now):
        elapsed = time.ticks_diff(now, self.last)
        self.last = now
        self.bgm.tick(elapsed)
        self.effect.tick(elapsed)

    def start_bgm(self, data, now):
        self.advance(now)
        self.bgm.start(data, True)

    def se(self, data, now):
        self.advance(now)
        # Latest input replaces the previous effect; there is no unbounded queue.
        self.effect.start(data)

    def stop_bgm(self):
        self.bgm.stop()

    def stop(self):
        self.bgm.stop()
        self.effect.stop()
        thumby.audio.stop()
        self.output_track = None
        self.output_version = -1

    def update(self, now):
        self.advance(now)
        active = self.effect if self.effect.data is not None else self.bgm
        if active.data is None:
            if self.output_track is not None:
                thumby.audio.stop()
                self.output_track = None
                self.output_version = -1
            return
        if active is not self.output_track or active.version != self.output_version:
            if active.frequency:
                thumby.audio.play(active.frequency, active.remaining)
            else:
                thumby.audio.stop()
            self.output_track = active
            self.output_version = active.version


# Stable across build names. Saves live outside the Games directory.
SAVE_NAME = "SraoshaVanish"
SAVE_KEY = "highscore"


class HighScore:
    def __init__(self):
        self.score = 0
        self.ready = False
        self.error = None
        self.load()

    def load(self):
        try:
            thumby.saveData.setName(SAVE_NAME)
            value = thumby.saveData.getItem(SAVE_KEY) if thumby.saveData.hasItem(SAVE_KEY) else 0
            if type(value) is not int or value < 0:
                raise ValueError("Invalid saved high score")
            self.score = value
            self.ready = True
            self.error = None
            print("HIGH SCORE loaded:", value)
            return True
        except (OSError, ValueError, TypeError, AttributeError) as error:
            self.ready = False
            self.error = "LOAD ERR"
            print("HIGH SCORE load failed:", error)
            return False

    def commit(self, score):
        if not self.ready:
            return False
        if score <= self.score:
            self.error = None
            return True
        try:
            thumby.saveData.setItem(SAVE_KEY, score)
            thumby.saveData.save()
        except (OSError, ValueError, TypeError, AttributeError) as error:
            self.error = "SAVE ERR"
            print("HIGH SCORE save failed:", error)
            return False
        self.score = score
        self.error = None
        print("HIGH SCORE saved:", score)
        return True


ENEMY_TEXT_OFFSETS = (0, 29, 53, 76, 97, 119, 140, 169, 190, 210, 238, 261, 280, 305, 326, 350, 377, 402, 427, 457, 486, 513, 533, 563, 591, 613, 636, 662, 686, 713)
AMMO_TEXT_OFFSETS = (737, 808, 863, 910, 959, 1002, 1074, 1111, 1157, 1198, 1255, 1313, 1356, 1407, 1457, 1492, 1534, 1588, 1624, 1662, 1706, 1750)

ENEMY_BOOK = 6
AMMO_BOOK = 7
ANGEL_BOOK = 8
ANGELS = (('Sraosha', 'CHERB', 'assets_ang_Sraosha_0.bin'), ('VohuManah', 'CHERB', 'assets_ang_VohuManah_0.bin'), ('Raziel', 'CHERB', 'assets_ang_Raziel_0.bin'), ('Baraqiel', 'SERAP', 'assets_ang_Baraqiel_0.bin'), ('Taat', 'CHERB', 'assets_ang_Taat_0.bin'), ('Zairic', 'SERAP', 'assets_ang_Zairic_0.bin'), ('Taurvi', 'SERAP', 'assets_ang_Taurvi_0.bin'), ('Xsathra', 'POWER', 'assets_ang_Xsathra_0.bin'), ('Sarva', 'DOMIN', 'assets_ang_Sarva_0.bin'), ('Zadkiel', 'DOMIN', 'assets_ang_Zadkiel_0.bin'), ('Azazel', 'FALL', 'assets_ang_Azazel_0.bin'))
ANGEL_TEXT_OFFSETS = (1814, 1866, 1913, 1965, 2017, 2072, 2125, 2178, 2232, 2280, 2333)



# In ANGELS order; lightweight form identifiers, no duplicate image data.
ANGEL_FORMS = (('0', '1', '2s', '3ss', 'fish'), ('0', 'fish'), ('0', 'owl'), ('0', 'whale0', 'whale1'), ('0',), ('0',), ('0',), ('0',), ('0',), ('0', '1'), ('0',))


def catalog_angel_image(index, frame):
    prefix = "assets_ang_" + ANGELS[index][0] + "_"
    form = ANGEL_FORMS[index][frame // 3]
    phase = frame % 3
    if phase == 0:
        paths = (prefix + form + ".bin", prefix + "0.bin")
    elif phase == 1:
        paths = (prefix + form + "_act.bin", prefix + "0_act.bin", prefix + "0.bin")
    else:
        paths = (prefix + form + "_rslt.bin", prefix + "0_rslt.bin",
                 prefix + "rslt.bin", prefix + "0.bin")
    for path in paths:
        if _get(path, 24, 24) is not None:
            # Keep only this frame, including no unsuccessful lookup entries.
            entry = _cache[-1]
            del _cache[:]
            _cache.append(entry)
            return path
    return None

def read_catalog_description(state, index):
    offsets = ANGEL_TEXT_OFFSETS if state == ANGEL_BOOK else (ENEMY_TEXT_OFFSETS if state == ENEMY_BOOK else AMMO_TEXT_OFFSETS)
    try:
        with open(_base + "/catalog_text.dat", "rb") as source:
            source.seek(offsets[index])
            line = source.readline()
            if not line.endswith(b"\n"):
                raise ValueError("Incomplete catalog entry")
            return line[:-1].decode("utf-8")
    except (OSError, ValueError) as error:
        print("CATALOG text unavailable:", state, index, error)
        return "Description unavailable"


class Game:
    def __init__(self, now):
        self.sound = Sound(now)
        self.highscore = HighScore()
        self.new_high = False
        self.save_failed = False
        self.book_index = 0
        self.book_lines = []
        self.state = TITLE
        self.course = 0
        self.bgm = 0
        self.remaining = 0
        self.total = 0
        self.points = 0
        self.hits = 0
        self.enemy = None
        self.character = None
        self.character_path = None
        self.result_path = None
        self.menu_path = None
        self.candidates = []
        self.locks = []
        self.cursor = 0
        self.last = now
        self.entered = now
        self.flash = None
        self.b_start = None
        self.b_slot = 0

    def book_data(self):
        if self.state == ANGEL_BOOK:
            return ANGELS
        return ENEMIES if self.state == ENEMY_BOOK else AMMO

    def book_entry(self, now=None):
        self.book_frame = 0
        self.book_frame_at = self.last if now is None else now
        self.book_image = None
        self.book_image_loaded = False
        data = self.book_data()
        entry = data[self.book_index]
        description = read_catalog_description(self.state, self.book_index)
        width = 11 if self.state == ANGEL_BOOK else (7 if self.state == ENEMY_BOOK else 12)
        self.book_lines = [description[i:i + width] for i in range(0, len(description), width)]
        clear_cache()
        gc.collect()

    def open_book(self, state, now):
        self.flash = None
        self.book_index = 0
        self.enter(state, now)
        self.book_entry(now)
        self.sound.se(SE_BP1, now)

    def enter(self, state, now):
        self.state = state
        if state == END:
            self.sound.stop_bgm()
            self.new_high = self.highscore.ready and self.total > self.highscore.score
            self.save_failed = not self.highscore.commit(self.total)
            self.sound.se(SE_CLEAR, now)
        self.entered = now
        self.b_start = None
        clear_cache()
        if state == SELECT:
            self.menu_path = resolve_character_image("Sraosha", "assets_ang_Sraosha_fish.bin")
        elif state == ENEMY:
            self.character_path = resolve_character_image(self.character[0], self.character[2])
        elif state == SCORE:
            self.result_path = resolve_result_image(self.character)
        elif state == END:
            self.result_path = resolve_result_image(self.character) if self.character else None
            self.character_path = None
            self.menu_path = None
        elif state == TITLE:
            self.character_path = None
            self.result_path = None
            self.menu_path = None
        gc.collect()
        print("ROUND", VERSION, "state:", state, "remaining_ms:", self.remaining,
              "total:", self.total, "free:", gc.mem_free())

    def title(self, now):
        self.new_high = False
        self.save_failed = False
        self.book_index = 0
        self.book_lines = []
        self.sound.stop()
        self.sound.se(SE_BP0, now)
        self.course = 0
        self.bgm = 0
        self.total = 0
        self.remaining = 0
        self.points = 0
        self.hits = 0
        self.enemy = None
        self.character = None
        self.character_path = None
        self.result_path = None
        self.menu_path = None
        self.candidates = []
        self.locks = []
        self.cursor = 0
        self.flash = None
        self.enter(TITLE, now)

    def next_enemy(self, now):
        self.enemy = ENEMIES[randbelow(len(ENEMIES))]
        self.character = choose_character()
        self.candidates = make_candidates(self.enemy)
        self.locks = []
        self.cursor = 0
        self.enter(ENEMY, now)
        print("ENEMY:", self.enemy[0], "WE:", self.enemy[1], self.enemy[2],
              "CHAR:", self.character[0], self.character[1])

    def step(self, now, pressed, held):
        elapsed = time.ticks_diff(now, self.last)
        self.last = now
        if self.state == PICK:
            self.remaining = max(0, self.remaining - elapsed)
            # Timeout wins over a simultaneous third lock. No partial score.
            if self.remaining == 0:
                self.enter(END, now)
                return

        if self.state in (ENEMY, PICK, SCORE):
            if held & 2:
                if self.b_start is None:
                    self.b_start = now
                    self.b_slot = self.cursor
                elif time.ticks_diff(now, self.b_start) >= 10000:
                    self.title(now)
                return
            elif self.b_start is not None:
                if self.state == PICK and self.b_slot in self.locks:
                    self.locks.remove(self.b_slot)
                    self.sound.se(SE_BP0, now)
                self.b_start = None

        if self.state == TITLE:
            if self.flash is None and pressed & 4:
                self.open_book(ANGEL_BOOK, now)
                return
            if self.flash is None and pressed & 16:
                self.open_book(ENEMY_BOOK, now)
                return
            elif self.flash is None and pressed & 32:
                self.open_book(AMMO_BOOK, now)
                return
            if self.flash is None and pressed & 1:
                self.flash = now
                self.sound.se(SE_BP1, now)
            if self.flash is not None and time.ticks_diff(now, self.flash) >= 120:
                self.flash = None
                self.enter(SELECT, now)
        elif self.state == ANGEL_BOOK:
            if pressed & 1:
                self.sound.se(SE_BP1, now)
            elif pressed & 2:
                self.title(now)
            elif pressed & (4 | 8):
                self.book_index += 1 if pressed & 4 else -1
                if self.book_index < 0 or self.book_index >= len(ANGELS):
                    self.title(now)
                else:
                    self.book_entry(now)
        elif self.state in (ENEMY_BOOK, AMMO_BOOK):
            if pressed & 2:
                self.title(now)
            elif pressed & (16 | 32):
                data = self.book_data()
                # Enemy book advances left; ammo book advances right.
                direction = -1 if pressed & 16 else 1
                self.book_index += -direction if self.state == ENEMY_BOOK else direction
                if self.book_index < 0 or self.book_index >= len(data):
                    self.title(now)
                else:
                    self.book_entry(now)
            elif pressed & 1:
                self.sound.se(SE_BP1, now)
        elif self.state == SELECT:
            if pressed & 2:
                self.title(now)
            else:
                if pressed & 4:
                    self.course = (self.course - 1) % 4
                elif pressed & 8:
                    self.course = (self.course + 1) % 4
                if pressed & 16:
                    self.bgm = (self.bgm - 1) % 2
                elif pressed & 32:
                    self.bgm = (self.bgm + 1) % 2
                if pressed & 1:
                    self.remaining = COURSE_SECONDS[self.course] * 1000
                    self.total = 0
                    print("START seconds:", COURSE_SECONDS[self.course], "bgm:", BGM_NAMES[self.bgm])
                    self.sound.start_bgm(BGM_TRACKS[self.bgm], now)
                    self.sound.se(SE_BP1, now)
                    self.next_enemy(now)
        elif self.state == ENEMY:
            if pressed & 1:
                self.enter(PICK, now)
                self.sound.se(SE_BP1, now)
        elif self.state == PICK:
            if pressed & 16:
                self.cursor = (self.cursor - 1) % 5
            elif pressed & 32:
                self.cursor = (self.cursor + 1) % 5
            if pressed & 1 and self.cursor not in self.locks:
                self.locks.append(self.cursor)
                self.sound.se(SE_BP1, now)
                if len(self.locks) == 3:
                    chosen = [self.candidates[i] for i in self.locks]
                    self.points, self.hits = round_score(self.enemy, chosen)
                    self.total += self.points
                    print("SCORE ammo:", chosen, "hits:", self.hits, "points:", self.points)
                    self.enter(SCORE, now)
        elif self.state == SCORE:
            if pressed & 1:
                self.next_enemy(now)
                self.sound.se(SE_BP1, now)
        elif self.state == END:
            if pressed & 2:
                self.title(now)
            elif pressed & 1:
                if self.save_failed:
                    if not self.highscore.ready:
                        self.highscore.load()
                        if self.highscore.ready:
                            self.new_high = self.total > self.highscore.score
                    self.save_failed = not self.highscore.commit(self.total)
                else:
                    self.title(now)

    def draw(self, now):
        d = thumby.display
        d.fill(0)
        if self.state == TITLE:
            safe_blit(0, 0, "assets_ui_title.bin", 72, 32, -1)
            inverted = 1 if self.flash is not None else 0
            d.drawFilledRectangle(21, 27, 30, 7, inverted)
            label = "PRESS A" if (time.ticks_diff(now, self.entered) // 2000) % 2 == 0 else VERSION
            d.drawText(label, 36 - len(label) * 2, 28, 1 - inverted)
            hs = padded(self.highscore.score, 6) if self.highscore.ready else "------"
            d.drawText("HS:" + hs, 0, 35, 1)
            if self.highscore.error is not None:
                d.drawText("!", 38, 35, 1)
            d.drawText("AZ_aeon", 44, 35, 1)
        elif self.state == ANGEL_BOOK:
            entry = ANGELS[self.book_index]
            d.drawText(entry[0], 4, 2, 1)
            d.drawText(entry[1], 46, 2, 1)
            for i in range(len(self.book_lines)):
                d.drawText(self.book_lines[i], 2, 9 + i * 6, 1)
            elapsed = time.ticks_diff(now, self.book_frame_at)
            if elapsed >= 3000:
                self.book_frame = (self.book_frame + elapsed // 3000) % (len(ANGEL_FORMS[self.book_index]) * 3)
                self.book_frame_at = now - elapsed % 3000
                self.book_image_loaded = False
                clear_cache()
            if not self.book_image_loaded:
                self.book_image = catalog_angel_image(self.book_index, self.book_frame)
                self.book_image_loaded = True
            if self.book_image is not None:
                safe_blit(46, 11, self.book_image, 24, 24, -1)
            else:
                safe_blit(46, 11, entry[2], 24, 24, -1)
        elif self.state in (ENEMY_BOOK, AMMO_BOOK):
            enemy_book = self.state == ENEMY_BOOK
            entry = (ENEMIES if enemy_book else AMMO)[self.book_index]
            number = padded(self.book_index + 1, 2) + ("/30" if enemy_book else "/22")
            if enemy_book:
                d.drawText(entry[1], 4, 0, 1)
                d.drawText(entry[2], 22, 0, 1)
                d.drawText(number, 48, 0, 1)
                safe_blit(0, 8, entry[3], 40, 24, -1)
                d.drawText(entry[0][:18], 0, 35, 1)
            else:
                d.drawText(entry[2], 4, 2, 1)
                safe_blit(5, 8, entry[3], 13, 18, -1)
                d.drawText(entry[0], 2, 28, 1)
                d.drawText(number, 2, 35, 1)
            for i in range(len(self.book_lines)):
                d.drawText(self.book_lines[i], 44 if enemy_book else 23,
                           (6 if enemy_book else 3) + i * 6, 1)
        elif self.state == SELECT:
            for i in range(4):
                selected = 1 if i == self.course else 0
                d.drawFilledRectangle(10, 1 + i * 8, 24, 7, selected)
                d.drawText(COURSE_LABELS[i], 12, 2 + i * 8, 1 - selected)
            draw_character(self.menu_path, 46, 9)
            safe_blit(1, 35, "assets_ui_musica.bin", 5, 5, -1)
            d.drawText(BGM_NAMES[self.bgm], 8, 35, 1)
        elif self.state in (ENEMY, PICK):
            d.drawFilledRectangle(0, 0, 72, 6, 1)
            d.drawFilledRectangle(0, 34, 72, 6, 1)
            d.drawText(self.enemy[1], 0, 0, 0)
            d.drawText(self.enemy[2], 24, 0, 0)
            d.drawText(time_text(self.remaining), 52, 0, 0)
            if self.state == ENEMY:
                path = self.character_path
                if (path is not None and time.ticks_diff(now, self.entered) >= 2000
                        and not path[:-4].endswith("_act") and not path[:-4].endswith("_rslt")):
                    path = resolve_action_image(self.character[0], path)
                safe_blit(0, 8, self.enemy[3], 40, 24, -1)
                draw_character(path, 46, 9)
            else:
                for i in range(5):
                    x = 1 + i * 14
                    locked = i in self.locks
                    selected = i == self.cursor
                    ammo = AMMO[self.candidates[i]]
                    safe_blit(x, 7, ammo[3], 13, 18, -1)
                    inverted = locked or selected
                    if inverted:
                        get_pixel = d.getPixel
                        set_pixel = d.setPixel
                        for yy in range(7, 25):
                            for xx in range(x, x + 13):
                                set_pixel(xx, yy, 1 - get_pixel(xx, yy))
                    d.drawFilledRectangle(x, 25, 13, 7, 1 if inverted else 0)
                    d.drawText(ammo[0], x + (13 - (len(ammo[0]) * 4 - 1)) // 2,
                               26, 0 if inverted else 1)
                    if selected:
                        d.drawFilledRectangle(x, 32, 13, 1, 1)
            d.drawText(self.enemy[0][:18], 0, 35, 0)
        elif self.state == SCORE:
            d.drawFilledRectangle(0, 0, 72, 6, 1)
            d.drawFilledRectangle(0, 34, 72, 6, 1)
            d.drawText("WIN!", 10, 0, 0)
            d.drawText(time_text(self.remaining), 52, 0, 0)
            d.drawText("HIT " + str(self.hits) + "/3", 4, 9, 1)
            d.drawText(padded(self.points, 6), 4, 17, 1)
            d.drawText("T:" + padded(self.total, 6), 4, 25, 1)
            draw_character(self.result_path, 46, 9)
            d.drawText(self.enemy[0][:18], 0, 35, 0)
        elif self.state == END:
            heading = self.highscore.error if self.save_failed else ("HIGH SCORE !" if self.new_high else "SCORE")
            d.drawFilledRectangle(0, 0, 72, 6, 1)
            d.drawText(heading, 0 if self.save_failed or self.new_high else 22, 0, 0)
            hs = padded(self.highscore.score, 6) if self.highscore.ready else "------"
            d.drawText(padded(self.total, 6), 4, 17, 1)
            d.drawText("HS:" + hs, 4, 26, 1)
            draw_character(self.result_path, 46, 9)
            d.drawFilledRectangle(0, 34, 72, 6, 1)
            d.drawText("A:RETRY B:TITLE" if self.save_failed else "Thank you !!",
                       0 if self.save_failed else 12, 35, 0)

        # Invert the completed frame in place, including sprites and selection.
        # Official thumbyGraphics uses display.display.buffer (MONO_VLSB).
        buffer = getattr(getattr(d, "display", None), "buffer", None)
        if buffer is not None and len(buffer) == 360:
            for i in range(360):
                buffer[i] ^= 255
        else:
            # Compatibility path for displays without the standard buffer.
            get_pixel = d.getPixel
            set_pixel = d.setPixel
            for y in range(40):
                for x in range(72):
                    set_pixel(x, y, 1 - get_pixel(x, y))


def run():
    d = thumby.display
    d.setFPS(60)
    d.setFont("/lib/font3x5.bin", 3, 5, 1)
    buttons = (thumby.buttonA, thumby.buttonB, thumby.buttonU,
               thumby.buttonD, thumby.buttonL, thumby.buttonR)
    game = Game(time.ticks_ms())
    previous = 0
    armed = False
    frames = 0
    print("ROUND", VERSION, "start")
    try:
        while True:
            now = time.ticks_ms()
            held = 0
            for i in range(6):
                if buttons[i].pressed():
                    held |= 1 << i
            pressed = held & ~previous
            previous = held
            if not armed:
                pressed = 0
                if held == 0:
                    armed = True
            game.step(now, pressed, held)
            game.sound.update(time.ticks_ms())
            game.draw(now)
            game.sound.update(time.ticks_ms())
            d.update()
            frames += 1
            if frames >= 300:
                gc.collect()
                print("ROUND free:", gc.mem_free(), "state:", game.state,
                      "remaining_ms:", game.remaining, "total:", game.total)
                frames = 0

    finally:
        game.sound.stop()


run()
