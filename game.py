"""
Main game logic for Dungeon Delver
"""
import random
from typing import List, Optional, Tuple
import constants as c
from entities import Player, Enemy, Item
from dungeon import Dungeon
import combat


class Game:
    """Main game state"""
    def __init__(self):
        self.player: Optional[Player] = None
        self.dungeon: Optional[Dungeon] = None
        self.enemies: List[Enemy] = []
        self.items: List[Item] = []
        self.current_level = 1
        self.game_over = False
        self.victory = False
        self.messages: List[str] = []
        self.max_messages = 10

    def start_new_game(self):
        """Start a new game"""
        self.current_level = 1
        self.game_over = False
        self.victory = False
        self.messages = []
        self._generate_level()
        self.add_message("Welcome to Dungeon Delver! Descend the dungeon and defeat enemies.")
        self.add_message("Use WASD or Arrow Keys to move. Bump into enemies to attack.")

    def _generate_level(self):
        """Generate a new dungeon level"""
        self.dungeon = Dungeon(c.GRID_WIDTH, c.GRID_HEIGHT)
        start_x, start_y = self.dungeon.generate()

        # Create player or move to new level
        if self.player is None:
            self.player = Player(start_x, start_y)
        else:
            self.player.set_pos(start_x, start_y)

        # Spawn enemies
        self._spawn_enemies()

        # Spawn items
        self._spawn_items()

        self.add_message(f"Entered dungeon level {self.current_level}.")

    def _spawn_enemies(self):
        """Spawn enemies on current level"""
        self.enemies = []
        level_modifier = 1.0 + (self.current_level - 1) * 0.3

        num_enemies = c.ENEMIES_PER_LEVEL_BASE + self.current_level

        for _ in range(num_enemies):
            # Choose enemy type based on level
            if self.current_level == 1:
                enemy_types = [c.ENEMY_GOBLIN] * 10
            elif self.current_level <= 3:
                enemy_types = [c.ENEMY_GOBLIN] * 6 + [c.ENEMY_SKELETON] * 4
            elif self.current_level <= 5:
                enemy_types = [c.ENEMY_GOBLIN] * 3 + [c.ENEMY_SKELETON] * 6 + [c.ENEMY_DRAGON] * 1
            else:
                enemy_types = [c.ENEMY_GOBLIN] * 2 + [c.ENEMY_SKELETON] * 5 + [c.ENEMY_DRAGON] * 3

            enemy_type = random.choice(enemy_types)
            x, y = self._get_spawn_position()
            enemy = Enemy(x, y, enemy_type, level_modifier)
            self.enemies.append(enemy)

    def _spawn_items(self):
        """Spawn items on current level"""
        self.items = []

        for _ in range(c.ITEMS_PER_LEVEL):
            item_types = [c.ITEM_HEALTH_POTION, c.ITEM_SWORD, c.ITEM_SHIELD]
            weights = [5, 3, 2]  # Health potions more common
            item_type = random.choices(item_types, weights=weights)[0]

            x, y = self._get_spawn_position()
            item = Item(x, y, item_type)
            self.items.append(item)

    def _get_spawn_position(self) -> Tuple[int, int]:
        """Get a valid spawn position away from player"""
        attempts = 0
        while attempts < 50:
            x, y = self.dungeon.get_random_floor_position()

            # Check distance from player
            if self.player:
                dist = abs(x - self.player.x) + abs(y - self.player.y)
                if dist > 5:  # Spawn at least 5 tiles away
                    # Check not occupied
                    if not self._is_position_occupied(x, y):
                        return (x, y)

            attempts += 1

        # Fallback
        return self.dungeon.get_random_floor_position()

    def _is_position_occupied(self, x: int, y: int) -> bool:
        """Check if position is occupied by entity"""
        if self.player and self.player.x == x and self.player.y == y:
            return True

        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return True

        return False

    def player_move(self, dx: int, dy: int) -> bool:
        """
        Attempt to move player.
        Returns True if turn was consumed.
        """
        if self.game_over or not self.player:
            return False

        new_x = self.player.x + dx
        new_y = self.player.y + dy

        # Check if trying to attack enemy
        enemy = self._get_enemy_at(new_x, new_y)
        if enemy:
            self._player_attack(enemy)
            self._enemy_turn()
            return True

        # Check if walkable
        if not self.dungeon.is_walkable(new_x, new_y):
            return False

        # Check for stairs
        if self.dungeon.get_tile(new_x, new_y) == c.TILE_STAIRS:
            self.player.set_pos(new_x, new_y)
            self._descend_stairs()
            return True

        # Move player
        self.player.set_pos(new_x, new_y)

        # Check for item pickup
        self._check_item_pickup()

        # Enemy turn
        self._enemy_turn()

        return True

    def _player_attack(self, enemy: Enemy):
        """Player attacks enemy"""
        message, enemy_died, xp = combat.player_attack_enemy(self.player, enemy)
        self.add_message(message)

        if enemy_died:
            self.enemies.remove(enemy)
            leveled_up = self.player.gain_xp(xp)
            if leveled_up:
                self.add_message(f"Level up! You are now level {self.player.level}!")

    def _enemy_turn(self):
        """Process enemy turns"""
        if self.game_over:
            return

        for enemy in self.enemies[:]:  # Copy list to allow modification
            # Get AI action
            dx, dy = enemy.get_ai_action(self.player.get_pos(), self.dungeon)
            new_x = enemy.x + dx
            new_y = enemy.y + dy

            # Check if attacking player
            if new_x == self.player.x and new_y == self.player.y:
                message, player_died = combat.enemy_attack_player(enemy, self.player)
                self.add_message(message)

                if player_died:
                    self.game_over = True
                    self.add_message("GAME OVER! Press R to restart.")
                    return

            # Move if walkable and not occupied
            elif self.dungeon.is_walkable(new_x, new_y):
                if not self._is_position_occupied(new_x, new_y):
                    enemy.set_pos(new_x, new_y)

    def _check_item_pickup(self):
        """Check if player is on item and pick it up"""
        for item in self.items[:]:
            if item.x == self.player.x and item.y == self.player.y:
                self.player.add_item(item)
                self.items.remove(item)
                self.add_message(f"Picked up {item.get_name()}!")

    def _descend_stairs(self):
        """Descend to next level"""
        self.current_level += 1
        self.add_message(f"Descending to level {self.current_level}...")
        self._generate_level()

    def _get_enemy_at(self, x: int, y: int) -> Optional[Enemy]:
        """Get enemy at position"""
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return enemy
        return None

    def add_message(self, message: str):
        """Add message to message log"""
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def get_entity_at(self, x: int, y: int):
        """Get entity at position for rendering"""
        if self.player and self.player.x == x and self.player.y == y:
            return self.player

        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return enemy

        for item in self.items:
            if item.x == x and item.y == y:
                return item

        return None
