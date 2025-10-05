"""
Entity classes for Dungeon Delver
"""
from typing import Tuple
import constants as c


class Entity:
    """Base entity class"""
    def __init__(self, x: int, y: int, entity_type: str):
        self.x = x
        self.y = y
        self.entity_type = entity_type

    def get_pos(self) -> Tuple[int, int]:
        """Get entity position"""
        return (self.x, self.y)

    def set_pos(self, x: int, y: int):
        """Set entity position"""
        self.x = x
        self.y = y


class Player(Entity):
    """Player entity"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y, c.ENTITY_PLAYER)
        self.max_hp = c.PLAYER_START_MAX_HP
        self.hp = c.PLAYER_START_HP
        self.base_attack = c.PLAYER_START_ATTACK
        self.base_defense = c.PLAYER_START_DEFENSE
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 50
        self.inventory = []
        self.weapon_bonus = 0
        self.armor_bonus = 0

    @property
    def attack(self) -> int:
        """Total attack including bonuses"""
        return self.base_attack + self.weapon_bonus

    @property
    def defense(self) -> int:
        """Total defense including bonuses"""
        return self.base_defense + self.armor_bonus

    def take_damage(self, damage: int) -> bool:
        """Take damage, return True if still alive"""
        self.hp = max(0, self.hp - damage)
        return self.hp > 0

    def heal(self, amount: int):
        """Heal HP"""
        self.hp = min(self.max_hp, self.hp + amount)

    def gain_xp(self, amount: int) -> bool:
        """Gain XP, return True if leveled up"""
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self.level_up()
            return True
        return False

    def level_up(self):
        """Level up the player"""
        self.level += 1
        self.xp = 0
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)

        # Increase stats
        self.max_hp += 20
        self.hp = self.max_hp  # Full heal on level up
        self.base_attack += 3
        self.base_defense += 2

    def add_item(self, item: 'Item'):
        """Add item to inventory and apply effects"""
        self.inventory.append(item)

        if item.item_type == c.ITEM_HEALTH_POTION:
            self.heal(c.ITEM_EFFECTS[c.ITEM_HEALTH_POTION]["heal"])
        elif item.item_type == c.ITEM_SWORD:
            self.weapon_bonus += c.ITEM_EFFECTS[c.ITEM_SWORD]["attack"]
        elif item.item_type == c.ITEM_SHIELD:
            self.armor_bonus += c.ITEM_EFFECTS[c.ITEM_SHIELD]["defense"]


class Enemy(Entity):
    """Enemy entity"""
    def __init__(self, x: int, y: int, enemy_type: str, level_modifier: float = 1.0):
        super().__init__(x, y, c.ENTITY_ENEMY)
        self.enemy_type = enemy_type

        # Get base stats and apply level modifier
        stats = c.ENEMY_STATS[enemy_type]
        self.max_hp = int(stats["hp"] * level_modifier)
        self.hp = self.max_hp
        self.attack = int(stats["attack"] * level_modifier)
        self.defense = int(stats["defense"] * level_modifier)
        self.xp_reward = int(stats["xp"] * level_modifier)

    def take_damage(self, damage: int) -> bool:
        """Take damage, return True if still alive"""
        self.hp = max(0, self.hp - damage)
        return self.hp > 0

    def get_ai_action(self, player_pos: Tuple[int, int], dungeon_map) -> Tuple[int, int]:
        """Determine next move based on AI type"""
        if self.enemy_type == c.ENEMY_GOBLIN:
            # Goblins chase the player
            return self._chase_player(player_pos)
        elif self.enemy_type == c.ENEMY_SKELETON:
            # Skeletons patrol randomly
            return self._random_move()
        elif self.enemy_type == c.ENEMY_DRAGON:
            # Dragons chase if close, otherwise patrol
            dist = abs(self.x - player_pos[0]) + abs(self.y - player_pos[1])
            if dist <= 5:
                return self._chase_player(player_pos)
            else:
                return self._random_move()
        return (0, 0)

    def _chase_player(self, player_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Move towards player"""
        dx = 0 if self.x == player_pos[0] else (1 if player_pos[0] > self.x else -1)
        dy = 0 if self.y == player_pos[1] else (1 if player_pos[1] > self.y else -1)

        # Prefer horizontal or vertical movement (not diagonal)
        if abs(self.x - player_pos[0]) > abs(self.y - player_pos[1]):
            return (dx, 0)
        else:
            return (0, dy)

    def _random_move(self) -> Tuple[int, int]:
        """Move randomly"""
        import random
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
        return random.choice(moves)


class Item(Entity):
    """Item entity"""
    def __init__(self, x: int, y: int, item_type: str):
        super().__init__(x, y, c.ENTITY_ITEM)
        self.item_type = item_type

    def get_name(self) -> str:
        """Get item display name"""
        names = {
            c.ITEM_HEALTH_POTION: "Health Potion",
            c.ITEM_SWORD: "Sword",
            c.ITEM_SHIELD: "Shield",
        }
        return names.get(self.item_type, "Unknown Item")
