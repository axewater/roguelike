"""
Main game logic for Dungeon Delver
"""
import random
from typing import List, Optional, Tuple
import constants as c
from entities import Player, Enemy, Item
from dungeon import Dungeon
from animations import AnimationManager
from abilities import CLASS_ABILITIES
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
        self.messages: List[Tuple[str, str]] = []  # (message, type)
        self.max_messages = 15
        self.anim_manager = AnimationManager()
        self.selected_class = c.CLASS_WARRIOR  # Default class
        self.ambient_timer = 0.0  # Timer for spawning ambient particles
        self.camera_x = 0  # Camera position (top-left of viewport in world coords)
        self.camera_y = 0

    def update_camera(self):
        """Center camera on player with boundary clamping"""
        if not self.player:
            return

        # Center camera on player
        self.camera_x = self.player.x - c.VIEWPORT_WIDTH // 2
        self.camera_y = self.player.y - c.VIEWPORT_HEIGHT // 2

        # Clamp to dungeon boundaries
        self.camera_x = max(0, min(self.camera_x, c.GRID_WIDTH - c.VIEWPORT_WIDTH))
        self.camera_y = max(0, min(self.camera_y, c.GRID_HEIGHT - c.VIEWPORT_HEIGHT))

    def start_new_game(self):
        """Start a new game"""
        self.current_level = 1
        self.game_over = False
        self.victory = False
        self.messages = []
        self._generate_level()
        self.add_message("Welcome to Dungeon Delver! Descend the dungeon and defeat enemies.", "event")
        self.add_message("Use WASD or Arrow Keys to move. Bump into enemies to attack.", "event")

    def _generate_level(self):
        """Generate a new dungeon level"""
        self.dungeon = Dungeon(c.GRID_WIDTH, c.GRID_HEIGHT)
        start_x, start_y = self.dungeon.generate()

        # Create player or move to new level
        if self.player is None:
            self.player = Player(start_x, start_y, self.selected_class)
            # Assign class-specific abilities
            self.player.abilities = CLASS_ABILITIES.get(self.selected_class, [])
        else:
            self.player.set_pos(start_x, start_y)

        # Update camera to center on player
        self.update_camera()

        # Spawn enemies
        self._spawn_enemies()

        # Spawn items
        self._spawn_items()

        self.add_message(f"Entered dungeon level {self.current_level}.", "event")

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
            # Choose item type
            item_types = [c.ITEM_HEALTH_POTION, c.ITEM_SWORD, c.ITEM_SHIELD, c.ITEM_BOOTS, c.ITEM_RING]
            weights = [5, 3, 2, 2, 2]  # Health potions more common
            item_type = random.choices(item_types, weights=weights)[0]

            # Determine rarity based on dungeon level
            rarity = self._determine_item_rarity()

            # Generate random affixes for rare+ items
            affixes = {}
            if rarity in [c.RARITY_RARE, c.RARITY_EPIC, c.RARITY_LEGENDARY]:
                affixes = self._generate_item_affixes(rarity)

            x, y = self._get_spawn_position()
            item = Item(x, y, item_type, rarity, affixes)
            self.items.append(item)

    def _determine_item_rarity(self) -> str:
        """Determine item rarity based on dungeon level"""
        # Higher levels have better drop rates
        level_factor = min(self.current_level / 10, 1.0)

        rarities = [
            c.RARITY_COMMON,
            c.RARITY_UNCOMMON,
            c.RARITY_RARE,
            c.RARITY_EPIC,
            c.RARITY_LEGENDARY
        ]

        # Weights adjusted by dungeon level
        weights = [
            max(60 - level_factor * 40, 20),  # Common: 60% -> 20%
            30 + level_factor * 10,            # Uncommon: 30% -> 40%
            8 + level_factor * 20,             # Rare: 8% -> 28%
            2 + level_factor * 8,              # Epic: 2% -> 10%
            level_factor * 2                   # Legendary: 0% -> 2%
        ]

        return random.choices(rarities, weights=weights)[0]

    def _generate_item_affixes(self, rarity: str) -> dict:
        """Generate random stat affixes for an item"""
        affixes = {}
        num_affixes = {
            c.RARITY_RARE: 1,
            c.RARITY_EPIC: 2,
            c.RARITY_LEGENDARY: 3
        }.get(rarity, 0)

        possible_stats = ["attack", "defense", "hp"]
        selected_stats = random.sample(possible_stats, min(num_affixes, len(possible_stats)))

        for stat in selected_stats:
            if stat == "hp":
                affixes["hp"] = random.randint(5, 15)
            else:
                affixes[stat] = random.randint(1, 5)

        return affixes

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
            self._reduce_ability_cooldowns()
            return True

        # Check if walkable
        if not self.dungeon.is_walkable(new_x, new_y):
            return False

        # Check for stairs
        if self.dungeon.get_tile(new_x, new_y) == c.TILE_STAIRS:
            self.player.set_pos(new_x, new_y)
            self.update_camera()
            self._descend_stairs()
            return True

        # Move player
        self.player.set_pos(new_x, new_y)
        self.update_camera()

        # Check for item pickup
        self._check_item_pickup()

        # Enemy turn
        self._enemy_turn()

        # Reduce ability cooldowns
        self._reduce_ability_cooldowns()

        return True

    def use_ability(self, ability_index: int, target_x: int = None, target_y: int = None) -> bool:
        """
        Use an ability. Returns True if turn was consumed.
        """
        if self.game_over or not self.player:
            return False

        if ability_index < 0 or ability_index >= len(self.player.abilities):
            return False

        ability = self.player.abilities[ability_index]

        # Use player position as default target
        if target_x is None or target_y is None:
            target_x = self.player.x
            target_y = self.player.y

        # Use ability
        success, message = ability.use(self.player, (target_x, target_y), self)
        self.add_message(message, "event" if success else "damage")

        if success:
            # Enemy turn
            self._enemy_turn()
            # Reduce ability cooldowns
            self._reduce_ability_cooldowns()

        return success

    def _reduce_ability_cooldowns(self):
        """Reduce all ability cooldowns by 1"""
        for ability in self.player.abilities:
            ability.reduce_cooldown()

    def _player_attack(self, enemy: Enemy):
        """Player attacks enemy"""
        message, enemy_died, xp = combat.player_attack_enemy(self.player, enemy)
        damage = combat.calculate_damage(self.player.attack, enemy.defense)

        # Check if crit (rogue has crit chance)
        is_crit = hasattr(self.player, 'crit_chance') and random.random() < getattr(self.player, 'crit_chance', 0)

        # Create animations
        from PyQt6.QtGui import QColor

        # Directional impact particles (spray away from player)
        impact_color = QColor(255, 80, 80) if not is_crit else QColor(255, 200, 50)
        self.anim_manager.add_directional_impact(
            enemy.x, enemy.y,
            self.player.x, self.player.y,
            impact_color, count=12 if not is_crit else 20, is_crit=is_crit
        )

        self.anim_manager.add_floating_text(enemy.x, enemy.y, str(damage),
                                           QColor(255, 100, 100) if not is_crit else QColor(255, 220, 50),
                                           is_crit=is_crit)
        self.anim_manager.add_flash_effect(enemy.x, enemy.y, QColor(255, 200, 200))

        if enemy_died:
            # Enhanced death effect with enemy-specific particles
            self.anim_manager.add_death_burst(enemy.x, enemy.y, enemy.enemy_type)
            self.anim_manager.add_screen_shake(4.0, 0.2)

        self.add_message(message, "damage")

        if enemy_died:
            self.enemies.remove(enemy)
            leveled_up = self.player.gain_xp(xp)
            if leveled_up:
                self.add_message(f"Level up! You are now level {self.player.level}!", "levelup")
                self.anim_manager.add_heal_sparkles(self.player.x, self.player.y)

    def _enemy_turn(self):
        """Process enemy turns"""
        if self.game_over:
            return

        for enemy in self.enemies[:]:  # Copy list to allow modification
            # Reduce status effects
            enemy.reduce_status_effects()

            # Get AI action
            dx, dy = enemy.get_ai_action(self.player.get_pos(), self.dungeon)
            new_x = enemy.x + dx
            new_y = enemy.y + dy

            # Check if attacking player
            if new_x == self.player.x and new_y == self.player.y:
                message, player_died = combat.enemy_attack_player(enemy, self.player)
                damage = combat.calculate_damage(enemy.attack, self.player.defense)

                # Create animations
                from PyQt6.QtGui import QColor

                # Directional impact particles (spray away from enemy)
                self.anim_manager.add_directional_impact(
                    self.player.x, self.player.y,
                    enemy.x, enemy.y,
                    QColor(255, 50, 50), count=10
                )

                self.anim_manager.add_floating_text(self.player.x, self.player.y, str(damage), QColor(255, 50, 50))
                self.anim_manager.add_flash_effect(self.player.x, self.player.y, QColor(255, 100, 100))

                if player_died:
                    self.anim_manager.add_screen_shake(8.0, 0.3)

                self.add_message(message, "damage")

                if player_died:
                    self.game_over = True
                    self.add_message("GAME OVER! Press R to restart.", "death")
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

                # Determine message type based on item
                if item.item_type == c.ITEM_HEALTH_POTION:
                    msg_type = "heal"
                    from PyQt6.QtGui import QColor
                    self.anim_manager.add_heal_sparkles(self.player.x, self.player.y)
                else:
                    msg_type = "item"
                    from PyQt6.QtGui import QColor
                    self.anim_manager.add_particle_burst(self.player.x, self.player.y,
                                                        QColor(255, 215, 0), count=6, particle_type="star")
                self.add_message(f"Picked up {item.get_name()}!", msg_type)

    def _descend_stairs(self):
        """Descend to next level"""
        self.current_level += 1
        self.add_message(f"Descending to level {self.current_level}...", "event")
        self._generate_level()

    def _get_enemy_at(self, x: int, y: int) -> Optional[Enemy]:
        """Get enemy at position"""
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return enemy
        return None

    def update(self, dt: float):
        """Update game state (called every frame)"""
        # Spawn ambient particles periodically
        self.ambient_timer += dt
        if self.ambient_timer >= 0.5:  # Every 0.5 seconds
            self.ambient_timer = 0.0
            # Spawn 2-4 ambient particles
            self.anim_manager.add_ambient_particles(count=random.randint(2, 4))

    def add_message(self, message: str, msg_type: str = "event"):
        """Add message to message log with type for color coding"""
        self.messages.append((message, msg_type))
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
