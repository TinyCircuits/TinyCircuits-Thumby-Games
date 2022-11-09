import gc
gc.threshold(2000)
gc.enable()
from monsters import Monsters, Bones
gc.collect()
from player import Player, bU, bD, bL, bR, bB, bA
gc.collect()
from tape import Tape, display_update, EMULATED
gc.collect()
from os import mkdir
from time import ticks_ms
from audio import audio_tick
from comms import comms, inbuf, outbuf
from script import get_chapters, story_events, story_jump, state
import script
gc.collect()

_FPS = const(60)

tape = Tape()
mons = Monsters(tape)
tape.mons_clear = mons.clear
tape.mons_add = mons.add

def _run_menu():
    handshake = held = t = 0
    # Umby/Glow, 1P/2P, Text/Talk, Easy/Hard, New/Load, Chapter, selection
    ch = [0, 0, 0, 0, 1, -1, 0]
    story_jump(tape, mons, -999, False)
    mons.add(Bones, -970, 32)
    chapters = list(get_chapters())

    def background_update():
        # Make the camera follow the monster
        mons.tick(t)
        mons.draw_and_check_death(t, None, None)
        tape.auto_camera(mons.x[0], mons.y[0]-64, 1, t)
        tape.comp()
        display_update()
        if not EMULATED:
            # Greyscale half-frame
            tape.comp()
            display_update()
        tape.clear_stage()

    def sel(i): # Menu arrows
        return (("_" if ch[i] else "<")
            + (((("_-" if ch[i] else "-_")) if i == ch[6] else "__"))
            + (">" if ch[i] else "_"))

    def update_main_menu():
        ch[6] = (ch[6] + (1 if not bD() else -1 if not bU() else 0)) % 5
        if not (bL() and bR()):
            ch[ch[6]] = 0 if not bL() else 1
        msg = "UMBY_"+sel(0)+"_GLOW "
        msg += "__1P_"+sel(1)+"_2P__ "
        msg += "TEXT_"+sel(2)+"_TALK "
        msg += "EASY_"+sel(3)+"_HARD "
        msg += "_NEW_"+sel(4)+"_LOAD"
        tape.clear_overlay()
        tape.message(0, msg, 3)

    def update_chapter_menu():
        if bU() and bD():
            return
        ch[5] = (ch[5] + (-1 if not bU() else 1)) % len(chapters)
        msg = chapters[ch[5]][0]
        tape.clear_overlay()
        tape.message(0, msg, 3)

    menu = update_main_menu
    menu()
    while menu:
        if held == 0 and not (bU() and bD() and bL() and bR()):
            menu()
            held = 1
        elif bU() and bD() and bL() and bR() and bB() and bA():
            held = 0
        if not bA() and held != 2:
            if not (bD() or bA() or bB()):
                # Secret chapter menu (DOWN+B+A)
                menu = update_chapter_menu
                menu()
                held = 2
            else:
                try:
                    mkdir("/Saves")
                except:
                    pass
                sav = "/Saves/Umby&Glow-"+("glow" if ch[0] else "umby")+".sav"
                # Find the starting position (of this player)
                if ch[5] == -1:
                    start = 3
                    if ch[4]:
                        try:
                            with open(sav, "r") as f:
                                start = int(f.read()) - 145
                        except:
                            pass
                    start = start if start > 3 else 3
                else: # Chapter selection
                    start = chapters[ch[5]][1]
                menu = None
        background_update()
        t += 1
    clip = not (bU() or bA() or bB())

    ## Negotiate 2 player communication and starting position (if needed)
    if ch[1]:
        tape.clear_overlay()
        # Waiting for other player...
        tape.message(0, "WAITING...", 3)
        while handshake < 240:
            # Get ready to send starting location information
            outbuf[0] = start>>24
            outbuf[1] = start>>16
            outbuf[2] = start>>8
            outbuf[3] = start
            # Communicate with other player on start position
            if comms():
                handshake += 60
                p2start = inbuf[0]<<24 | inbuf[1]<<16 | inbuf[2]<<8 | inbuf[3]
                if p2start > start:
                    start = p2start
            # Update background
            background_update()
            t += 1

    tape.clear_overlay()
    tape.message(0, "GET READY!!...", 3)
    background_update()
    tape.clear_overlay()
    return ch[0], clip, ch[1], ch[2], ch[3], start, sav
glow, clip, coop, autotxt, hard, start, sav = _run_menu()
del _run_menu

@micropython.native
def run_game():
    prof = not bL() # Activate profiling by holding Left direction
    # Select character, or testing mode by holding Up+B+A (release Up last)
    p1 = Player(tape, mons,
        "Clip" if clip else "Glow" if glow else "Umby", start+10, 20, hard=hard)
    tape.player = p1
    tape.players.append(p1)
    story_jump(tape, mons, start, True)
    gc.collect()
    gc.threshold(16000)

    mons2 = Monsters(tape)
    mons.omons = mons2
    ch = tape.check
    p1.port_out(outbuf) # Initialise coop send-buffer
    p2 = Player(tape, mons,
        "Umby" if glow else "Glow", start+10, 20, ai=not coop, coop=coop)
    tape.players.append(p2)

    # Main gameplay loop
    t = savst = coop_px = pstat = pstat2 = ptot = pfps1 = pfps2 = 0
    pw = pw2 = pfpst = ticks_ms()
    while(1):
        story_events(tape, mons, coop_px, autotxt, outbuf, inbuf)
        play = outbuf[14] and (not coop or inbuf[14])
        # Update the game engine by a tick
        if play:
            p1.tick(t)
            p2.tick(t)
            mons.tick(t)
        # Make the camera follow the action
        tape.auto_camera(p1.x, p1.y, p1.dir, t)

        # Update coop networking
        if coop:
            if comms():
                # Update player 2 data (and also monsters)
                coop_px = p2.port_in(inbuf)
                mons2.port_in(inbuf)
                # Send player 1 data (and also monsters)
                p1.port_out(outbuf)
                mons.port_out(outbuf)

        # Half frame greyscale render
        if not EMULATED:
            if not prof:
                tape.comp()
                display_update()
            else:
                tape.comp()
                pw2 = ticks_ms()
                display_update()
                pstat2 += ticks_ms() - pw2
                pfps2 += 1

        # Drawing and collisions
        tape.clear_stage()
        # Draw all the monsters, and check for collisions along the way
        mons.draw_and_check_death(t, p1, p2)
        mons2.draw_and_check_death(t, None, None)

        # Check for death by monster
        if play and ch(p1.x-tape.x[0], p1.y, 224):
            p1.die("Umby became monster food!")
        # Draw the players
        p1.draw(t)
        p2.draw(t)

        # Composite everything together to the render buffer
        tape.comp()
        audio_tick()
        if play:
            t += 1

        # Save any script progress (script events function as save points)
        if (savst != state[0]):
            f = open(sav, "w")
            f.write(str(state[0]))
            f.close()
            savst = state[0]

        # Flush to the display, waiting on the next frame interval
        if not prof:
            display_update()
            continue
        # Or flush display with speed and memory profiling
        pstat += ticks_ms() - pw
        pfps1 += 1
        display_update()
        if t % _FPS == 0:
            fpst = ticks_ms() - pfpst
            ptot += pstat
            gc.collect() # Full garbage collect for good memory use reading.
            print(pstat, ptot*_FPS//t, gc.mem_alloc(), gc.mem_free(), pstat2,
                pfps1*1000//fpst, pfps2*1000//fpst, tape.x[0])
            pstat = pstat2 = pfps1 = pfps2 = 0
            pfpst = ticks_ms()
        pw = ticks_ms()

run_game()
