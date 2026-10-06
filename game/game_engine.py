import random
import pygame
from game.button import ChoiceButton


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.choices = ["ROCK", "PAPER", "SCISSORS"]

        # ---------------------------------------------
        # Task 3: Adaptive AI history
        # ---------------------------------------------
        self.player_history = []
        self.history_limit = 5

        # ---------------------------------------------
        # Button layout
        # ---------------------------------------------
        btn_w, btn_h = 130, 50
        gap = 20

        total_w = 3 * btn_w + 2 * gap
        start_x = (width - total_w) // 2

        self.btn_y = height - 85

        self.buttons = [
            ChoiceButton(
                "ROCK",
                pygame.Rect(
                    start_x,
                    self.btn_y,
                    btn_w,
                    btn_h
                ),
                (160, 50, 50),
                (200, 70, 70)
            ),

            ChoiceButton(
                "PAPER",
                pygame.Rect(
                    start_x + btn_w + gap,
                    self.btn_y,
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
                    self.btn_y,
                    btn_w,
                    btn_h
                ),
                (180, 140, 30),
                (220, 180, 50)
            ),
        ]

        # ---------------------------------------------
        # Choices
        # ---------------------------------------------
        self.player_choice = None
        self.cpu_choice = None

        # ---------------------------------------------
        # Task 4: Reveal animation state
        # ---------------------------------------------
        self.pending_player_choice = None
        self.pending_cpu_choice = None

        self.reveal_active = False
        self.reveal_start_time = 0
        self.reveal_duration = 1400

        # ---------------------------------------------
        # Result
        # ---------------------------------------------
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        # ---------------------------------------------
        # Scores
        # ---------------------------------------------
        self.player_score = 0
        self.cpu_score = 0

        # ---------------------------------------------
        # Task 2: First to 5 wins
        # ---------------------------------------------
        self.target_score = 5
        self.game_over = False
        self.match_winner = ""

        self.round_resolved_time = 0
        self.display_duration = 1800
        self.showing_result = False

        # ---------------------------------------------
        # Fonts
        # ---------------------------------------------
        self.font_title = pygame.font.SysFont(None, 36)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_arena = pygame.font.SysFont(None, 32)
        self.font_countdown = pygame.font.SysFont(None, 72)
        self.font_icon_label = pygame.font.SysFont(None, 24)

    # =================================================
    # TASK 1: DETERMINE WINNER
    # =================================================

    def determine_winner(self, player, cpu):
        if player == cpu:
            return "TIE"

        rules = {
            ("ROCK", "SCISSORS"): "PLAYER",
            ("SCISSORS", "PAPER"): "PLAYER",
            ("PAPER", "ROCK"): "PLAYER",

            ("SCISSORS", "ROCK"): "CPU",
            ("PAPER", "SCISSORS"): "CPU",
            ("ROCK", "PAPER"): "CPU",
        }

        return rules.get((player, cpu), "TIE")

    # =================================================
    # TASK 3: ADAPTIVE AI
    # =================================================

    def get_cpu_choice(self):
        # Until enough history exists, use normal random AI.
        if len(self.player_history) < 3:
            return random.choice(self.choices)

        recent = self.player_history[-self.history_limit:]

        # Find the player's most frequently used choice.
        favorite = max(
            self.choices,
            key=recent.count
        )

        # If player repeatedly uses the same choice,
        # bias CPU toward the counter.
        if recent.count(favorite) >= 3:

            counters = {
                "ROCK": "PAPER",
                "PAPER": "SCISSORS",
                "SCISSORS": "ROCK",
            }

            counter = counters[favorite]

            # 70% chance to use the counter.
            if random.random() < 0.7:
                return counter

        # Otherwise use normal random choice.
        return random.choice(self.choices)

    # =================================================
    # TASK 4: PROCEDURAL GESTURE ICONS
    # =================================================

    def draw_gesture_icon(
        self,
        screen,
        choice,
        center,
        size,
        shake=0
    ):
        x = int(center[0] + shake)
        y = int(center[1])

        # ---------------------------------------------
        # ROCK
        # ---------------------------------------------
        if choice == "ROCK":

            pygame.draw.circle(
                screen,
                (150, 150, 160),
                (x, y + 5),
                size // 2
            )

            # Knuckles
            for offset in (-18, -6, 6, 18):
                pygame.draw.circle(
                    screen,
                    (185, 185, 195),
                    (x + offset, y - 18),
                    10
                )

            # Thumb
            pygame.draw.circle(
                screen,
                (170, 170, 180),
                (x + 28, y + 15),
                12
            )

            # Outline
            pygame.draw.circle(
                screen,
                (110, 110, 120),
                (x, y + 5),
                size // 2,
                3
            )

        # ---------------------------------------------
        # PAPER
        # ---------------------------------------------
        elif choice == "PAPER":

            palm_rect = pygame.Rect(
                x - 35,
                y - 5,
                70,
                65
            )

            pygame.draw.rect(
                screen,
                (235, 235, 220),
                palm_rect,
                border_radius=12
            )

            finger_positions = [-30, -10, 10, 30]

            for finger_x in finger_positions:

                finger_rect = pygame.Rect(
                    x + finger_x - 7,
                    y - 45,
                    14,
                    55
                )

                pygame.draw.rect(
                    screen,
                    (245, 245, 230),
                    finger_rect,
                    border_radius=7
                )

            pygame.draw.rect(
                screen,
                (120, 120, 125),
                palm_rect,
                3,
                border_radius=12
            )

        # ---------------------------------------------
        # SCISSORS
        # ---------------------------------------------
        elif choice == "SCISSORS":

            # Upper blade
            pygame.draw.line(
                screen,
                (210, 215, 220),
                (x - 30, y - 30),
                (x + 15, y + 15),
                10
            )

            # Lower blade
            pygame.draw.line(
                screen,
                (210, 215, 220),
                (x - 30, y + 30),
                (x + 15, y - 15),
                10
            )

            # Handles
            pygame.draw.circle(
                screen,
                (210, 80, 80),
                (x - 35, y - 32),
                15,
                5
            )

            pygame.draw.circle(
                screen,
                (210, 80, 80),
                (x - 35, y + 32),
                15,
                5
            )

            # Center joint
            pygame.draw.circle(
                screen,
                (120, 125, 130),
                (x + 15, y),
                7
            )

    # =================================================
    # TASK 4: REVEAL SYMBOL
    # =================================================

    def draw_reveal_symbol(
        self,
        screen,
        center,
        shake=0
    ):
        x = int(center[0] + shake)
        y = int(center[1])

        pygame.draw.circle(
            screen,
            (70, 75, 90),
            (x, y),
            55
        )

        pygame.draw.circle(
            screen,
            (180, 185, 200),
            (x, y),
            55,
            4
        )

        question = self.font_countdown.render(
            "?",
            True,
            (245, 245, 250)
        )

        screen.blit(
            question,
            (
                x - question.get_width() // 2,
                y - question.get_height() // 2
            )
        )

    # =================================================
    # PLAY ROUND
    # =================================================

    def play_round(self, choice):

        if self.game_over or self.reveal_active:
            return

        # Store player's choice.
        self.pending_player_choice = choice

        # Adaptive CPU chooses based on previous history.
        self.pending_cpu_choice = self.get_cpu_choice()

        # Add current player choice to history.
        self.player_history.append(choice)

        if len(self.player_history) > self.history_limit:
            self.player_history.pop(0)

        # Hide actual choices during countdown.
        self.player_choice = None
        self.cpu_choice = None

        self.result_text = "Get ready..."
        self.result_color = (220, 225, 235)

        # Start reveal animation.
        self.reveal_active = True
        self.reveal_start_time = pygame.time.get_ticks()
        self.showing_result = False

    # =================================================
    # RESOLVE ROUND
    # =================================================

    def resolve_round(self):

        self.player_choice = self.pending_player_choice
        self.cpu_choice = self.pending_cpu_choice

        outcome = self.determine_winner(
            self.player_choice,
            self.cpu_choice
        )

        # ---------------------------------------------
        # PLAYER WINS
        # ---------------------------------------------
        if outcome == "PLAYER":

            self.player_score += 1

            self.result_text = (
                f"You Win! "
                f"{self.player_choice} beats "
                f"{self.cpu_choice}."
            )

            self.result_color = (80, 230, 120)

            if self.player_score >= self.target_score:
                self.game_over = True
                self.match_winner = "PLAYER"

        # ---------------------------------------------
        # CPU WINS
        # ---------------------------------------------
        elif outcome == "CPU":

            self.cpu_score += 1

            self.result_text = (
                f"You Lose! "
                f"{self.cpu_choice} beats "
                f"{self.player_choice}."
            )

            self.result_color = (240, 80, 80)

            if self.cpu_score >= self.target_score:
                self.game_over = True
                self.match_winner = "CPU"

        # ---------------------------------------------
        # DRAW
        # ---------------------------------------------
        else:

            self.result_text = (
                f"It's a Draw! "
                f"Both picked {self.player_choice}."
            )

            self.result_color = (240, 210, 80)

        self.showing_result = True
        self.round_resolved_time = pygame.time.get_ticks()

    # =================================================
    # EVENTS
    # =================================================

    def handle_event(self, event):

        # Restart match
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_r
        ):

            self.player_score = 0
            self.cpu_score = 0

            self.player_choice = None
            self.cpu_choice = None

            self.pending_player_choice = None
            self.pending_cpu_choice = None

            self.player_history = []

            self.result_text = "Make your move!"
            self.result_color = (220, 225, 235)

            self.game_over = False
            self.match_winner = ""

            self.reveal_active = False
            self.showing_result = False

        # Mouse click
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            for btn in self.buttons:

                if btn.contains(event.pos):
                    self.play_round(btn.choice_name)
                    break

    # =================================================
    # UPDATE
    # =================================================

    def update(self):

        now = pygame.time.get_ticks()

        # ---------------------------------------------
        # Reveal animation
        # ---------------------------------------------
        if self.reveal_active:

            elapsed = now - self.reveal_start_time

            if elapsed >= self.reveal_duration:

                self.reveal_active = False
                self.resolve_round()

            return

        # ---------------------------------------------
        # Clear round result after a short delay
        # ---------------------------------------------
        if (
            self.showing_result
            and not self.game_over
            and now - self.round_resolved_time
            >= self.display_duration
        ):

            self.player_choice = None
            self.cpu_choice = None

            self.result_text = "Make your move!"
            self.result_color = (190, 195, 205)

            self.showing_result = False

    # =================================================
    # RENDER
    # =================================================

    def render(self, screen):

        screen.fill((24, 28, 36))

        # ---------------------------------------------
        # Title
        # ---------------------------------------------

        title_surf = self.font_title.render(
            "Rock Paper Scissors",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2
                - title_surf.get_width() // 2,
                14
            )
        )

        # ---------------------------------------------
        # Scores
        # ---------------------------------------------

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

        screen.blit(
            p_surf,
            (35, 52)
        )

        screen.blit(
            c_surf,
            (
                self.width
                - c_surf.get_width()
                - 35,
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

        # =================================================
        # REVEAL ANIMATION
        # =================================================

        if self.reveal_active:

            elapsed = (
                pygame.time.get_ticks()
                - self.reveal_start_time
            )

            # Animated shaking.
            shake = int(
                8 * ((elapsed // 80) % 2)
            )

            if (elapsed // 80) % 2 == 1:
                shake = -shake

            # Left reveal symbol.
            self.draw_reveal_symbol(
                screen,
                (
                    self.width // 2 - 150,
                    175
                ),
                shake
            )

            # Right reveal symbol.
            self.draw_reveal_symbol(
                screen,
                (
                    self.width // 2 + 150,
                    175
                ),
                -shake
            )

            # Countdown.
            countdown_step = elapsed // 350

            if countdown_step < 3:
                countdown_text = str(
                    3 - countdown_step
                )
            else:
                countdown_text = "REVEAL!"

            countdown_surf = self.font_countdown.render(
                countdown_text,
                True,
                (245, 225, 90)
            )

            screen.blit(
                countdown_surf,
                (
                    self.width // 2
                    - countdown_surf.get_width() // 2,
                    245
                )
            )

            # Player label.
            left_label = self.font_icon_label.render(
                "PLAYER",
                True,
                (100, 180, 255)
            )

            screen.blit(
                left_label,
                (
                    self.width // 2
                    - 150
                    - left_label.get_width() // 2,
                    110
                )
            )

            # CPU label.
            right_label = self.font_icon_label.render(
                "CPU",
                True,
                (255, 120, 120)
            )

            screen.blit(
                right_label,
                (
                    self.width // 2
                    + 150
                    - right_label.get_width() // 2,
                    110
                )
            )

        # =================================================
        # AFTER REVEAL
        # =================================================

        else:

            # ---------------------------------------------
            # Actual player icon
            # ---------------------------------------------

            if self.player_choice:

                self.draw_gesture_icon(
                    screen,
                    self.player_choice,
                    (
                        self.width // 2 - 150,
                        170
                    ),
                    70
                )

            # ---------------------------------------------
            # Actual CPU icon
            # ---------------------------------------------

            if self.cpu_choice:

                self.draw_gesture_icon(
                    screen,
                    self.cpu_choice,
                    (
                        self.width // 2 + 150,
                        170
                    ),
                    70
                )

            # ---------------------------------------------
            # Player choice label
            # ---------------------------------------------

            if self.player_choice:

                player_label = self.font_icon_label.render(
                    self.player_choice,
                    True,
                    (100, 180, 255)
                )

                screen.blit(
                    player_label,
                    (
                        self.width // 2
                        - 150
                        - player_label.get_width() // 2,
                        235
                    )
                )

            # ---------------------------------------------
            # CPU choice label
            # ---------------------------------------------

            if self.cpu_choice:

                cpu_label = self.font_icon_label.render(
                    self.cpu_choice,
                    True,
                    (255, 120, 120)
                )

                screen.blit(
                    cpu_label,
                    (
                        self.width // 2
                        + 150
                        - cpu_label.get_width() // 2,
                        235
                    )
                )

            # =================================================
            # RESULT AREA
            # =================================================

            # Put result safely above the buttons.
            result_y = self.btn_y - 55

            # ---------------------------------------------
            # Match winner
            # ---------------------------------------------

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
                        self.width // 2
                        - winner_surf.get_width() // 2,
                        result_y - 35
                    )
                )

                screen.blit(
                    restart_surf,
                    (
                        self.width // 2
                        - restart_surf.get_width() // 2,
                        result_y
                    )
                )

            # ---------------------------------------------
            # Round result
            # ---------------------------------------------

            else:

                res_surf = self.font_arena.render(
                    self.result_text,
                    True,
                    self.result_color
                )

                screen.blit(
                    res_surf,
                    (
                        self.width // 2
                        - res_surf.get_width() // 2,
                        result_y
                    )
                )

        # =================================================
        # BUTTONS
        # =================================================

        for btn in self.buttons:
            btn.render(screen)