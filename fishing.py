import random

class FishingModule:
    def __init__(self, player):
        self.player = player  # Reference the Monopoly player
        self.fish_types = {
            "Carp": 5,
            "Bass": 8,
            "Salmon": 12,
            "Trout": 7,
            "Cod": 6
        }

    def fish(self):
        """Simulate fishing"""
        caught_fish = random.choice(list(self.fish_types.keys()))
        self.player.add_fish(caught_fish)
        self.player.show_inventory()  # Show updated inventory
