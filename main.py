import engine_main
import engine
import engine_draw
import engine_io

engine.fps_limit(60)
fb = engine_draw.back_fb()

W, H = 128, 128
PW, PH = 10, 14
SPEED, GRAVITY, JUMP, MAX_FALL = 1.75, 0.34, -6.1, 6.5

SKY=0x867D; SUN=0xFFE0; WHITE=0xFFFF; PINK=0xFE19
DARK_PINK=0xF810; DIRT=0xA285; GRASS=0x07E0; DARK_GRASS=0x03E0
PURPLE=0x780F; YELLOW=0xFFE0; BLACK=0x0000; BLUE=0x001F; RED=0xF800

# moving platform: x,y,width,axis,min,max,speed,direction
LEVELS = [
 {"name":"SUNNY MEADOW","width":620,
  "platforms":[(0,112,150,16),(184,112,120,16),(340,112,115,16),(500,112,120,16),
               (60,84,45,8),(235,76,48,8),(385,70,45,8),(535,80,45,8)],
  "moving":[[145,91,36,"x",140,195,.55,1],[446,88,38,"y",65,96,.38,-1]],
  "coins":[(79,67),(164,73),(254,59),(361,94),(405,53),(467,62),(554,63)],
  "enemies":[(112,102,"snail",92,138,1),(250,66,"caterpillar",238,270,1),
             (370,102,"mushroom",348,430,-1),(548,70,"spiky",537,567,1)]},
 {"name":"BLOSSOM BROOK","width":700,
  "platforms":[(0,112,125,16),(180,112,105,16),(330,112,100,16),(485,112,90,16),
               (625,112,75,16),(76,78,42,8),(218,69,42,8),(367,62,46,8),
               (515,76,42,8),(636,57,42,8)],
  "moving":[[127,93,42,"x",125,182,.68,1],[286,84,42,"y",61,96,.48,-1],
            [432,88,46,"x",430,489,.72,-1],[577,82,40,"y",57,94,.42,1]],
  "coins":[(95,61),(146,75),(237,52),(307,52),(389,45),(454,69),(535,59),(596,51),(655,40)],
  "enemies":[(82,102,"snail",55,112,1),(225,59,"spiky",219,247,-1),
             (350,102,"mushroom",340,414,1),(520,66,"caterpillar",516,544,-1),
             (650,102,"spiky",638,680,1)]},
 {"name":"RAINBOW HEIGHTS","width":760,
  "platforms":[(0,112,105,16),(165,112,90,16),(315,112,85,16),(465,112,80,16),
               (605,112,155,16),(45,75,42,8),(190,61,42,8),(337,72,42,8),
               (485,55,42,8),(630,72,46,8)],
  "moving":[[108,91,45,"y",65,99,.55,-1],[258,84,45,"x",252,318,.80,1],
            [405,84,45,"y",57,96,.58,1],[548,78,46,"x",541,607,.85,-1]],
  "coins":[(65,58),(128,55),(207,44),(279,60),(356,55),(425,48),(505,38),(570,54),(652,55),(716,93)],
  "enemies":[(61,102,"mushroom",35,92,1),(191,51,"spiky",190,218,1),
             (338,62,"caterpillar",338,365,-1),(487,45,"snail",486,514,1),
             (642,102,"spiky",620,690,-1)]}
]

WORLD2 = [
 {"name":"GLOWING GROVE","width":650,
  "platforms":[(0,112,130,16),(175,112,110,16),(330,112,105,16),(480,112,170,16),
               (52,79,46,8),(211,70,44,8),(363,80,46,8),(520,66,48,8)],
  "moving":[[132,91,40,"x",128,178,.62,1],[286,86,42,"y",61,97,.46,-1],[436,88,42,"x",433,482,.70,-1]],
  "coins":[(72,62),(151,72),(231,53),(307,58),(386,63),(457,68),(543,49),(608,94)],
  "enemies":[(91,102,"beetle",60,119,1),(221,60,"ghost",214,245,-1),
             (356,102,"mushroom",342,420,1),(525,56,"bat",518,555,1)]},
 {"name":"FAIRY FUNGUS","width":720,
  "platforms":[(0,112,105,16),(155,112,95,16),(300,112,90,16),(445,112,90,16),(585,112,135,16),
               (61,72,42,8),(186,57,44,8),(329,72,44,8),(466,53,44,8),(615,70,46,8)],
  "moving":[[108,91,44,"y",65,98,.55,-1],[253,83,44,"x",248,304,.76,1],
            [393,87,48,"y",57,97,.52,1],[538,82,44,"x",533,589,.80,-1]],
  "coins":[(80,55),(130,54),(205,40),(272,58),(348,55),(416,49),(486,36),(558,56),(637,53),(686,94)],
  "enemies":[(65,102,"beetle",35,94,1),(188,47,"bat",187,217,1),(324,102,"ghost",312,375,-1),
             (469,43,"mushroom",467,497,1),(624,102,"beetle",606,690,-1)]},
 {"name":"MOONCAP CASTLE","width":780,
  "platforms":[(0,112,95,16),(150,112,85,16),(290,112,85,16),(430,112,80,16),(565,112,80,16),(700,112,80,16),
               (38,70,42,8),(178,56,42,8),(313,75,42,8),(450,51,42,8),(585,69,42,8),(718,52,42,8)],
  "moving":[[98,88,48,"x",94,153,.84,1],[238,84,48,"y",55,98,.61,-1],
            [378,82,48,"x",374,434,.88,-1],[513,82,48,"y",52,98,.62,1],[648,81,48,"x",644,704,.90,1]],
  "coins":[(57,53),(119,64),(198,39),(260,51),(334,58),(398,54),(470,34),(535,55),(605,52),(671,55),(738,35)],
  "enemies":[(54,102,"ghost",28,84,1),(180,46,"bat",179,208,-1),(309,102,"beetle",301,361,1),
             (452,41,"mushroom",450,479,-1),(583,102,"ghost",575,632,1),(719,42,"bat",718,748,-1)]}
]

WORLD3 = [
 {"name":"FROSTY FIELDS","width":670,
  "platforms":[(0,112,125,16),(170,112,105,16),(320,112,100,16),(465,112,90,16),(600,112,70,16),
               (55,76,44,8),(205,66,46,8),(350,78,44,8),(492,61,46,8),(610,76,42,8)],
  "moving":[[127,91,40,"x",124,173,.68,1],[277,86,40,"y",61,98,.50,-1],[423,88,40,"x",419,468,.75,-1],[557,84,40,"y",58,96,.48,1]],
  "coins":[(75,59),(146,70),(228,49),(297,58),(371,61),(444,67),(515,44),(578,58),(630,59)],
  "enemies":[(82,102,"penguin",48,113,1),(212,56,"snowball",207,239,-1),
             (345,102,"icebug",333,406,1),(500,51,"penguin",494,526,-1),(620,102,"snowball",607,655,1)]},
 {"name":"CRYSTAL CAVES","width":740,
  "platforms":[(0,112,100,16),(150,112,90,16),(290,112,85,16),(425,112,85,16),(560,112,80,16),(690,112,50,16),
               (38,70,42,8),(178,55,42,8),(315,71,42,8),(451,50,42,8),(582,67,42,8),(690,52,42,8)],
  "moving":[[103,88,44,"y",61,98,.58,-1],[243,82,44,"x",238,294,.82,1],[378,84,44,"y",54,98,.60,1],
            [513,80,44,"x",508,564,.86,-1],[643,83,44,"y",52,97,.62,-1]],
  "coins":[(58,53),(122,61),(198,38),(263,55),(336,54),(400,50),(472,33),(535,53),(603,50),(666,54),(711,35)],
  "enemies":[(52,102,"icebug",28,88,1),(180,45,"penguin",179,208,-1),(309,102,"snowball",300,362,1),
             (453,40,"icebug",451,480,-1),(580,102,"penguin",571,628,1),(696,42,"snowball",693,722,-1)]},
 {"name":"BLIZZARD PEAK","width":800,
  "platforms":[(0,112,90,16),(145,112,80,16),(280,112,80,16),(415,112,75,16),(545,112,75,16),(675,112,125,16),
               (32,68,40,8),(169,52,42,8),(302,72,42,8),(435,48,42,8),(565,66,42,8),(698,49,44,8)],
  "moving":[[93,87,48,"x",89,149,.90,1],[228,83,48,"y",52,98,.68,-1],[363,80,48,"x",359,419,.94,-1],
            [493,81,48,"y",49,98,.70,1],[623,79,48,"x",619,679,.98,1],[748,76,44,"y",45,96,.72,-1]],
  "coins":[(51,51),(112,61),(189,35),(249,49),(323,55),(383,51),(456,31),(516,53),(586,49),(646,51),(719,32),(770,55)],
  "enemies":[(48,102,"penguin",25,80,1),(170,42,"icebug",169,198,-1),(298,102,"snowball",289,349,1),
             (437,38,"penguin",435,465,-1),(560,102,"icebug",552,608,1),(700,39,"snowball",697,729,-1)]}
]

WORLD4 = [
 {"name":"LOLLIPOP LANE","width":690,
  "platforms":[(0,112,120,16),(165,112,105,16),(315,112,100,16),(460,112,95,16),(600,112,90,16),
               (50,77,44,8),(200,65,46,8),(345,78,44,8),(488,59,46,8),(620,75,44,8)],
  "moving":[[122,91,40,"x",119,168,.72,1],[272,86,40,"y",60,98,.52,-1],[418,87,40,"x",414,463,.80,-1],[558,83,40,"y",56,96,.54,1]],
  "coins":[(70,60),(142,70),(223,48),(293,58),(366,61),(438,66),(511,42),(580,57),(641,58)],
  "enemies":[(78,102,"gummy",45,108,1),(207,55,"cupcake",202,234,-1),
             (340,102,"lollipop",328,402,1),(496,49,"gummy",490,524,-1),(632,102,"cupcake",612,675,1)]},
 {"name":"CARAMEL CLOUDS","width":760,
  "platforms":[(0,112,100,16),(150,112,90,16),(290,112,85,16),(425,112,85,16),(560,112,80,16),(690,112,70,16),
               (38,69,42,8),(178,54,42,8),(315,70,42,8),(451,49,42,8),(582,66,42,8),(700,51,42,8)],
  "moving":[[103,87,44,"y",59,98,.61,-1],[243,81,44,"x",238,294,.86,1],[378,83,44,"y",52,98,.64,1],
            [513,79,44,"x",508,564,.90,-1],[643,82,44,"y",50,97,.66,-1]],
  "coins":[(58,52),(122,60),(198,37),(263,54),(336,53),(400,49),(472,32),(535,52),(603,49),(666,53),(721,34)],
  "enemies":[(50,102,"cupcake",27,88,1),(180,44,"gummy",179,208,-1),(309,102,"lollipop",300,362,1),
             (453,39,"cupcake",451,480,-1),(580,102,"gummy",571,628,1),(705,41,"lollipop",701,731,-1)]},
 {"name":"SUGAR PALACE","width":820,
  "platforms":[(0,112,90,16),(145,112,80,16),(280,112,80,16),(415,112,75,16),(545,112,75,16),(675,112,70,16),(790,112,30,16),
               (32,67,40,8),(169,51,42,8),(302,71,42,8),(435,47,42,8),(565,65,42,8),(698,48,44,8),(770,67,40,8)],
  "moving":[[93,86,48,"x",89,149,.94,1],[228,82,48,"y",50,98,.72,-1],[363,79,48,"x",359,419,.98,-1],
            [493,80,48,"y",47,98,.74,1],[623,78,48,"x",619,679,1.02,1],[748,75,40,"y",43,96,.76,-1]],
  "coins":[(51,50),(112,60),(189,34),(249,48),(323,54),(383,50),(456,30),(516,52),(586,48),(646,50),(719,31),(774,52)],
  "enemies":[(47,102,"gummy",24,80,1),(170,41,"lollipop",169,198,-1),(298,102,"cupcake",289,349,1),
             (437,37,"gummy",435,465,-1),(560,102,"lollipop",552,608,1),(700,38,"cupcake",697,729,-1)]}
]

WORLD5 = [
 {"name":"EMBER VALLEY","width":710,
  "platforms":[(0,112,115,16),(160,112,100,16),(305,112,95,16),(445,112,90,16),(580,112,130,16),
               (48,75,44,8),(193,63,46,8),(333,76,44,8),(472,57,46,8),(615,73,44,8)],
  "moving":[[117,90,40,"x",114,163,.78,1],[262,85,40,"y",58,98,.58,-1],[403,86,40,"x",399,448,.86,-1],[538,82,40,"y",54,96,.60,1]],
  "coins":[(68,58),(138,69),(216,46),(283,57),(354,59),(424,65),(495,40),(557,56),(636,56)],
  "enemies":[(76,102,"ember",43,104,1),(200,53,"fireball",195,228,-1),
             (329,102,"salamander",318,388,1),(480,47,"ember",474,506,-1),(625,102,"fireball",602,688,1)]},
 {"name":"LAVA TUNNELS","width":780,
  "platforms":[(0,112,95,16),(145,112,85,16),(280,112,80,16),(410,112,80,16),(540,112,75,16),(665,112,115,16),
               (35,68,42,8),(171,52,42,8),(305,68,42,8),(435,47,42,8),(564,64,42,8),(695,49,42,8)],
  "moving":[[98,86,44,"y",56,98,.68,-1],[233,80,44,"x",228,284,.94,1],[363,82,44,"y",49,98,.70,1],
            [493,78,44,"x",488,544,.98,-1],[618,80,44,"y",47,97,.72,-1]],
  "coins":[(55,51),(119,59),(191,35),(253,53),(326,51),(390,48),(456,30),(516,51),(585,47),(641,52),(716,32)],
  "enemies":[(48,102,"salamander",25,84,1),(174,42,"ember",172,201,-1),(298,102,"fireball",289,348,1),
             (437,37,"salamander",435,465,-1),(558,102,"ember",550,604,1),(701,39,"fireball",697,727,-1)]},
 {"name":"VOLCANO CORE","width":840,
  "platforms":[(0,112,85,16),(140,112,75,16),(270,112,75,16),(400,112,70,16),(525,112,70,16),(650,112,70,16),(775,112,65,16),
               (28,65,40,8),(159,49,42,8),(289,69,42,8),(419,45,42,8),(544,62,42,8),(669,46,42,8),(790,64,40,8)],
  "moving":[[88,85,48,"x",84,144,1.00,1],[218,81,48,"y",47,98,.78,-1],[348,78,48,"x",344,404,1.04,-1],
            [473,79,48,"y",44,98,.80,1],[598,76,48,"x",594,654,1.08,1],[723,74,48,"y",40,96,.82,-1]],
  "coins":[(47,48),(108,58),(179,32),(239,46),(310,52),(370,48),(440,28),(500,50),(565,45),(625,48),(690,29),(750,50),(810,47)],
  "enemies":[(44,102,"ember",22,76,1),(160,39,"fireball",159,188,-1),(288,102,"salamander",279,335,1),
             (421,35,"ember",419,449,-1),(540,102,"fireball",532,584,1),(670,36,"salamander",667,699,-1),(793,102,"ember",784,827,1)]}
]

WORLD6 = [
 {"name":"STARLIGHT PATH","width":730,
  "platforms":[(0,112,110,16),(155,112,95,16),(295,112,90,16),(430,112,85,16),(560,112,80,16),(685,112,45,16),
               (44,73,44,8),(184,60,46,8),(322,73,44,8),(456,55,46,8),(585,70,44,8),(690,52,38,8)],
  "moving":[[112,89,40,"x",109,158,.82,1],[252,84,40,"y",56,98,.62,-1],[388,85,40,"x",384,433,.90,-1],[518,81,40,"y",52,96,.64,1],[643,79,40,"x",639,688,.94,1]],
  "coins":[(64,56),(132,68),(207,43),(273,56),(343,56),(408,64),(479,38),(541,54),(606,53),(663,55),(706,35)],
  "enemies":[(72,102,"starling",40,99,1),(191,50,"owl",186,218,-1),(320,102,"shadow",309,373,1),
             (464,45,"starling",458,492,-1),(578,102,"owl",570,628,1),(697,42,"shadow",691,719,-1)]},
 {"name":"CLOUD DREAMS","width":800,
  "platforms":[(0,112,95,16),(140,112,80,16),(270,112,75,16),(395,112,75,16),(520,112,70,16),(640,112,70,16),(760,112,40,16),
               (31,66,40,8),(159,50,42,8),(289,68,42,8),(414,45,42,8),(539,62,42,8),(659,47,42,8),(770,64,30,8)],
  "moving":[[98,85,38,"y",52,98,.72,-1],[223,79,44,"x",218,274,.98,1],[348,81,44,"y",45,98,.74,1],
            [473,77,44,"x",468,524,1.02,-1],[593,78,44,"y",43,97,.76,-1],[713,75,44,"x",708,764,1.04,1]],
  "coins":[(50,49),(117,57),(179,33),(242,51),(310,51),(370,47),(435,28),(495,49),(560,45),(617,50),(680,30),(737,48),(781,47)],
  "enemies":[(45,102,"owl",23,84,1),(160,40,"shadow",159,188,-1),(286,102,"starling",278,333,1),
             (416,35,"owl",414,444,-1),(535,102,"shadow",527,578,1),(661,37,"starling",658,690,-1),(773,102,"owl",765,790,1)]},
 {"name":"MOONLIGHT CASTLE","width":860,
  "platforms":[(0,112,80,16),(135,112,70,16),(260,112,70,16),(385,112,65,16),(505,112,65,16),(625,112,65,16),(745,112,65,16),(850,112,10,16),
               (25,63,38,8),(150,47,40,8),(275,66,40,8),(400,42,40,8),(520,59,40,8),(640,43,40,8),(760,61,40,8),(820,42,38,8)],
  "moving":[[83,83,48,"x",79,139,1.06,1],[208,79,48,"y",43,98,.84,-1],[333,76,48,"x",329,389,1.10,-1],
            [453,77,48,"y",40,98,.86,1],[573,74,48,"x",569,629,1.14,1],[693,72,48,"y",37,96,.88,-1],[813,70,35,"x",809,849,1.16,-1]],
  "coins":[(44,46),(104,55),(170,30),(229,44),(295,49),(354,46),(420,25),(479,48),(540,42),(599,46),(660,26),(719,47),(780,44),(833,25)],
  "enemies":[(40,102,"shadow",20,70,1),(151,37,"starling",150,179,-1),(274,102,"owl",267,320,1),
             (402,32,"shadow",400,430,-1),(518,102,"starling",512,558,1),(642,33,"owl",639,670,-1),(760,102,"shadow",752,798,1)]}
]

def hit(ax,ay,aw,ah,bx,by,bw,bh):
    return ax<bx+bw and ax+aw>bx and ay<by+bh and ay+ah>by

def load_level(n):
    global level_index,level,world_w,platforms,movers,coins,enemies,powerups
    global player_x,player_y,vy,camera_x,on_ground,state
    global boss_x,boss_y,boss_vx,boss_hp,boss_flash,world_number,boss_name,bullets
    level_index=n
    if n<3 or 4<=n<=6 or 8<=n<=10 or 12<=n<=14 or 16<=n<=18 or 20<=n<=22:
        if n<3:
            level=LEVELS[n]; world_number=1
        elif n<=6:
            level=WORLD2[n-4]; world_number=2
        elif n<=10:
            level=WORLD3[n-8]; world_number=3
        elif n<=14:
            level=WORLD4[n-12]; world_number=4
        elif n<=18:
            level=WORLD5[n-16]; world_number=5
        else:
            level=WORLD6[n-20]; world_number=6
        world_w=level["width"]
        platforms=[list(p) for p in level["platforms"]]
        movers=[list(p) for p in level["moving"]]
        coins=[[c[0],c[1],False] for c in level["coins"]]
        enemies=[[e[0],e[1],e[2],e[3],e[4],e[5],True] for e in level["enemies"]]
        pickup_kind=("blaster","jump","life")[n%3]
        pickup_coin=coins[len(coins)//2]
        powerups=[[pickup_coin[0],pickup_coin[1]-14,pickup_kind,False]]
    else:
        if n==3:
            world_number=1; boss_name="KING SLIME"
        elif n==7:
            world_number=2; boss_name="QUEEN MORELLA"
        elif n==11:
            world_number=3; boss_name="FROSTFANG"
        elif n==15:
            world_number=4; boss_name="CANDY DRAGON"
        elif n==19:
            world_number=5; boss_name="VOLCANO TITAN"
        else:
            world_number=6; boss_name="NIGHTMARE MOON"
        level={"name":"BOSS: "+boss_name}; world_w=360
        platforms=[[0,112,360,16],[72,78,45,8],[246,78,45,8]]
        movers=[[157,82,46,"y",58,94,.45,1]]
        coins=[]; enemies=[]; powerups=[]
        boss_x,boss_y,boss_vx=285.0,88.0,-.75
        boss_hp,boss_flash=(5 if n==3 else (7 if n==7 else (8 if n==11 else (9 if n==15 else (10 if n==19 else 12))))),0
    player_x,player_y,vy,camera_x=18.0,88.0,0.0,0.0
    bullets=[]
    on_ground=False; state="intro"

def reset_game():
    global score,lives,state,has_blaster,super_jump,super_jump_timer
    global shop_choice,shop_note,player_facing
    score=0; lives=3
    has_blaster=False; super_jump=False; super_jump_timer=0
    shop_choice=0; shop_note="CHOOSE AN ITEM"
    player_facing=1
    load_level(0); state="title"

def respawn():
    global player_x,player_y,vy,camera_x,on_ground,bullets
    player_x,player_y,vy,camera_x=18.0,88.0,0.0,0.0; on_ground=False
    bullets=[]

def lose_life():
    global lives,state,has_blaster
    lives-=1
    has_blaster=False
    if lives<=0: state="game_over"
    else: respawn()

def update_movers():
    for p in movers:
        old_x,old_y=p[0],p[1]
        if p[3]=="x": p[0]+=p[6]*p[7]; value=p[0]
        else: p[1]+=p[6]*p[7]; value=p[1]
        if value<=p[4]:
            if p[3]=="x": p[0]=p[4]
            else: p[1]=p[4]
            p[7]=1
        elif value>=p[5]:
            if p[3]=="x": p[0]=p[5]
            else: p[1]=p[5]
            p[7]=-1
        p.append(p[0]-old_x)
        p.append(p[1]-old_y)

def clear_deltas():
    for p in movers:
        if len(p)>8: del p[8:]

def update_enemies():
    speeds={"snail":.32,"caterpillar":.48,"mushroom":.58,"spiky":.70,
            "beetle":.62,"ghost":.44,"bat":.78,
            "penguin":.58,"snowball":.86,"icebug":.68,
            "gummy":.64,"cupcake":.52,"lollipop":.82,
            "ember":.74,"fireball":.96,"salamander":.70,
            "starling":.82,"owl":.68,"shadow":.92}
    for e in enemies:
        if not e[6]: continue
        e[0]+=speeds[e[2]]*e[5]
        if e[0]<=e[3]: e[0],e[5]=e[3],1
        elif e[0]>=e[4]: e[0],e[5]=e[4],-1

def update_boss(previous_bottom):
    global boss_x,boss_vx,boss_hp,boss_flash,vy,player_y,state
    boss_x+=boss_vx
    if boss_x<205 or boss_x>330: boss_vx=-boss_vx
    if boss_flash>0: boss_flash-=1
    if hit(player_x,player_y,PW,PH,boss_x,boss_y,22,24):
        if vy>0 and previous_bottom<=boss_y+5 and boss_flash==0:
            boss_hp-=1; boss_flash=45; player_y=boss_y-PH; vy=-5.0
            if boss_hp<=0: state="world_complete"
        elif boss_flash==0: lose_life()

def fire_bullet():
    if len(bullets)<4:
        start_x=player_x+PW if player_facing>0 else player_x-4
        bullets.append([start_x,player_y+6,player_facing,True])

def update_bullets():
    global boss_hp,boss_flash,state
    boss_level=level_index in (3,7,11,15,19,23)
    for b in bullets:
        if not b[3]: continue
        b[0]+=3.4*b[2]
        if b[0]<0 or b[0]>world_w: b[3]=False; continue
        for e in enemies:
            if e[6] and hit(b[0],b[1],4,2,e[0],e[1],12,10):
                e[6]=False; b[3]=False; break
        if b[3] and boss_level and boss_flash==0 and hit(b[0],b[1],4,2,boss_x,boss_y,22,24):
            boss_hp-=1; boss_flash=20; b[3]=False
            if boss_hp<=0: state="world_complete"

def update_powerup_timers():
    global super_jump,super_jump_timer
    if super_jump_timer>0:
        super_jump_timer-=1
        if super_jump_timer<=0:
            super_jump_timer=0; super_jump=False

def update_player():
    global player_x,player_y,vy,on_ground,camera_x,score,state,player_facing
    global has_blaster,super_jump,super_jump_timer,lives
    old_y=player_y
    if engine_io.LEFT.is_pressed: player_x-=SPEED; player_facing=-1
    if engine_io.RIGHT.is_pressed: player_x+=SPEED; player_facing=1
    player_x=max(0,min(player_x,world_w-PW))
    wants_jump=engine_io.A.is_just_pressed or (engine_io.B.is_just_pressed and not has_blaster)
    if wants_jump and on_ground:
        vy=-7.5 if super_jump else JUMP; on_ground=False
    if engine_io.B.is_just_pressed and has_blaster:
        fire_bullet()
    vy=min(vy+GRAVITY,MAX_FALL); player_y+=vy
    on_ground=False; old_bottom=old_y+PH; new_bottom=player_y+PH
    if vy>=0:
        for p in platforms+movers:
            if player_x+PW>p[0] and player_x<p[0]+p[2] and old_bottom<=p[1] and new_bottom>=p[1]:
                player_y=p[1]-PH; vy=0.0; on_ground=True
                if len(p)>8: player_x+=p[8]
                break
    if player_y>150: lose_life(); return
    for c in coins:
        if not c[2] and hit(player_x,player_y,PW,PH,c[0]-4,c[1]-4,8,8):
            c[2]=True; score+=1
    for p in powerups:
        if not p[3] and hit(player_x,player_y,PW,PH,p[0]-5,p[1]-5,10,10):
            p[3]=True
            if p[2]=="blaster":
                if has_blaster: score+=3
                else: has_blaster=True
            elif p[2]=="jump":
                super_jump=True; super_jump_timer=720
            else:
                if lives<5: lives+=1
                else: score+=3
    for e in enemies:
        if e[6] and hit(player_x,player_y,PW,PH,e[0],e[1],12,10):
            if vy>0 and old_bottom<=e[1]+4: e[6]=False; vy=-4.4
            else: lose_life(); return
    if level_index in (3,7,11,15,19,23): update_boss(old_bottom)
    elif player_x>world_w-42: state="level_complete"
    target=max(0,min(player_x-42,world_w-W))
    camera_x+=(target-camera_x)*.16

def sx(x): return int(x-camera_x)

def draw_cloud(x,y):
    x=sx(x)
    if -25<x<145:
        fb.fill_rect(x,y+4,22,7,WHITE); fb.fill_rect(x+5,y,9,12,WHITE)
        fb.fill_rect(x+13,y+2,7,10,WHITE)

def draw_world():
    if world_number==1:
        fb.fill(SKY); fb.fill_rect(int(103-camera_x*.05),12,13,13,SUN)
        for x,y in ((36,20),(180,34),(345,18),(520,30),(690,20)):
            draw_cloud(x+camera_x*.55,y)
        for hx in range(10,world_w,150):
            x=sx(hx); fb.fill_rect(x,91,70,21,0x4DA9); fb.fill_rect(x+12,83,46,29,0x4DA9)
    elif world_number==2:
        fb.fill(0x2108)
        fb.fill_rect(int(105-camera_x*.03),12,12,12,0xC61F)
        for tx in range(15,world_w,90):
            x=sx(tx); fb.fill_rect(x,42,9,70,0x30C3); fb.fill_rect(x-8,35,25,14,0x580F)
        for mx in range(42,world_w,105):
            x=sx(mx)
            if -12<x<138:
                fb.fill_rect(x,93,5,19,WHITE); fb.fill_rect(x-5,88,15,7,PURPLE)
                fb.pixel(x-1,90,PINK); fb.pixel(x+5,89,YELLOW)
    elif world_number==3:
        fb.fill(0x6D7F)
        fb.fill_rect(int(104-camera_x*.03),11,13,13,WHITE)
        for mx in range(0,world_w,120):
            x=sx(mx); fb.fill_rect(x,82,80,30,0xB65F); fb.fill_rect(x+18,68,45,44,0xCEBF)
        for flake_x in range(24,world_w,47):
            x=sx(flake_x)
            if 0<x<128:
                y=25+(flake_x%53); fb.pixel(x,y,WHITE); fb.pixel(x-1,y,WHITE); fb.pixel(x+1,y,WHITE)
    elif world_number==4:
        fb.fill(0xF59F)
        for cx in range(10,world_w,115):
            x=sx(cx); fb.fill_rect(x,83,78,29,0xFE19); fb.fill_rect(x+14,72,50,40,0xF81F)
        for lx in range(45,world_w,100):
            x=sx(lx)
            if -10<x<138:
                fb.fill_rect(x,75,3,37,WHITE); fb.fill_rect(x-5,68,13,13,YELLOW)
                fb.fill_rect(x-3,70,9,9,RED); fb.fill_rect(x-1,72,5,5,WHITE)
    elif world_number==5:
        fb.fill(0x3102)
        for vx in range(0,world_w,135):
            x=sx(vx); fb.fill_rect(x,80,90,32,0x6000); fb.fill_rect(x+18,64,54,48,0x8000)
            fb.fill_rect(x+35,72,18,40,RED); fb.fill_rect(x+40,82,9,30,YELLOW)
        for spark_x in range(20,world_w,43):
            x=sx(spark_x)
            if 0<x<128:
                y=24+(spark_x%48); fb.pixel(x,y,RED); fb.pixel(x,y+1,YELLOW)
    else:
        fb.fill(0x1084)
        fb.fill_rect(int(103-camera_x*.02),10,15,15,0xC61F)
        fb.fill_rect(int(99-camera_x*.02),7,8,8,0x1084)
        for star_x in range(18,world_w,39):
            x=sx(star_x)
            if 0<x<128:
                y=18+(star_x%57); fb.pixel(x,y,WHITE)
                if star_x%2: fb.pixel(x+1,y,YELLOW)
        for cloud_x in range(5,world_w,125):
            x=sx(cloud_x); fb.fill_rect(x,88,82,24,0x4210); fb.fill_rect(x+15,78,50,34,0x4210)
    for p in platforms:
        x=sx(p[0])
        if x<W and x+p[2]>0:
            ground_color=0x9D5F if world_number==3 else (0xFB2D if world_number==4 else (0x6000 if world_number==5 else (0x4210 if world_number==6 else DIRT)))
            top_color=WHITE if world_number in (3,4) else GRASS
            if world_number==5: top_color=RED
            if world_number==6: top_color=0xC61F
            fb.fill_rect(x,int(p[1]),p[2],p[3],ground_color); fb.fill_rect(x,int(p[1]),p[2],3,top_color)
    for p in movers:
        x=sx(p[0])
        if x<W and x+p[2]>0:
            move_color=0x4DDF if world_number==3 else (DARK_PINK if world_number==4 else (RED if world_number==5 else (0x801F if world_number==6 else PURPLE)))
            move_top=WHITE if world_number in (3,4) else YELLOW
            fb.fill_rect(x,int(p[1]),p[2],8,move_color); fb.fill_rect(x,int(p[1]),p[2],3,move_top)
    for c in coins:
        if not c[2]:
            x,y=sx(c[0]),c[1]
            if -6<x<134:
                fb.fill_rect(x-3,y-3,7,7,PINK); fb.fill_rect(x-1,y-5,3,11,PINK)
                fb.fill_rect(x-5,y-1,11,3,PINK); fb.fill_rect(x-1,y-1,3,3,YELLOW)
    for p in powerups:
        if not p[3]:
            x,y=sx(p[0]),int(p[1])
            if -8<x<136:
                box_color=RED if p[2]=="blaster" else (BLUE if p[2]=="jump" else PINK)
                fb.fill_rect(x-5,y-5,11,11,WHITE); fb.fill_rect(x-4,y-4,9,9,box_color)
                if p[2]=="blaster":
                    fb.fill_rect(x-2,y-1,6,2,BLACK); fb.fill_rect(x-2,y+1,2,3,BLACK)
                elif p[2]=="jump":
                    fb.fill_rect(x-1,y-3,3,6,YELLOW); fb.pixel(x-2,y-2,YELLOW); fb.pixel(x+2,y-2,YELLOW)
                else:
                    fb.fill_rect(x-1,y-3,3,7,WHITE); fb.fill_rect(x-3,y-1,7,3,WHITE)
    if level_index not in (3,7,11,15,19,23):
        x=sx(world_w-36)
        fb.fill_rect(x,62,2,50,WHITE); fb.fill_rect(x+2,64,18,6,RED)
        fb.fill_rect(x+2,70,18,6,YELLOW); fb.fill_rect(x+2,76,18,6,BLUE)

def draw_bunny():
    x,y=sx(player_x),int(player_y)
    fb.fill_rect(x+1,y-5,3,7,WHITE); fb.fill_rect(x+6,y-5,3,7,WHITE)
    fb.fill_rect(x+2,y-4,1,4,PINK); fb.fill_rect(x+7,y-4,1,4,PINK)
    fb.fill_rect(x,y,PW,PH,WHITE); fb.fill_rect(x+3,y+7,5,6,PINK); fb.pixel(x+7,y+3,BLACK)
    if has_blaster:
        gun_x=x+8 if player_facing>0 else x-3
        fb.fill_rect(gun_x,y+7,5,2,BLACK)

def draw_bullets():
    for b in bullets:
        if b[3]:
            x=sx(b[0])
            if -5<x<132: fb.fill_rect(x,int(b[1]),4,2,YELLOW)

def draw_enemies():
    for e in enemies:
        if not e[6]: continue
        x,y,k=sx(e[0]),int(e[1]),e[2]
        if not -14<x<130: continue
        if k=="snail":
            fb.fill_rect(x+1,y+3,8,7,PINK); fb.fill_rect(x+3,y+1,5,5,DARK_PINK); fb.fill_rect(x+8,y+6,5,4,YELLOW)
        elif k=="caterpillar":
            fb.fill_rect(x,y+4,5,6,GRASS); fb.fill_rect(x+4,y+3,5,7,0x07EF); fb.fill_rect(x+8,y+2,5,8,GRASS)
        elif k=="mushroom":
            fb.fill_rect(x+3,y+5,6,5,WHITE); fb.fill_rect(x,y+1,12,6,PURPLE); fb.pixel(x+3,y+3,WHITE)
        elif k=="spiky":
            fb.fill_rect(x+1,y+3,11,7,BLUE)
            for dx in (2,5,8,11): fb.pixel(x+dx,y+1,YELLOW)
        if k=="beetle":
            fb.fill_rect(x+1,y+3,11,7,DARK_PINK); fb.vline(x+6,y+3,7,BLACK)
            fb.pixel(x+3,y+5,YELLOW); fb.pixel(x+9,y+5,YELLOW)
        elif k=="ghost":
            fb.fill_rect(x+2,y+1,9,9,WHITE); fb.fill_rect(x,y+5,13,5,WHITE)
            fb.pixel(x+4,y+4,PURPLE); fb.pixel(x+8,y+4,PURPLE)
        elif k=="bat":
            fb.fill_rect(x+4,y+3,5,7,PURPLE); fb.fill_rect(x,y+2,4,5,DARK_PINK)
            fb.fill_rect(x+9,y+2,4,5,DARK_PINK); fb.pixel(x+5,y+5,YELLOW); fb.pixel(x+7,y+5,YELLOW)
        elif k=="penguin":
            fb.fill_rect(x+2,y,9,10,BLACK); fb.fill_rect(x+4,y+3,5,6,WHITE)
            fb.pixel(x+4,y+2,WHITE); fb.pixel(x+8,y+2,WHITE); fb.fill_rect(x+10,y+4,3,2,YELLOW)
        elif k=="snowball":
            fb.fill_rect(x+1,y+1,11,9,WHITE); fb.fill_rect(x+3,y,7,10,WHITE)
            fb.pixel(x+4,y+4,BLUE); fb.pixel(x+8,y+4,BLUE)
        elif k=="icebug":
            fb.fill_rect(x+1,y+3,11,7,0x4DDF); fb.fill_rect(x+4,y+1,5,3,WHITE)
            fb.pixel(x+3,y+5,BLACK); fb.pixel(x+9,y+5,BLACK)
        elif k=="gummy":
            fb.fill_rect(x+1,y+2,11,8,PINK); fb.fill_rect(x+3,y,7,4,DARK_PINK)
            fb.pixel(x+4,y+5,WHITE); fb.pixel(x+8,y+5,WHITE)
        elif k=="cupcake":
            fb.fill_rect(x+2,y+5,9,5,YELLOW); fb.fill_rect(x,y+2,13,5,PINK)
            fb.pixel(x+3,y+3,WHITE); fb.pixel(x+9,y+3,WHITE)
        elif k=="lollipop":
            fb.fill_rect(x+5,y+5,2,5,WHITE); fb.fill_rect(x+1,y,10,7,RED)
            fb.fill_rect(x+3,y+2,6,3,YELLOW); fb.pixel(x+5,y+3,WHITE)
        elif k=="ember":
            fb.fill_rect(x+2,y+3,9,7,RED); fb.fill_rect(x+4,y,5,5,YELLOW)
            fb.pixel(x+4,y+6,WHITE); fb.pixel(x+8,y+6,WHITE)
        elif k=="fireball":
            fb.fill_rect(x+1,y+2,11,8,RED); fb.fill_rect(x+3,y,7,10,YELLOW)
            fb.pixel(x+4,y+4,BLACK); fb.pixel(x+8,y+4,BLACK)
        elif k=="salamander":
            fb.fill_rect(x,y+4,13,6,0xFA20); fb.fill_rect(x+8,y+1,5,5,RED)
            fb.pixel(x+10,y+3,YELLOW); fb.fill_rect(x-2,y+7,3,2,0xFA20)
        elif k=="starling":
            fb.fill_rect(x+3,y+1,7,8,YELLOW); fb.pixel(x+1,y+4,YELLOW); fb.pixel(x+11,y+4,YELLOW)
            fb.pixel(x+5,y+4,WHITE); fb.pixel(x+8,y+4,WHITE)
        elif k=="owl":
            fb.fill_rect(x+2,y+1,9,9,0xA145); fb.fill_rect(x,y+3,4,6,PURPLE)
            fb.fill_rect(x+9,y+3,4,6,PURPLE); fb.pixel(x+4,y+4,YELLOW); fb.pixel(x+8,y+4,YELLOW)
        elif k=="shadow":
            fb.fill_rect(x+1,y+2,11,8,BLACK); fb.fill_rect(x+3,y,7,10,PURPLE)
            fb.pixel(x+4,y+4,RED); fb.pixel(x+8,y+4,RED)

def draw_boss():
    if level_index not in (3,7,11,15,19,23): return
    x,y=sx(boss_x),int(boss_y)
    color=WHITE if boss_flash and boss_flash%6<3 else PURPLE
    if level_index==3:
        fb.fill_rect(x+2,y+5,20,19,color); fb.fill_rect(x+5,y+1,14,9,color)
        fb.pixel(x+7,y+9,WHITE); fb.pixel(x+16,y+9,WHITE)
        fb.fill_rect(x+5,y-3,3,5,YELLOW); fb.fill_rect(x+11,y-5,3,7,YELLOW); fb.fill_rect(x+17,y-3,3,5,YELLOW)
    elif level_index==7:
        fb.fill_rect(x+8,y+8,8,16,WHITE); fb.fill_rect(x+1,y+2,22,10,color)
        fb.fill_rect(x+4,y,16,5,DARK_PINK); fb.pixel(x+6,y+5,WHITE); fb.pixel(x+17,y+5,YELLOW)
        fb.pixel(x+10,y+13,BLACK); fb.pixel(x+14,y+13,BLACK)
    elif level_index==11:
        fb.fill_rect(x+3,y+4,18,20,WHITE); fb.fill_rect(x+1,y+8,22,11,color)
        fb.fill_rect(x+4,y,4,8,0x4DDF); fb.fill_rect(x+16,y,4,8,0x4DDF)
        fb.pixel(x+7,y+10,BLUE); fb.pixel(x+16,y+10,BLUE); fb.fill_rect(x+9,y+15,7,3,BLACK)
    elif level_index==15:
        fb.fill_rect(x+3,y+5,19,18,color); fb.fill_rect(x+1,y+8,5,8,DARK_PINK)
        fb.fill_rect(x+20,y+8,5,8,DARK_PINK); fb.fill_rect(x+6,y+1,4,7,YELLOW)
        fb.fill_rect(x+16,y,4,8,YELLOW); fb.pixel(x+8,y+10,WHITE); fb.pixel(x+17,y+10,WHITE)
        fb.fill_rect(x+20,y+14,6,3,RED)
    elif level_index==19:
        fb.fill_rect(x+2,y+4,21,20,color); fb.fill_rect(x,y+9,5,11,RED)
        fb.fill_rect(x+20,y+9,5,11,RED); fb.fill_rect(x+5,y,5,8,YELLOW)
        fb.fill_rect(x+15,y,5,8,YELLOW); fb.pixel(x+7,y+10,YELLOW); fb.pixel(x+17,y+10,YELLOW)
        fb.fill_rect(x+8,y+16,9,4,BLACK); fb.pixel(x+10,y+17,RED); fb.pixel(x+14,y+17,RED)
    else:
        fb.fill_rect(x+2,y+4,21,20,color); fb.fill_rect(x,y+8,5,13,BLACK)
        fb.fill_rect(x+20,y+8,5,13,BLACK); fb.fill_rect(x+7,y,11,8,0xC61F)
        fb.pixel(x+7,y+10,YELLOW); fb.pixel(x+17,y+10,YELLOW)
        fb.fill_rect(x+8,y+16,9,3,BLACK); fb.pixel(x+4,y+2,WHITE); fb.pixel(x+21,y+1,WHITE)
    fb.text("BOSS",4,18,RED); fb.fill_rect(35,19,60,5,BLACK)
    unit=4 if level_index==23 else (5 if level_index==19 else (6 if level_index==15 else (7 if level_index==11 else (8 if level_index==7 else 11))))
    fb.fill_rect(36,20,boss_hp*unit,3,RED)

def draw_hud():
    fb.fill_rect(2,2,124,12,WHITE); fb.text("FLOWERS:"+str(score),5,4,PURPLE)
    for h in range(lives):
        x=86+h*8; fb.fill_rect(x,5,6,5,PINK); fb.pixel(x+1,4,PINK); fb.pixel(x+4,4,PINK)

def center(text,y,color):
    fb.text(text,max(2,(128-len(text)*6)//2),y,color)

def message(title,line,action):
    fb.fill(PINK); center(title,27,WHITE); center(line,53,YELLOW); center(action,92,PURPLE)

def buy_shop_item():
    global score,lives,has_blaster,super_jump,super_jump_timer,shop_note
    if shop_choice==0:
        if has_blaster: shop_note="ALREADY OWNED"
        elif score<8: shop_note="NOT ENOUGH FLOWERS"
        else: score-=8; has_blaster=True; shop_note="BLASTER BOUGHT!"
    elif shop_choice==1:
        if super_jump: shop_note="ALREADY OWNED"
        elif score<10: shop_note="NOT ENOUGH FLOWERS"
        else:
            score-=10; super_jump=True; super_jump_timer=720
            shop_note="SUPER JUMP BOUGHT!"
    else:
        if lives>=5: shop_note="LIVES ARE FULL"
        elif score<15: shop_note="NOT ENOUGH FLOWERS"
        else: score-=15; lives+=1; shop_note="EXTRA LIFE BOUGHT!"

def update_shop():
    global shop_choice,shop_note,state
    if engine_io.UP.is_just_pressed:
        shop_choice=(shop_choice-1)%3; shop_note="CHOOSE AN ITEM"
    if engine_io.DOWN.is_just_pressed:
        shop_choice=(shop_choice+1)%3; shop_note="CHOOSE AN ITEM"
    if engine_io.A.is_just_pressed: buy_shop_item()
    if engine_io.B.is_just_pressed or engine_io.MENU.is_just_pressed: state="playing"

def draw_shop():
    fb.fill(0x2108)
    center("FLOWER SHOP",7,YELLOW)
    fb.text("FLOWERS:"+str(score),5,20,WHITE)
    blaster_text="BLASTER  OWNED" if has_blaster else "BLASTER      8"
    jump_text=("JUMP "+str((super_jump_timer+59)//60)+"S LEFT") if super_jump else "SUPER JUMP  10"
    life_text="EXTRA LIFE "+str(lives)+"/5"
    items=(blaster_text,jump_text,life_text)
    for i in range(3):
        y=38+i*19
        if i==shop_choice:
            fb.fill_rect(3,y-3,122,15,PURPLE)
            fb.text(">"+items[i],7,y,WHITE)
        else:
            fb.text(" "+items[i],7,y,0xC61F)
    center(shop_note,98,PINK)
    center("A:BUY  B:CLOSE",114,WHITE)

def draw_title():
    fb.fill(SKY); fb.fill_rect(0,95,128,33,GRASS)
    center("BUNNYBITCH",23,PURPLE); center("WORLD 1",43,WHITE); center("A: START",74,YELLOW)

reset_game()
while True:
    if engine.tick():
        if state=="title":
            draw_title()
            if engine_io.A.is_just_pressed or engine_io.B.is_just_pressed: load_level(0)
        elif state=="intro":
            message("WORLD "+str(world_number),level["name"],"A: GO!")
            if engine_io.A.is_just_pressed or engine_io.B.is_just_pressed: state="playing"
        elif state=="playing":
            if engine_io.MENU.is_just_pressed:
                state="shop"
            else:
                update_movers(); update_enemies(); update_powerup_timers(); update_player(); update_bullets()
                draw_world(); draw_enemies(); draw_boss(); draw_bullets(); draw_bunny(); draw_hud(); clear_deltas()
        elif state=="shop":
            update_shop(); draw_shop()
        elif state=="level_complete":
            message("LEVEL COMPLETE!","GREAT HOPPING!","A: NEXT LEVEL")
            if engine_io.A.is_just_pressed or engine_io.B.is_just_pressed: load_level(level_index+1)
        elif state=="world_complete":
            if level_index==3:
                message("WORLD 1 COMPLETE!","KING SLIME BEATEN","A: WORLD 2")
                if engine_io.A.is_just_pressed or engine_io.B.is_just_pressed: load_level(4)
            elif level_index==7:
                message("WORLD 2 COMPLETE!","MORELLA BEATEN","A: WORLD 3")
                if engine_io.A.is_just_pressed or engine_io.B.is_just_pressed: load_level(8)
            elif level_index==11:
                message("WORLD 3 COMPLETE!","FROSTFANG BEATEN","A: WORLD 4")
                if engine_io.A.is_just_pressed or engine_io.B.is_just_pressed: load_level(12)
            elif level_index==15:
                message("WORLD 4 COMPLETE!","CANDY DRAGON DOWN","A: WORLD 5")
                if engine_io.A.is_just_pressed or engine_io.B.is_just_pressed: load_level(16)
            elif level_index==19:
                message("WORLD 5 COMPLETE!","TITAN DEFEATED","A: WORLD 6")
                if engine_io.A.is_just_pressed or engine_io.B.is_just_pressed: load_level(20)
            else:
                fb.fill(PURPLE)
                center("YOU SAVED",28,WHITE); center("BUNNYBITCH!",42,YELLOW)
                center("ALL 6 WORLDS",63,WHITE); center("COMPLETE!",75,PINK)
                center("A: PLAY AGAIN",103,YELLOW)
                if engine_io.A.is_just_pressed or engine_io.B.is_just_pressed: reset_game(); load_level(0)
        elif state=="game_over":
            message("GAME OVER","KEEP HOPPING!","A: TRY AGAIN")
            if engine_io.A.is_just_pressed or engine_io.B.is_just_pressed: reset_game(); load_level(0)
