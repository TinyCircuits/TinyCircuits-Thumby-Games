from platform_loader import PC, display, buttonA, buttonB, buttonU, buttonD, buttonL, buttonR, IS_THUMBY_COLOR
from time import sleep
from utime import ticks_ms, ticks_diff
import os
from gc import collect
import stream_json as sj


class CampaignEngine:
    def __init__(self, game_loc="/Games/ThumbCommander/"):
        self.game_loc = game_loc
        self.campaign_file = None
        self.current_campaign = None
        self.current_mission = 0
        self.total_score = 0
        self.campaign_saves = {}
        self.campaign_order = []
        self._mission_cache = None
        self._mission_cache_idx = -1
        self._load_campaigns()
        self.background = None
        display.setFont("/lib/font3x5.bin", 3, 5, 1)

    def _load_campaigns(self):
        """Load campaign headers only (title + description) - no full JSON parse"""
        try:
            files = [f for f in os.listdir(self.game_loc) if f.endswith("_campaign.json")]
            files.sort()
            self.campaigns = {}
            self.campaign_order = []
            for file in files:
                data = sj.read_fields(self.game_loc + file, ['title', 'description'])
                if data['title']:
                    self.campaigns[data['title']] = {"file": file, "description": data['description'] or ""}
                    self.campaign_order.append(data['title'])
            try:
                with open(self.game_loc + "campaign_saves.json", 'r') as f:
                    import json
                    self.campaign_saves = json.loads(f.read())
            except: self.campaign_saves = {}
            collect()
        except:
            self.campaigns = {}
            self.campaign_order = []

    def _get_mission(self, idx):
        """Get mission data by index using streaming"""
        if self._mission_cache_idx == idx and self._mission_cache:
            return self._mission_cache
        if not self.campaign_file: return None
        result = sj.get_array_object(self.game_loc + self.campaign_file, 'missions', idx)
        if result:
            self._mission_cache = result
            self._mission_cache_idx = idx
        return result

    def _count_missions(self):
        """Count missions using streaming"""
        if not self.campaign_file: return 0
        return sj.count_array(self.game_loc + self.campaign_file, 'missions')

    def load_campaign(self, campaign_file):
        """Set campaign file for on-demand loading"""
        self.campaign_file = campaign_file
        self._mission_cache = None
        self._mission_cache_idx = -1
        self.current_campaign = sj.read_field(self.game_loc + campaign_file, 'title')
        return self.current_campaign is not None

    def save_progress(self):
        """Save current campaign progress"""
        if not self.current_campaign: return False
        self.campaign_saves[self.current_campaign] = {"mission": self.current_mission, "score": self.total_score}
        try:
            import json
            with open(self.game_loc + "campaign_saves.json", 'w') as f:
                f.write(json.dumps(self.campaign_saves))
            return True
        except: return False

    def load_progress(self, campaign_title):
        """Load saved progress for a campaign"""
        if campaign_title in self.campaign_saves:
            save_data = self.campaign_saves[campaign_title]
            self.current_mission = save_data["mission"]
            self.total_score = save_data["score"]
            return True
        return False

    def select_campaign_menu(self):
        """Show menu to select a campaign"""
        if not self.campaigns:
            self.show_message("No campaigns available", "Please add campaign files to the game directory")
            return None
        campaigns = self.campaign_order
        selected = 0
        if IS_THUMBY_COLOR:
            campaign_spacing, header_y, line_y, first_campaign_y = 30, 17, 31, 38
            back_button_y, tag_margin, line_spacing, text_offset_x = PC.HEIGHT - PC.FONT_HEIGHT - 15, 4, PC.FONT_HEIGHT + 2, 4
        else:
            campaign_spacing, header_y, line_y, first_campaign_y = 13, 0, 7, 12
            back_button_y, tag_margin, line_spacing, text_offset_x = PC.HEIGHT - PC.FONT_HEIGHT, 2, PC.FONT_HEIGHT + 1, 0
        fw = PC.FONT_WIDTH + PC.FONT_SPACE
        while True:
            display.fill(0)
            if self.background: self.background.run(0)
            header_text = "SELECT CAMPAIGN"
            display.drawText(header_text, (PC.WIDTH - len(header_text) * fw) // 2, header_y, PC.WHITE)
            display.drawLine(0, line_y, PC.WIDTH, line_y, PC.WHITE)
            start_idx = max(0, selected - (0 if selected == 0 else 1))
            for i in range(start_idx, min(start_idx + 2, len(campaigns))):
                campaign_y = first_campaign_y + (i - start_idx) * campaign_spacing
                text_color = PC.WHITE if i == selected else PC.LIGHTGRAY
                campaign_name = campaigns[i]
                tag_text = "CON" if campaigns[i] in self.campaign_saves else "NEW"
                tag_width = len(tag_text) * fw + tag_margin * 2
                available_width = PC.WIDTH - 8 - tag_width
                max_chars = available_width // fw
                tag_x = PC.WIDTH - tag_width
                if len(campaign_name) * fw <= available_width:
                    text_y = campaign_y + (campaign_spacing - PC.FONT_HEIGHT) // 2
                    display.drawText(campaign_name, 8, text_y, text_color)
                    display.drawText(tag_text, tag_x, text_y, text_color)
                else:
                    split_point = max_chars - 1
                    while split_point > 0 and campaign_name[split_point] != ' ': split_point -= 1
                    if split_point == 0:
                        first_line, second_line = campaign_name[:max_chars], campaign_name[max_chars:]
                    else:
                        first_line, second_line = campaign_name[:split_point], campaign_name[split_point+1:]
                    total_text_height = PC.FONT_HEIGHT * 2 + line_spacing
                    start_y = campaign_y + (campaign_spacing - total_text_height) // 2
                    display.drawText(first_line, 8, start_y, text_color)
                    display.drawText(second_line, 8, start_y + line_spacing, text_color)
                    display.drawText(tag_text, tag_x, start_y, text_color)
            cursor_y = first_campaign_y + (selected - start_idx) * campaign_spacing + (campaign_spacing - PC.FONT_HEIGHT) // 2
            display.drawText(">", text_offset_x, cursor_y, PC.WHITE)
            display.drawText("B:Back", 4 + text_offset_x, back_button_y, PC.LIGHTGRAY)
            display.update()
            if buttonU.justPressed(): selected = (selected - 1) % len(campaigns);
            elif buttonD.justPressed(): selected = (selected + 1) % len(campaigns);
            elif buttonA.justPressed(): return campaigns[selected]
            elif buttonB.justPressed(): return None

    def show_scrolling_text(self, title, text, continue_text="A to continue", type=0, actions=None):
        """Display scrolling text screen with title and content"""
        display.setFont(PC.FONT_FILE, PC.FONT_WIDTH, PC.FONT_HEIGHT, PC.FONT_SPACE)
        fw, fh = PC.FONT_WIDTH + PC.FONT_SPACE, PC.FONT_HEIGHT
        TEXT_SCROLL_DELAY = 40
        if IS_THUMBY_COLOR:
            if type == 0: header_y, line_y, content_y0, text_x, text_w, content_h, actions_y, actions_h, scroll_x, TEXT_SCROLL_DELAY  = 14, 23, 27, 10, 114, 82, 118, 10, 115, 20
            elif type == 1: header_y, line_y, content_y0, text_x, text_w, content_h, actions_y, actions_h, scroll_x, TEXT_SCROLL_DELAY = 5, 15, 28, 3, 95, 54 if actions else 66, 116, 10, 123, 20
            else: header_y, line_y, content_y0, text_x, text_w, content_h, actions_y, actions_h, scroll_x = 65, 74, 76, 3, 120, 42, 110, 16, 123
        else:
            header_y, line_y, content_y0, text_x, text_w = 0, 6, 8, 2, 66
            content_h, actions_y, actions_h, scroll_x = (20, 33, 7, 68) if actions else (26, 33, 7, 68)
        wrapped = []
        for p in text.split("\n"):
            if not p.strip(): wrapped.append(""); continue
            line = ""
            for w in p.split():
                test = line + w + " "
                if len(test) * fw <= text_w: line = test
                else:
                    if line: wrapped.append(line)
                    line = w + " "
            if line: wrapped.append(line)
        text_h = len(wrapped) * fh
        scroll, max_scroll = 0, max(0, text_h - content_h)
        last_t, sel = ticks_ms(), 0 if actions else -1
        while True:
            display.fill(0)
            if self.background: self.background.run(type)
            display.drawText(title, (PC.WIDTH - len(title) * fw) // 2, header_y, PC.WHITE)
            display.drawLine(0, line_y, PC.WIDTH, line_y, PC.WHITE)
            cy = content_y0 - scroll
            for ln in wrapped:
                if content_y0 <= cy < content_y0 + content_h and ln.strip():
                    display.drawText(ln, text_x, cy, PC.LIGHTGRAY)
                cy += fh
            if actions:
                display.drawFilledRectangle(0, actions_y, PC.WIDTH, actions_h, PC.BLACK)
                n = len(actions)
                if n == 2: pos = [2, PC.WIDTH - len(actions[1]) * fw - 2]
                elif n == 3: pos = [2, len(actions[0]) * fw + 4, PC.WIDTH - len(actions[2]) * fw - 2]
                else: pos = [i * PC.WIDTH // n + 2 for i in range(n)]
                for i, a in enumerate(actions):
                    display.drawText(a, pos[i], actions_y + 1, PC.WHITE if i == sel else PC.LIGHTGRAY)
            elif scroll >= max_scroll:
                display.drawText(continue_text, (PC.WIDTH - len(continue_text) * fw) // 2, PC.HEIGHT - fh - 1, PC.WHITE)
            if scroll > 0: display.drawText("^", scroll_x, content_y0, PC.WHITE)
            if scroll < max_scroll: display.drawText("v", scroll_x, content_y0 + content_h - fh, PC.WHITE)
            display.update()
            t = ticks_ms()
            if buttonB.justPressed(): return "back" if actions else None
            if actions and buttonL.justPressed(): sel = (sel - 1) % len(actions);
            elif actions and buttonR.justPressed(): sel = (sel + 1) % len(actions);
            elif buttonA.justPressed():
                if actions: return actions[sel].lower()
                elif scroll >= max_scroll: return None
            elif buttonU.pressed() and scroll > 0 and ticks_diff(t, last_t) > TEXT_SCROLL_DELAY: scroll -= 2; last_t = t
            elif buttonD.pressed() and scroll < max_scroll and ticks_diff(t, last_t) > TEXT_SCROLL_DELAY: scroll += 2; last_t = t

    def campaign_info_screen(self, campaign_title):
        """Show campaign info and ask to start new or continue"""
        campaign = self.campaigns[campaign_title]
        has_save = campaign_title in self.campaign_saves
        actions = ["CONTINUE", "NEW", "BACK"] if has_save else ["START", "BACK"]
        result = self.show_scrolling_text("Campaign Info", campaign_title+"\n\n"+campaign["description"], type=0, actions=actions)
        if result == "continue" or result == "start": return "continue" if has_save and result == "continue" else "new"
        elif result == "new": return "new"
        return "back"

    def show_mission_briefing(self, mission):
        """Show mission briefing for the current mission"""
        m = self._get_mission(self.current_mission)
        if not m: return
        title = f"MISSION {self.current_mission + 1}"
        text = f"{m.get('name','')}\n\n{m.get('briefing','')}"
        obj = m.get("objectives", {})
        if obj:
            text += "\n\nMISSION OBJECTIVES:"
            if "survive_time" in obj: text += f"\n- Survive for {obj['survive_time']} seconds"
            if "kills" in obj: text += f"\n- Destroy {obj['kills']} enemies / asteroids"
        self.show_scrolling_text(title, text, type=1)

    def show_mission_debriefing(self, mission_score):
        """Show mission debriefing with score and continue story"""
        m = self._get_mission(self.current_mission)
        if not m: return False
        title = f"MISSION {self.current_mission + 1}"
        text = f"Mission Completed!\n\nScore: {mission_score}\nTotal: {self.total_score + mission_score}\n\n{m.get('debriefing','')}"
        self.show_scrolling_text(title, text, type=2)
        self.total_score += mission_score
        self.current_mission += 1
        self._mission_cache = None
        self._mission_cache_idx = -1
        self.save_progress()
        if self.current_mission >= self._count_missions():
            self.show_campaign_complete()
            return True
        return False

    def show_campaign_complete(self):
        """Show campaign completion screen"""
        if not self.campaign_file: return
        outro = sj.read_field(self.game_loc + self.campaign_file, 'outro') or 'Congratulations on completing the campaign!'
        self.show_scrolling_text("CAMPAIGN COMPLETE", f"Total Score: {self.total_score}\n\n{outro}")
        if self.current_campaign in self.campaign_saves:
            del self.campaign_saves[self.current_campaign]
            self.save_progress()

    def show_message(self, title, message):
        """Show a simple message box"""
        display.fill(0)
        if self.background: self.background.run(0)
        bw, bh, bx, by = PC.WIDTH - 10, 60, 5, 10
        display.drawRectangle(bx, by, bw, bh, PC.WHITE)
        display.drawFilledRectangle(bx, by, bw, PC.FONT_HEIGHT + 4, PC.WHITE)
        display.drawText(title, bx + 4, by + 4, PC.BLACK)
        display.drawText(message[:PC.WIDTH // PC.FONT_WIDTH], bx + 4, by + PC.FONT_HEIGHT + 20, PC.WHITE)
        display.drawText("Press A to continue", bx + 4, by + bh - PC.FONT_HEIGHT - 10, PC.WHITE)
        display.update()
        while not buttonA.justPressed(): display.update()
        sleep(0.2)

    def get_mission_config(self):
        """Get the configuration for the current mission"""
        m = self._get_mission(self.current_mission)
        return m.get("config") if m else None

    def get_mission_objectives(self):
        """Get the objectives for the current mission"""
        m = self._get_mission(self.current_mission)
        return m.get("objectives", {}) if m else {}

    def run_campaign_menu(self, background=None):
        """Main method to run the campaign selection and management"""
        self.background = background
        while True:
            campaign_title = self.select_campaign_menu()
            if not campaign_title: return None
            action = self.campaign_info_screen(campaign_title)
            if action == "back": continue
            elif not action: return None
            campaign_file = self.campaigns[campaign_title]["file"]
            if not self.load_campaign(campaign_file):
                self.show_message("Error", "Failed to load campaign")
                return None
            if action == "continue": self.load_progress(campaign_title)
            else:
                self.current_mission = 0
                self.total_score = 0
                intro = sj.read_field(self.game_loc + self.campaign_file, 'intro')
                if intro: self.show_scrolling_text("INTRODUCTION", intro)
            return self

    def run_post_mission_menu(self, mission_score):
        """Show post-mission menu with options to continue, save, or exit"""
        if self.show_mission_debriefing(mission_score): return "complete"
        selected, options = 0, ["CONTINUE", "SAVE & EXIT"]
        while True:
            display.fill(0)
            if self.background: self.background.run(0)
            header_text = "MISSION COMPLETE"
            display.drawText(header_text, (PC.WIDTH - len(header_text) * (PC.FONT_WIDTH+PC.FONT_SPACE)) // 2, 2*PC.SCREEN_SCALE, PC.WHITE)
            display.drawLine(0, 9*PC.SCREEN_SCALE, PC.WIDTH, 9*PC.SCREEN_SCALE, PC.WHITE)
            for i, option in enumerate(options):
                y_pos = (15*PC.SCREEN_SCALE) + i * (PC.FONT_HEIGHT * 2)
                display.drawText(option, (PC.WIDTH - len(option) * PC.FONT_WIDTH) // 2, y_pos, PC.WHITE if i == selected else PC.LIGHTGRAY)
            display.update()
            if buttonU.justPressed(): selected = (selected - 1) % len(options);
            elif buttonD.justPressed(): selected = (selected + 1) % len(options);
            elif buttonA.justPressed(): return "continue" if selected == 0 else "exit"

    def show_mission_failed(self, attempt, max_attempts):
        """Show mission failed screen with attempt information"""
        display.fill(0)
        if self.background: self.background.run(0)
        display.setFont("/lib/font5x7.bin", 5, 7, 1)
        display.drawText("MISSION", (PC.WIDTH - 7 * (PC.FONT_WIDTH+PC.FONT_SPACE)) // 2, 10*PC.SCREEN_SCALE, PC.WHITE)
        display.drawText("FAILED", (PC.WIDTH - 6 * (PC.FONT_WIDTH+PC.FONT_SPACE)) // 2, 20*PC.SCREEN_SCALE, PC.WHITE)
        display.update()
        sleep(1)
        display.setFont("/lib/font3x5.bin", 3, 5, 1)
        display.fill(0)
        if self.background: self.background.run(0)
        display.drawText(f"Attempt {attempt} of {max_attempts}", 4, 10*PC.SCREEN_SCALE, PC.WHITE)
        display.drawText("Press A to retry", 4, 20*PC.SCREEN_SCALE, PC.WHITE)
        display.update()
        while not buttonA.justPressed(): display.update()
        sleep(0.2)

    def show_mission_success(self):
        """Show mission success screen"""
        display.fill(0)
        if self.background: self.background.run(0)
        display.setFont("/lib/font5x7.bin", 5, 7, 1)
        display.drawText("MISSION", (PC.WIDTH - 7 * (PC.FONT_WIDTH+PC.FONT_SPACE)) // 2, 10*PC.SCREEN_SCALE, PC.WHITE)
        display.drawText("COMPLETE", (PC.WIDTH - 8 * (PC.FONT_WIDTH+PC.FONT_SPACE)) // 2, 20*PC.SCREEN_SCALE, PC.WHITE)
        display.update()
        sleep(2)
        display.setFont("/lib/font3x5.bin", 3, 5, 1)
