import time
import thumby
import math
import random
import machine

#set FPS to 60
thumby.display.setFPS(60)

def TitleScreen():
    # BITMAP: width: 6, height: 27
#    by_xyvir = bytearray([248,169,223,174,249,254,
#               255,235,247,251,255,255,
#               255,190,221,238,255,255,
#               7,7,5,2,7,7])
           
#    by_xyvirSprite = thumby.Sprite(6, 27, by_xyvir, 61, 2,1)
           
    # BITMAP: width: 72, height: 12
    mountains = bytearray([15,7,3,3,3,1,1,1,3,3,3,3,3,3,3,7,15,7,3,3,3,1,1,0,0,0,1,3,3,1,1,1,0,3,7,15,3,1,1,3,1,1,1,0,1,1,3,3,7,15,15,15,15,7,7,3,3,3,7,3,3,3,3,3,7,15,15,15,15,15,7,7,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
           
    mountainsSprite1 = thumby.Sprite(72, 12, mountains, 0, 28,1)  
    mountainsSprite2 = thumby.Sprite(72, 12, mountains, 72, 28,1) 

    # BITMAP: width: 31, height: 34
    summit = bytearray([255,255,255,255,255,255,255,255,255,127,31,127,63,127,63,128,143,191,191,63,127,255,255,255,255,255,255,255,255,255,255,
               255,255,255,255,255,255,255,255,255,240,7,237,239,231,174,235,235,232,235,131,48,255,255,255,255,255,255,255,255,255,255,
               255,255,255,255,255,255,63,31,7,0,1,1,1,1,134,143,217,81,97,0,0,1,15,31,63,127,255,255,255,255,255,
               255,255,255,63,1,0,0,0,0,0,0,12,2,33,33,192,0,0,0,0,0,0,0,3,6,4,31,63,127,255,255,
               3,3,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3])
           
    summitSprite = thumby.Sprite(31,34, summit, 34, 6)
           
    # BITMAP: width: 31, height: 34
    summit_mask = bytearray([0,0,0,0,0,0,0,0,0,128,224,128,192,128,192,255,240,192,192,192,128,0,0,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,15,255,255,255,255,255,255,255,255,255,255,207,0,0,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,192,224,248,255,255,255,255,255,255,255,255,255,255,255,255,254,240,224,192,128,0,0,0,0,0,
               0,0,224,224,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,248,240,224,128,0,
               2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2])
           
    summit_maskSprite = thumby.Sprite(31,34, summit_mask)      
    # BITMAP: width: 40, height: 40
    sun = bytearray([0,0,0,0,0,128,192,224,240,248,248,252,252,254,254,254,255,255,255,255,255,255,255,255,254,254,254,252,252,248,248,240,224,192,128,0,0,0,0,0,
               128,240,248,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,248,240,128,
               255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
               1,15,31,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,31,15,1,
               0,0,0,0,0,1,3,7,15,31,31,63,63,127,127,127,255,255,255,255,255,255,255,255,127,127,127,63,63,31,31,15,7,3,1,0,0,0,0,0])

    sunSprite = thumby.Sprite(40,40, sun, 2, -10,0)           
           
    # BITMAP: width: 39, height: 25
    title = bytearray([0,0,255,255,255,255,255,255,255,127,191,191,191,127,127,255,239,1,0,239,255,239,1,0,239,239,255,127,63,191,191,127,127,255,63,127,191,191,63,
               120,48,215,215,215,215,151,55,255,248,246,246,246,242,250,255,255,48,16,255,255,255,48,16,255,255,255,248,240,246,246,242,250,255,240,240,255,255,255,
               158,28,249,251,251,243,103,15,255,15,215,215,215,79,79,255,253,0,0,253,255,253,0,0,253,253,255,15,7,215,215,79,79,255,7,15,247,247,231,
               1,1,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,1,0,0,0,0,1,1,0,0,1,1,1])
           
           
    titleSprite = thumby.Sprite(39,25, title, 3, 2,1) 

    TitleSong = [554, 329, 493, 329, 466, 329, 415, 329, 415, 311, 247, 415, 392, 277, 466, 392, 415, 415, 415, 415, 554, 311, 466, 311 , 523,523,523,523]

    width = 0
    speed = 15
    lineystart = 350
    Animstart = time.ticks_ms()
    #Title Screen Loop
    while(thumby.buttonB.pressed() == False):
        Animnow = time.ticks_ms() - Animstart
        tempo = int(Animnow/300)
        if tempo < len(TitleSong): 
            thumby.audio.play(TitleSong[tempo], 100)
        thumby.display.fill(0)
        if Animnow > 5250:
           width = width + 6
        if Animnow > 6200:
           thumby.display.fill(1)
        thumby.display.drawSprite(sunSprite)
        liney = int(lineystart-(Animnow/speed))
        thumby.display.drawFilledRectangle(22-int(width/2), liney, 1+width, 160, 1)
        thumby.display.drawSprite(titleSprite)
        mountainsSprite1.x = 0  - (72 - tempo % 72)
        mountainsSprite2.x = 72 - (72 - tempo % 72)
        thumby.display.drawSprite(mountainsSprite1)
        thumby.display.drawSprite(mountainsSprite2)
        thumby.display.drawSpriteWithMask(summitSprite, summit_maskSprite)
        sunSprite.y = sunSprite.y + (Animnow/ 12000)
        thumby.display.update()
        
TitleScreen()


#Create List StartingWords
StartingWords = ["FOR", "NOT", "WAS", "BuT", "GET", "HER", "CAN", "NOW", "HIM", "HOW", "GOT", "DID", "HEY", "HES", "YES", "HIS", "HAD", "SAY", "WAY", "LET", "MAN", "HAS", "GOD", "DAY", "PuT", "GuY", "BIG", "LOT", "NEW", "BAD", "MOM", "DAD", "SON", "SAW", "SIR", "JOB", "BOY", "CAR", "YET", "FEW", "RuN", "SIT", "FuN", "KID", "BIT", "SET", "FAR", "DIE", "HIT", "PAY", "MEN", "BED", "CuT", "MET", "HOT", "SIX", "BET", "LIE", "TEN", "BuY", "MAD", "GuN", "TOP", "LAW", "WED", "DOG", "WIN"]

#Create LegalWords Dictionary
class LegalWords:
    A = ["AAH", "AAL", "AAS", "ABA", "ABB", "ABO", "ABS", "ABY", "ACE", "ACH", "ACT", "ADD", "ADO", "ADS", "ADZ", "AFF", "AFT", "AGA", "AGE", "AGO", "AGS", "AHA", "AHI", "AHS", "AIA", "AID", "AIL", "AIM", "AIN", "AIR", "AIS", "AIT", "AKA", "AKE", "ALA", "ALB", "ALE", "ALF", "ALL", "ALP", "ALS", "ALT", "ALu", "AMA", "AME", "AMI", "AMP", "AMu", "ANA", "AND", "ANE", "ANI", "ANN", "ANS", "ANT", "ANY", "APE", "APO", "APP", "APT", "ARB", "ARC", "ARD", "ARE", "ARF", "ARK", "ARM", "ARS", "ART", "ARY", "ASH", "ASK", "ASP", "ASS", "ATE", "ATS", "ATT", "AuA", "AuE", "AuF", "AuK", "AVA", "AVE", "AVO", "AWA", "AWE", "AWK", "AWL", "AWN", "AXE", "AYE", "AYS", "AYu", "AZO"]
    B = ["BAA", "BAC", "BAD", "BAG", "BAH", "BAL", "BAM", "BAN", "BAP", "BAR", "BAS", "BAT", "BAY", "BED", "BEE", "BEG", "BEL", "BEN", "BES", "BET", "BEY", "BEZ", "BIB", "BID", "BIG", "BIN", "BIO", "BIS", "BIT", "BIZ", "BOA", "BOB", "BOD", "BOG", "BOH", "BOI", "BOK", "BON", "BOO", "BOP", "BOR", "BOS", "BOT", "BOW", "BOX", "BOY", "BRA", "BRO", "BRR", "BRu", "BuB", "BuD", "BuG", "BuM", "BuN", "BuR", "BuS", "BuT", "BuY", "BYE", "BYS"]
    C = ["CAA", "CAB", "CAD", "CAG", "CAM", "CAN", "CAP", "CAR", "CAT", "CAW", "CAY", "CAZ", "CEE", "CEL", "CEP", "CHA", "CHE", "CHI", "CID", "CIG", "CIS", "CIT", "CLY", "COB", "COD", "COG", "COL", "CON", "COO", "COP", "COR", "COS", "COT", "COW", "COX", "COY", "COZ", "CRu", "CRY", "CuB", "CuD", "CuE", "CuM", "CuP", "CuR", "CuT", "CuZ", "CWM"]
    D = ["DAB", "DAD", "DAE", "DAG", "DAH", "DAK", "DAL", "DAM", "DAN", "DAP", "DAS", "DAW", "DAY", "DEB", "DEE", "DEF", "DEG", "DEI", "DEL", "DEN", "DEV", "DEW", "DEX", "DEY", "DIB", "DID", "DIE", "DIF", "DIG", "DIM", "DIN", "DIP", "DIS", "DIT", "DIV", "DOB", "DOC", "DOD", "DOE", "DOF", "DOG", "DOH", "DOL", "DOM", "DON", "DOO", "DOP", "DOR", "DOS", "DOT", "DOW", "DOY", "DRY", "DSO", "DuB", "DuD", "DuE", "DuG", "DuH", "DuI", "DuN", "DuO", "DuP", "DuX", "DYE", "DZO"]
    E = ["EAN", "EAR", "EAS", "EAT", "EAu", "EBB", "ECH", "ECO", "ECu", "EDH", "EDS", "EEK", "EEL", "EEN", "EFF", "EFS", "EFT", "EGG", "EGO", "EHS", "EIK", "EKE", "ELD", "ELF", "ELK", "ELL", "ELM", "ELS", "ELT", "EME", "EMO", "EMS", "EMu", "END", "ENE", "ENG", "ENS", "EON", "ERA", "ERE", "ERF", "ERG", "ERK", "ERM", "ERN", "ERR", "ERS", "ESS", "EST", "ETA", "ETH", "EuK", "EVE", "EVO", "EWE", "EWK", "EWT", "EXO", "EYE"]
    F = ["FAA", "FAB", "FAD", "FAE", "FAG", "FAH", "FAN", "FAP", "FAR", "FAS", "FAT", "FAW", "FAX", "FAY", "FED", "FEE", "FEG", "FEH", "FEM", "FEN", "FER", "FES", "FET", "FEu", "FEW", "FEY", "FEZ", "FIB", "FID", "FIE", "FIG", "FIL", "FIN", "FIR", "FIT", "FIX", "FIZ", "FLu", "FLY", "FOB", "FOE", "FOG", "FOH", "FON", "FOP", "FOR", "FOu", "FOX", "FOY", "FRA", "FRO", "FRY", "FuB", "FuD", "FuG", "FuM", "FuN", "FuR"]
    G = ["GAB", "GAD", "GAE", "GAG", "GAK", "GAL", "GAM", "GAN", "GAP", "GAR", "GAS", "GAT", "GAu", "GAW", "GAY", "GED", "GEE", "GEL", "GEM", "GEN", "GEO", "GER", "GET", "GEY", "GHI", "GIB", "GID", "GIE", "GIF", "GIG", "GIN", "GIO", "GIP", "GIS", "GIT", "GJu", "GNu", "GOA", "GOB", "GOD", "GOE", "GON", "GOO", "GOR", "GOS", "GOT", "GOV", "GOX", "GOY", "GuB", "GuE", "GuL", "GuM", "GuN", "GuP", "GuR", "GuS", "GuT", "GuV", "GuY", "GYM", "GYP"]
    H = ["HAD", "HAE", "HAG", "HAH", "HAJ", "HAM", "HAN", "HAO", "HAP", "HAS", "HAT", "HAW", "HAY", "HEH", "HEM", "HEN", "HEP", "HER", "HES", "HET", "HEW", "HEX", "HEY", "HIC", "HID", "HIE", "HIM", "HIN", "HIP", "HIS", "HIT", "HMM", "HOA", "HOB", "HOC", "HOD", "HOE", "HOG", "HOH", "HOI", "HOM", "HON", "HOO", "HOP", "HOS", "HOT", "HOW", "HOX", "HOY", "HuB", "HuE", "HuG", "HuH", "HuI", "HuM", "HuN", "HuP", "HuT", "HYE", "HYP"]
    I = ["ICE", "ICH", "ICK", "ICY", "IDE", "IDS", "IFF", "IFS", "IGG", "ILK", "ILL", "IMP", "ING", "INK", "INN", "INS", "ION", "IOS", "IRE", "IRK", "ISH", "ISM", "ISO", "ITA", "ITS", "IVY", "IWI"]
    J = ["JAB", "JAG", "JAI", "JAK", "JAM", "JAP", "JAR", "JAW", "JAY", "JEE", "JET", "JEu", "JEW", "JIB", "JIG", "JIN", "JIZ", "JOB", "JOE", "JOG", "JOL", "JOR", "JOT", "JOW", "JOY", "JuD", "JuG", "JuN", "JuS", "JuT"]
    K = ["KAB", "KAE", "KAF", "KAI", "KAK", "KAM", "KAS", "KAT", "KAW", "KAY", "KEA", "KEB", "KED", "KEF", "KEG", "KEN", "KEP", "KET", "KEX", "KEY", "KHI", "KID", "KIF", "KIN", "KIP", "KIR", "KIS", "KIT", "KOA", "KOB", "KOI", "KON", "KOP", "KOR", "KOS", "KOW", "KuE", "KYE", "KYu"]
    L = ["LAB", "LAC", "LAD", "LAG", "LAH", "LAM", "LAP", "LAR", "LAS", "LAT", "LAV", "LAW", "LAX", "LAY", "LEA", "LED", "LEE", "LEG", "LEI", "LEK", "LEP", "LES", "LET", "LEu", "LEV", "LEW", "LEX", "LEY", "LEZ", "LIB", "LID", "LIE", "LIG", "LIN", "LIP", "LIS", "LIT", "LOB", "LOD", "LOG", "LOO", "LOP", "LOR", "LOS", "LOT", "LOu", "LOW", "LOX", "LOY", "LuD", "LuG", "LuM", "LuR", "LuV", "LuX", "LuZ", "LYE", "LYM"]
    M = ["MAA", "MAC", "MAD", "MAE", "MAG", "MAK", "MAL", "MAM", "MAN", "MAP", "MAR", "MAS", "MAT", "MAW", "MAX", "MAY", "MED", "MEE", "MEG", "MEH", "MEL", "MEM", "MEN", "MES", "MET", "MEu", "MEW", "MHO", "MIB", "MIC", "MID", "MIG", "MIL", "MIM", "MIR", "MIS", "MIX", "MIZ", "MNA", "MOA", "MOB", "MOC", "MOD", "MOE", "MOG", "MOI", "MOL", "MOM", "MON", "MOO", "MOP", "MOR", "MOS", "MOT", "MOu", "MOW", "MOY", "MOZ", "MuD", "MuG", "MuM", "MuN", "MuS", "MuT", "MuX", "MYC"]
    N = ["NAB", "NAE", "NAG", "NAH", "NAM", "NAN", "NAP", "NAS", "NAT", "NAW", "NAY", "NEB", "NED", "NEE", "NEF", "NEG", "NEK", "NEP", "NET", "NEW", "NIB", "NID", "NIE", "NIL", "NIM", "NIP", "NIS", "NIT", "NIX", "NOB", "NOD", "NOG", "NOH", "NOM", "NON", "NOO", "NOR", "NOS", "NOT", "NOW", "NOX", "NOY", "NTH", "NuB", "NuN", "NuR", "NuS", "NuT", "NYE", "NYS"]
    O = ["OAF", "OAK", "OAR", "OAT", "OBA", "OBE", "OBI", "OBO", "OBS", "OCA", "OCH", "ODA", "ODD", "ODE", "ODS", "OES", "OFF", "OFT", "OHM", "OHO", "OHS", "OIK", "OIL", "OIS", "OKA", "OKE", "OLD", "OLE", "OLM", "OMS", "ONE", "ONO", "ONS", "ONY", "OOF", "OOH", "OOM", "OON", "OOP", "OOR", "OOS", "OOT", "OPE", "OPS", "OPT", "ORA", "ORB", "ORC", "ORD", "ORE", "ORF", "ORS", "ORT", "OSE", "OuD", "OuK", "OuP", "OuR", "OuS", "OuT", "OVA", "OWE", "OWL", "OWN", "OWT", "OXO", "OXY", "OYE", "OYS"]
    P = ["PAC", "PAD", "PAH", "PAL", "PAM", "PAN", "PAP", "PAR", "PAS", "PAT", "PAV", "PAW", "PAX", "PAY", "PEA", "PEC", "PED", "PEE", "PEG", "PEH", "PEL", "PEN", "PEP", "PER", "PES", "PET", "PEW", "PHI", "PHO", "PHT", "PIA", "PIC", "PIE", "PIG", "PIN", "PIP", "PIR", "PIS", "PIT", "PIu", "PIX", "PLu", "PLY", "POA", "POD", "POH", "POI", "POL", "POM", "POO", "POP", "POS", "POT", "POW", "POX", "POZ", "PRE", "PRO", "PRY", "PSI", "PST", "PuB", "PuD", "PuG", "PuH", "PuL", "PuN", "PuP", "PuR", "PuS", "PuT", "PuY", "PYA", "PYE", "PYX"]
    Q = ["QAT", "QIN", "QIS", "QuA"]
    R = ["RAD", "RAG", "RAH", "RAI", "RAJ", "RAM", "RAN", "RAP", "RAS", "RAT", "RAV", "RAW", "RAX", "RAY", "REB", "REC", "RED", "REE", "REF", "REG", "REH", "REI", "REM", "REN", "REO", "REP", "RES", "RET", "REV", "REW", "REX", "REZ", "RHO", "RHY", "RIA", "RIB", "RID", "RIF", "RIG", "RIM", "RIN", "RIP", "RIT", "RIZ", "ROB", "ROC", "ROD", "ROE", "ROK", "ROM", "ROO", "ROT", "ROW", "RuB", "RuC", "RuD", "RuE", "RuG", "RuM", "RuN", "RuT", "RYA", "RYE"]
    S = ["SAB", "SAC", "SAD", "SAE", "SAG", "SAI", "SAL", "SAM", "SAN", "SAP", "SAR", "SAT", "SAu", "SAV", "SAW", "SAX", "SAY", "SAZ", "SEA", "SEC", "SED", "SEE", "SEG", "SEI", "SEL", "SEN", "SER", "SET", "SEW", "SEX", "SEY", "SEZ", "SHA", "SHE", "SHH", "SHY", "SIB", "SIC", "SIF", "SIK", "SIM", "SIN", "SIP", "SIR", "SIS", "SIT", "SIX", "SKA", "SKI", "SKY", "SLY", "SMA", "SNY", "SOB", "SOC", "SOD", "SOG", "SOH", "SOL", "SOM", "SON", "SOP", "SOS", "SOT", "SOu", "SOV", "SOW", "SOX", "SOY", "SOZ", "SPA", "SPY", "SRI", "STY", "SuB", "SuD", "SuE", "SuG", "SuI", "SuK", "SuM", "SuN", "SuP", "SuQ", "SuR", "SuS", "SWY", "SYE", "SYN"]
    T = ["TAB", "TAD", "TAE", "TAG", "TAI", "TAJ", "TAK", "TAM", "TAN", "TAO", "TAP", "TAR", "TAS", "TAT", "TAu", "TAV", "TAW", "TAX", "TAY", "TEA", "TEC", "TED", "TEE", "TEF", "TEG", "TEL", "TEN", "TES", "TET", "TEW", "TEX", "THE", "THO", "THY", "TIC", "TID", "TIE", "TIG", "TIK", "TIL", "TIN", "TIP", "TIS", "TIT", "TIX", "TOC", "TOD", "TOE", "TOG", "TOM", "TON", "TOO", "TOP", "TOR", "TOT", "TOW", "TOY", "TRY", "TSK", "TuB", "TuG", "TuI", "TuM", "TuN", "TuP", "TuT", "TuX", "TWA", "TWO", "TWP", "TYE", "TYG"]
    u = ["uDO", "uDS", "uEY", "uFO", "uGH", "uGS", "uKE", "uLE", "uLu", "uMM", "uMP", "uMS", "uMu", "uNI", "uNS", "uPO", "uPS", "uRB", "uRD", "uRE", "uRN", "uRP", "uSE", "uTA", "uTE", "uTS", "uTu", "uVA"]
    V = ["VAC", "VAE", "VAG", "VAN", "VAR", "VAS", "VAT", "VAu", "VAV", "VAW", "VEE", "VEG", "VET", "VEX", "VIA", "VID", "VIE", "VIG", "VIM", "VIN", "VIS", "VLY", "VOE", "VOL", "VOR", "VOW", "VOX", "VuG", "VuM"]
    W = ["WAB", "WAD", "WAE", "WAG", "WAI", "WAN", "WAP", "WAR", "WAS", "WAT", "WAW", "WAX", "WAY", "WEB", "WED", "WEE", "WEM", "WEN", "WET", "WEX", "WEY", "WHA", "WHO", "WHY", "WIG", "WIN", "WIS", "WIT", "WIZ", "WOE", "WOF", "WOG", "WOK", "WON", "WOO", "WOP", "WOS", "WOT", "WOW", "WOX", "WRY", "WuD", "WuS", "WYE", "WYN"]
    X = ["XIS"]
    Y = ["YAD", "YAE", "YAG", "YAH", "YAK", "YAM", "YAP", "YAR", "YAW", "YAY", "YEA", "YEH", "YEN", "YEP", "YES", "YET", "YEW", "YEX", "YGO", "YID", "YIN", "YIP", "YOB", "YOD", "YOK", "YOM", "YON", "YOu", "YOW", "YuG", "YuK", "YuM", "YuP", "YuS"]
    Z = ["ZAG", "ZAP", "ZAS", "ZAX", "ZEA", "ZED", "ZEE", "ZEK", "ZEL", "ZEP", "ZEX", "ZHO", "ZIG", "ZIN", "ZIP", "ZIT", "ZIZ", "ZOA", "ZOL", "ZOO", "ZOS", "ZuZ", "ZZZ"]

#List for full alphabet  
ALPHA = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", 
"T", "u", "V", "W", "X", "Y", "Z"]  


#Generate list of pixel-perfect starting positions per each letter
AlphaNum = []
AlphaNumStep = 280
for z in range(26, 0, -1):
        # Total Row Height minus  Horizontal Offset (Letter A first) minus Vertical Offset
        AlphaNum.append(int((z * AlphaNumStep) - (3*AlphaNumStep) - 12))

#Sqaure Selector box gfx
bitmap0 = bytearray([254,1,1,1,1,1,1,1,254,3,4,4,4,4,4,4,4,3])

#Inverse Square Selector box BITMAP: width: 9, height: 11
bitmap1 = bytearray([254,255,255,255,255,255,255,255,254,
           3,7,7,7,7,7,7,7,3])
           
#Bonus Egg Sprite
# BITMAP: width: 10, height: 10
bitmap2 = bytearray([15,243,253,254,254,254,254,253,243,15,
           3,2,1,1,1,1,1,1,2,3])


#Copy Selector Box Sprite 4x
thumbySpriteMain = thumby.Sprite(9, 11, bitmap0)
thumbySprite1 = thumby.Sprite(9, 11, bitmap0)
thumbySprite2 = thumby.Sprite(9, 11, bitmap0)
thumbySprite3 = thumby.Sprite(9, 11, bitmap0)
EggSprite = thumby.Sprite(10, 10, bitmap2)

#Copy Inverse Selector Box
thumbySpriteReverse1 = thumby.Sprite(9, 11, bitmap1)
thumbySpriteReverse2 = thumby.Sprite(9, 11, bitmap1)
thumbySpriteReverse3 = thumby.Sprite(9, 11, bitmap1)

x = int((thumby.display.width/2) - 28)
y = int(round(thumby.display.height/2)) - 4

thumbySprite1.x = 7 
thumbySprite1.y = y-2

thumbySprite2.x = 31 
thumbySprite2.y = y-2

thumbySprite3.x = 55 
thumbySprite3.y = y-2

thumbySpriteReverse1.x = 7 
thumbySpriteReverse1.y = y-2

thumbySpriteReverse2.x = 31 
thumbySpriteReverse2.y = y-2

thumbySpriteReverse3.x = 55 
thumbySpriteReverse3.y = y-2

EggSprite.x = 49
EggSprite.y = 0

#Smaller is Faster
ScrollRate = 35

delta = 0
PlayfieldWord = None
ModTime = 0
bonus = -1

def ClearVars():
    
    global CurLegalWords
    global Playfield
    global PressedLast     
    global direction 
    global delta2 
    global turn 
    global strscore 
    global ActiveColumns 
    global CurAlpha
    global CurAlpha2
    global CurTimer
    global WrongGuessTimer
    global lenscore

#Copy LegalWords Class to create dictionary
    CurLegalWords = LegalWords
    
#Create clean CurAlpha    
    CurAlpha = ALPHA.copy()
    CurAlpha2 = CurAlpha[-5:] + CurAlpha
    

#Select starting word from dictionary and remove it via POP
    random.seed(time.ticks_us())    
    RandomWord = random.choice(StartingWords)

#Turn word string into array.
    Playfield = list(RandomWord)

#init variables
    CurTimer = time.ticks_ms()
    PressedLast = ""    
    direction = 0
    delta2 = 0
    turn = 0
    strscore = "0"
    if bonus < 0:
        ActiveColumns = [0,1,2]
    else:
        ActiveColumns = [2,1,0]
    WrongGuessTimer = 0
    lenscore = 1
    


def CurAlphaRemove():
    global CurAlpha
    global CurAlpha2
    if score > 0:
        CurAlpha = ALPHA.copy()
        CurLetterChar = Playfield[ActiveColumns[turn % len(ActiveColumns)]]
        CurLetterNumber = ALPHA.index(CurLetterChar)
        CurAlpha[CurLetterNumber] = "-"
        CurAlpha2 = CurAlpha[-5:] + CurAlpha
    return
    


ClearVars()
ScrollAnimTimer1 = AlphaNum[ALPHA.index(Playfield[ActiveColumns[turn % len(ActiveColumns)]])]  
################################## Main Game Loop   #################################### 
while(1):
    
    #Stop on B Button

        # ModTime for Stop Directly on Letter 
    if PressedLast == "B" and (ModTime  % 8) == 0:
        direction = 0

    if thumby.buttonB.pressed():
        #Slow for approach
        if direction < 0:
            direction = -.75
        if direction > 0:
            direction = .75
        PressedLast = "B"
        
        
    #Select Letter on A button, ModTime for stop directly on letter
        
    if PressedLast == "a" and thumby.buttonB.pressed() == False and (ModTime  % 8) == 0 and not CurAlpha[CurLetter] == "-":
        PressedLast = "A"
        direction = 0
        TempPlayfield = None
        TempPlayfield = Playfield.copy()
        TempPlayfield[ActiveColumns[turn % len(ActiveColumns)]] = CurAlpha[CurLetter]
        PlayfieldWord = ''.join(TempPlayfield)
        LegalWord = getattr(CurLegalWords, TempPlayfield[0])
        if PlayfieldWord in LegalWord:
            thumby.audio.playBlocking(494, 100)
            thumby.audio.playBlocking(392, 150)
            Playfield[ActiveColumns[turn % len(ActiveColumns)]] = CurAlpha[CurLetter]
            LegalWord.pop(LegalWord.index(PlayfieldWord))
            turn = turn + 1
            score = turn - (3-len(ActiveColumns))
            if score % 100 == 0:
                bonus = bonus + 1
            strscore = str(score)
            lenscore = len(strscore)
            CurAlphaRemove()
            ScrollAnimTimer1 = AlphaNum[ALPHA.index(Playfield[ActiveColumns[turn % len(ActiveColumns)]])]
            CurTimer = time.ticks_ms()
        else:
            WrongGuessTimer = delta + 1200
            
                
        
    if thumby.buttonA.pressed() and PressedLast != "A":
        #Slow for approach
        if direction < 0:
            direction = -.75
        if direction > 0:
            direction = .75
        PressedLast = "a"

    #Play Letter Selector Noise
    if (ModTime  % 8) > 4 and direction != 0:
            thumby.audio.play(247, 50)

    #Main Time Calculation for Text Selector Animation
    if time.ticks_ms() > delta:
        delta2 = time.ticks_ms() - delta
        ScrollAnimTimer1 = ScrollAnimTimer1 + int(direction * delta2)
        delta = time.ticks_ms()
       
    
  


#Up and Down inputs / double tap detection

    if PressedLast == "uu" and thumby.buttonU.pressed() == False:
        direction = -2
        PressedLast = "UU"
        
    if PressedLast == "u" and thumby.buttonU.pressed() == False:
        direction = -1
        PressedLast = "U"
            
    if thumby.buttonU.pressed() and PressedLast != "uu":
        if PressedLast == "U":
            PressedLast = "uu"
        else:
            PressedLast = "u"
       
    if PressedLast == "dd" and thumby.buttonD.pressed() == False:
        direction = 2
        PressedLast = "DD"
        
    if PressedLast == "d" and thumby.buttonD.pressed() == False:
        direction = 1
        PressedLast = "D"
            
    if thumby.buttonD.pressed() and PressedLast != "dd":
        if PressedLast == "D":
            PressedLast = "dd"
        else:
            PressedLast = "d"
            
        


       

    
#################### Render Display ########################################    
    thumby.display.fill(0) # Fill canvas to black

    #Calculate center values:
    xprime = int((thumby.display.width/2) - 28) + (ActiveColumns[(turn % len(ActiveColumns))] * 24)
    y = int(round(thumby.display.height/2)) - 4
    bobOffset = int(math.sin(delta / 50) * 4)
    
    #Wrong Guess Animation / SOund 
    if WrongGuessTimer > delta:
        x = xprime + bobOffset
        thumby.audio.play(150 + (bobOffset * 10), 50)
        PressedLast = ""
    else:
        x = xprime 
        
    
    #Cycle thru alpha based on gametime# BITMAP: width: 9, height: 11
    ModTime = ((ScrollAnimTimer1//ScrollRate) % 208)+ 1
    CurLetter = 25 - ((ModTime + 20) // 8 % 26)
    
	#Draw timebar
    thumby.display.drawLine(0, 39, 71, 39, 1)
    
    #Shrink Timebar
    shrinkrate = len(ActiveColumns) * (4.75 - (bonus * .25))
    shrinkx = 71 - int((72 / shrinkrate) * ((delta - CurTimer)/1000))
    thumby.display.drawLine(71, 39, shrinkx, 39, 0)
    
    
    
    #Freeze Column when Timer runs out
    if shrinkx == 0:
            thumby.audio.playBlocking(100, 50)
            thumby.audio.playBlocking(80, 200)
            ActiveColumns.pop(turn % len(ActiveColumns))
            turn = turn + 1
            score = turn - (3-len(ActiveColumns))
            strscore = str(score)
            lenscore = len(strscore)
            CurTimer = time.ticks_ms()
            
            #Correct order as needed
            if ((turn+5) % 6) < 3:
                ActiveColumns.reverse()
            
            #Check for Game Over / Game Over Screen
            if len(ActiveColumns) == 0:
                #Play Music
                thumby.display.fill(1)
                thumby.display.drawText("Game Over!",7,9,0)
                thumby.display.update()
                thumby.audio.playBlocking(392, 300)
                for i in range(6):
                    thumby.audio.playBlocking(415, 70)
                    thumby.audio.playBlocking(392, 70)
                thumby.audio.playBlocking(349, 600)
                thumby.audio.playBlocking(392, 600)
                thumby.audio.playBlocking(415, 1200)
                #Game Over Loop
                while(thumby.buttonB.pressed() == False):
                    thumby.display.fill(1)
                    thumby.display.drawText(strscore,0,0,0)
                    thumby.display.drawText("Game Over!",7,9,0)
                    thumby.display.drawText("B: Again?",14,21,0)
                    thumby.display.drawText("A>+B: Quit",7,30,0)
                    if bonus > 0:
                        thumby.display.drawText(str(bonus),60,1,0)
                        print(str(bonus))
                    if bonus > -1:
                        thumby.display.drawSprite(EggSprite)
                    thumby.display.update()
                if thumby.buttonA.pressed():
                    machine.reset()
                ClearVars()
            else:
                CurAlphaRemove()  
                
              
            ScrollAnimTimer1 = AlphaNum[ALPHA.index(Playfield[ActiveColumns[turn % len(ActiveColumns)]])]
            direction = 0
        

    
    
    #Draw Current Word Letters & their Bounding Boxes
    
    if 0 in ActiveColumns:
        thumby.display.drawSprite(thumbySprite1)
        thumby.display.drawText(Playfield[0],  9, y, 1)
    else:
        thumby.display.drawSprite(thumbySpriteReverse1)
        thumby.display.drawText(Playfield[0],  9, y, 0)
        
    if 1 in ActiveColumns:
        thumby.display.drawSprite(thumbySprite2)
        thumby.display.drawText(Playfield[1],  33, y, 1)
    else:
        thumby.display.drawSprite(thumbySpriteReverse2)
        thumby.display.drawText(Playfield[1],  33, y, 0)
    
    if 2 in ActiveColumns:
        thumby.display.drawSprite(thumbySprite3)
        thumby.display.drawText(Playfield[2],  57, y, 1)
    else:
        thumby.display.drawSprite(thumbySpriteReverse3)
        thumby.display.drawText(Playfield[2],  57, y, 0)
    
    #Left and right Current Letter Highligher
    thumby.display.drawText(CurAlpha[CurLetter], x-7, y, 1)
    thumby.display.drawText(CurAlpha[CurLetter], x+9, y, 1)
    
    #Draw Selctor Boxes
    thumbySpriteMain.x = x-1
    thumbySpriteMain.y = y-2
    thumby.display.drawSprite(thumbySpriteMain)
    
    #Draw Vertical Text Selector
    
     
    for z in range(31):
        thumby.display.drawText(CurAlpha2[z], x+1, ModTime + (z*8)-208, 1)
    
    #Draw Score
        #strscore = str(score)
        if ActiveColumns[(turn % len(ActiveColumns))] != 0:
            thumby.display.drawText(strscore,0,0,1)
            
        if ActiveColumns[(turn % len(ActiveColumns))] != 2:
            thumby.display.drawText(strscore,72-(lenscore *6),0,1)
    
   
    thumby.display.update()
