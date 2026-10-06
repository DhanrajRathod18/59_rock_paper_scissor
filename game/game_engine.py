import random
import pygame
from game.button import ChoiceButton


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.choices = ["ROCK", "PAPER", "SCISSORS"]

        # Task 3: Adaptive AI history
        self.player_history = []
        self.history_limit = 5

        btn_w, btn_h = 130, 50
        gap = 20
        total_w = 3 * btn_w + 2 * gap
        start_x = (width - total_w) // 2
        btn_y = height - 85

        self.buttons = [
            ChoiceButton(
                "ROCK",
                pygame.Rect(start_x, btn_y, btn_w, btn_h),
                (160, 50, 50),
                (200, 70, 70)
            ),
            ChoiceButton(
                "PAPER",
                pygame.Rect(
                    start_x + btn_w + gap,
                    btn_y,
                    btn_w,
                    btn_h
                ),
                (40, 100, 170),
                (60, 130, 210)
            ),
            ChoiceButton(
                "SCISSORS",
                pygame.Rect(
                    start_x + 2 * (btn_w + gap),
                    btn_y,
                    btn_w,
                    btn_h
                ),
                (180, 140, 30),
                (220, 180, 50)
            ),
        ]

        self.player_choice = None
        self.cpu_choice = None

        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        self.player_score = 0
        self.cpu_score = 0

        # Task 2: First to 5 wins
        self.target_score = 5
        self.game_over = False
        self.match_winner = ""

        self.round_resolved_time = 0
        self.display_duration = 1800
        self.showing_result = False

        self.font_title = pygame.font.SysFont(None, 36)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_arena = pygame.font.SysFont(None, 32)

    def determine_winner(self, player, cpu):
        if player == cpu:
            return "TIE"

        # Task 1: Correct Rock Paper Scissors rules
        rules = {
            ("ROCK", "SCISSORS"): "PLAYER",
            ("SCISSORS", "PAPER"): "PLAYER",
            ("PAPER", "ROCK"): "PLAYER",
            ("SCISSORS", "ROCK"): "CPU",
            ("PAPER", "SCISSORS"): "CPU",
            ("ROCK", "PAPER"): "CPU",
        }

        return rules.get((player, cpu), "TIE")

    # Task 3: Adaptive AI
    def get_cpu_choice(self):
        # For the first few rounds, use normal random choices
        if len(self.player_history) < 3:
            return random.choice(self.choices)

        # Look at the player's recent choices
        recent = self.player_history[-self.history_limit:]

        # Find the choice the player uses most often
        favorite = max(self.choices, key=recent.count)

        # If the player strongly favors one choice,
        # make the CPU more likely to counter it
        if recent.count(favorite) >= 3:
            counters = {
                "ROCK": "PAPER",
                "PAPER": "SCISSORS",
                "SCISSORS": "ROCK",
            }

            counter = counters[favorite]

            # 70% chance of choosing the counter
            if random.random() < 0.7:
                return counter

        # Otherwise choose randomly
        return random.choice(self.choices)

    def play_round(self, choice):
        if self.game_over:
            return

        self.player_choice = choice

        # Task 3: CPU adapts to player's previous choices
        self.cpu_choice = self.get_cpu_choice()

        # Record player's choice for future AI decisions
        self.player_history.append(choice)

        # Keep only the most recent choices
        if len(self.player_history) > self.history_limit:
            self.player_history.pop(0)

        outcome = self.determine_winner(
            self.player_choice,
            self.cpu_choice
        )

        if outcome == "PLAYER":
            self.player_score += 1

            self.result_text = (
                f"You Win! {self.player_choice} beats {self.cpu_choice}."
            )

            self.result_color = (80, 230, 120)

            if self.player_score >= self.target_score:
                self.game_over = True
                self.match_winner = "PLAYER"

        elif outcome == "CPU":
            self.cpu_score += 1

            self.result_text = (
                f"You Lose! {self.cpu_choice} beats {self.player_choice}."
            )

            self.result_color = (240, 80, 80)

            if self.cpu_score >= self.target_score:
                self.game_over = True
                self.match_winner = "CPU"

        else:
            self.result_text = (
                f"It's a Draw! Both picked {self.player_choice}."
            )

            self.result_color = (240, 210, 80)

        self.showing_result = True
        self.round_resolved_time = pygame.time.get_ticks()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.player_score = 0
            self.cpu_score = 0

            self.player_choice = None
            self.cpu_choice = None

            # Task 3: Clear AI history when restarting
            self.player_history = []

            self.result_text = "Make your move!"
            self.result_color = (220, 225, 235)

            self.game_over = False
            self.match_winner = ""
            self.showing_result = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn.contains(event.pos):
                    self.play_round(btn.choice_name)
                    break

    def update(self):
        now = pygame.time.get_ticks()

        if (
            self.showing_result
            and not self.game_over
            and now - self.round_resolved_time >= self.display_duration
        ):
            self.player_choice = None
            self.cpu_choice = None

            self.result_text = "Make your move!"
            self.result_color = (190, 195, 205)

            self.showing_result = False

    def render(self, screen):
        screen.fill((24, 28, 36))

        title_surf = self.font_title.render(
            "Rock Paper Scissors",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                14
            )
        )

        p_surf = self.font_hud.render(
            f"Player Score: {self.player_score}",
            True,
            (100, 180, 255)
        )

        c_surf = self.font_hud.render(
            f"CPU Score: {self.cpu_score}",
            True,
            (255, 120, 120)
        )

        screen.blit(p_surf, (35, 52))

        screen.blit(
            c_surf,
            (
                self.width - c_surf.get_width() - 35,
                52
            )
        )

        pygame.draw.line(
            screen,
            (45, 52, 66),
            (25, 82),
            (self.width - 25, 82),
            2
        )

        p_str = self.player_choice if self.player_choice else "--"
        c_str = self.cpu_choice if self.cpu_choice else "--"

        arena_p = self.font_arena.render(
            f"Your Pick:  {p_str}",
            True,
            (225, 225, 230)
        )

        arena_c = self.font_arena.render(
            f"CPU Pick:  {c_str}",
            True,
            (225, 225, 230)
        )

        screen.blit(
            arena_p,
            (
                self.width // 2 - arena_p.get_width() // 2,
                115
            )
        )

        screen.blit(
            arena_c,
            (
                self.width // 2 - arena_c.get_width() // 2,
                155
            )
        )

        if self.game_over:
            if self.match_winner == "PLAYER":
                winner_text = "YOU WIN THE MATCH!"
                winner_color = (80, 230, 120)
            else:
                winner_text = "CPU WINS THE MATCH!"
                winner_color = (240, 80, 80)

            winner_surf = self.font_arena.render(
                winner_text,
                True,
                winner_color
            )

            restart_surf = self.font_hud.render(
                "Press R to restart",
                True,
                (245, 245, 245)
            )

            screen.blit(
                winner_surf,
                (
                    self.width // 2 - winner_surf.get_width() // 2,
                    205
                )
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    245
                )
            )

        else:
            res_surf = self.font_arena.render(
                self.result_text,
                True,
                self.result_color
            )

            screen.blit(
                res_surf,
                (
                    self.width // 2 - res_surf.get_width() // 2,
                    205
                )
            )

        for btn in self.buttons:
            btn.render(screen)