class MonopolyPlayer: 
    """
    Player class for Monopoly game\n
    Contains player data.\n
    """
    def __init__(self, cash: int, order: int, name: str) -> None:
        self.cash = cash
        self.properties = []
        self.order = order
        self.location = 0
        self.jail = False
        self.jail_cards = 0
        self.name = name if name != "" else "Player " + str(order)
        self.jail_turns = 0
        self.repeat_offender = 0

        self.fish_inventory = {"Carp": 0, "Bass": 0, "Salmon": 0, "Trout": 0, "Cod": 0}

    """
    Player cash\n
    @cash: int\n
    Player properties\n
    @properties: list\n
    Player location\n
    @location: int\n
    Player jail status\n
    @jail: bool\n
    """
    def buy(self, location:int, board) -> None:
        """
        Buy property\n
        @location: int\n
        """
        self.properties.append(location)
        self.cash -= board.locations[location].getPrice()
        if (board.locations[location].owner == -1):
            board.locations[location].owner = self.order
            if location == 5 or location == 15 or location == 25 or location == 35:   # railroad
                owned_rails = [k for k in [5, 15, 25, 35] if board.locations[k].owner == self.order]
                for k in owned_rails:
                    board.locations[k].houses = len(owned_rails)   
            elif location == 12: # electric company, check if water works is owned
                if board.locations[28].owner == self.order:
                    board.locations[12].houses = 2
                    board.locations[28].houses = 2
                else: board.locations[12].houses = 1
            elif location == 28: # water works, check if electric company is owned
                if board.locations[12].owner == self.order:
                    board.locations[28].houses = 2
                    board.locations[12].houses = 2
                else: board.locations[28].houses = 1
    def pay(self, amount:int) -> None:
        """
        Pay amount\n
        @amount: int\n
        """
        self.cash -= amount
    def receive(self, amount:int) -> None:
        """
        Receive amount\n
        @amount: int\n
        """
        self.cash += amount
    def go_to_jail(self) -> None:
        """
        Go to jail\n
        """
        self.location = 10
        self.jail = True
        self.jail_turns = 0
        self.repeat_offender += 1
    def leave_jail(self) -> None:
        """
        Leave jail\n
        """
        self.jail = False
        self.jail_turns = 0
    def attempt_jail_roll(self, dice: tuple) -> tuple:
        """
        Attempt to leave jail by rolling doubles
        Returns (left_jail: bool, reason: str)
        """
        self.jail_turns += 1
        if dice[0] == dice[1]:
            self.leave_jail()
            return True, "doubles"
        elif self.jail_turns == 3:
            self.pay_jail_fine()
            return True, "third_turn"
        return False, ""
    def pay_jail_fine(self) -> None:
        """
        Pay jail fine of $50
        """
        self.pay(50 * self.repeat_offender)
        self.leave_jail()
    def use_jail_card(self) -> None:
        """
        Use jail card\n
        """
        self.jail_cards -= 1
        self.leave_jail()

    def __str__(self) -> str:
        return self.name

    def add_fish(self, fish_name, quantity=1):
        """Add caught fish to inventory"""
        if fish_name in self.fish_inventory:
            self.fish_inventory[fish_name] += quantity
        print(f"🎣 You caught a {fish_name}! Added to your inventory.")

    def remove_fish(self, fish_name, quantity=1):
        """Remove fish from inventory"""
        if self.fish_inventory.get(fish_name, 0) >= quantity:
            self.fish_inventory[fish_name] -= quantity
            return True
        return False

    def show_inventory(self):
        """Display player's fish inventory"""
        print("\n📦 Your Fish Inventory:")
        for fish, qty in self.fish_inventory.items():
            if qty > 0:
                print(f" - {fish}: {qty}")
        print(f"\n💰 Balance: ${self.cash}")

    def sell_fish(self, fish_name, price):
        """Sell fish and earn money"""
        if self.remove_fish(fish_name):
            self.cash += price
            print(f"💰 Sold 1 {fish_name} for ${price}. New Balance: ${self.cash}")
        else:
            print(f"You don't have any {fish_name} to sell!")