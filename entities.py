"""
Entity classes for Dungeon Delver
"""
from typing import Tuple, List
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
    def __init__(self, x: int, y: int, class_type: str = c.CLASS_WARRIOR):
        super().__init__(x, y, c.ENTITY_PLAYER)
        self.class_type = class_type

        # Set class-specific stats
        stats = c.CLASS_STATS[class_type]
        self.max_hp = stats["hp"]
        self.hp = self.max_hp
        self.base_attack = stats["attack"]
        self.base_defense = stats["defense"]

        # Class-specific attributes
        self.crit_chance = stats.get("crit_chance", 0.0)  # Rogue has crit chance
        self.dodge_chance = 0.15 if class_type == c.CLASS_ROGUE else 0.0  # Rogue can dodge

        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 50
        self.inventory = []

        # Equipment slots
        self.equipment = {
            c.SLOT_WEAPON: None,
            c.SLOT_ARMOR: None,
            c.SLOT_ACCESSORY: None,
            c.SLOT_BOOTS: None,
        }

        # Abilities - will be set by game after creation
        self.abilities: List = []

    @property
    def attack(self) -> int:
        """Total attack including bonuses from equipment"""
        bonus = 0
        # Get bonus from weapon
        if self.equipment[c.SLOT_WEAPON]:
            bonus += self.equipment[c.SLOT_WEAPON].get_stat_bonus("attack")
        # Get bonus from accessories
        if self.equipment[c.SLOT_ACCESSORY]:
            bonus += self.equipment[c.SLOT_ACCESSORY].get_stat_bonus("attack")
        return self.base_attack + bonus

    @property
    def defense(self) -> int:
        """Total defense including bonuses from equipment"""
        bonus = 0
        # Get bonus from armor
        if self.equipment[c.SLOT_ARMOR]:
            bonus += self.equipment[c.SLOT_ARMOR].get_stat_bonus("defense")
        # Get bonus from boots
        if self.equipment[c.SLOT_BOOTS]:
            bonus += self.equipment[c.SLOT_BOOTS].get_stat_bonus("defense")
        # Get bonus from accessories
        if self.equipment[c.SLOT_ACCESSORY]:
            bonus += self.equipment[c.SLOT_ACCESSORY].get_stat_bonus("defense")
        return self.base_defense + bonus

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
        # Consumables are used immediately
        if item.item_type == c.ITEM_HEALTH_POTION:
            self.heal(c.ITEM_EFFECTS[c.ITEM_HEALTH_POTION]["heal"])
            return  # Don't add to inventory

        # Equipment is automatically equipped
        if item.item_type in c.EQUIPMENT_TYPES:
            slot = c.EQUIPMENT_TYPES[item.item_type]
            # Unequip old item if exists
            if self.equipment[slot]:
                self.inventory.append(self.equipment[slot])
            # Equip new item
            self.equipment[slot] = item
        else:
            # Add to inventory
            self.inventory.append(item)

    def equip_item(self, item: 'Item') -> bool:
        """Equip an item from inventory. Returns True if successful"""
        if item not in self.inventory:
            return False

        if item.item_type not in c.EQUIPMENT_TYPES:
            return False

        slot = c.EQUIPMENT_TYPES[item.item_type]

        # Unequip old item
        if self.equipment[slot]:
            self.inventory.append(self.equipment[slot])

        # Equip new item
        self.inventory.remove(item)
        self.equipment[slot] = item
        return True

    def get_class_name(self) -> str:
        """Get display name for class"""
        names = {
            c.CLASS_WARRIOR: "Warrior",
            c.CLASS_MAGE: "Mage",
            c.CLASS_ROGUE: "Rogue",
            c.CLASS_RANGER: "Ranger",
        }
        return names.get(self.class_type, "Unknown")


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

        # Status effects
        self.frozen_turns = 0

    def take_damage(self, damage: int) -> bool:
        """Take damage, return True if still alive"""
        self.hp = max(0, self.hp - damage)
        return self.hp > 0

    def get_ai_action(self, player_pos: Tuple[int, int], dungeon_map) -> Tuple[int, int]:
        """Determine next move based on AI type"""
        # Check if frozen
        if self.frozen_turns > 0:
            return (0, 0)  # Can't move when frozen

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

    def reduce_status_effects(self):
        """Reduce duration of status effects"""
        if self.frozen_turns > 0:
            self.frozen_turns -= 1


class Item(Entity):
    """Item entity"""
    def __init__(self, x: int, y: int, item_type: str, rarity: str = "common", affixes: dict = None):
        super().__init__(x, y, c.ENTITY_ITEM)
        self.item_type = item_type
        self.rarity = rarity  # common, uncommon, rare, epic, legendary
        self.affixes = affixes or {}  # Additional stat modifiers

    def get_stat_bonus(self, stat_name: str) -> int:
        """Get bonus for a specific stat"""
        # Base bonus from item effects
        base_bonus = c.ITEM_EFFECTS.get(self.item_type, {}).get(stat_name, 0)

        # Additional bonus from affixes
        affix_bonus = self.affixes.get(stat_name, 0)

        # Rarity multiplier
        rarity_mult = {
            "common": 1.0,
            "uncommon": 1.2,
            "rare": 1.5,
            "epic": 2.0,
            "legendary": 3.0,
        }.get(self.rarity, 1.0)

        return int((base_bonus + affix_bonus) * rarity_mult)

    def get_name(self) -> str:
        """Get item display name"""
        base_names = {
            c.ITEM_HEALTH_POTION: "Health Potion",
            c.ITEM_SWORD: "Sword",
            c.ITEM_SHIELD: "Shield",
            c.ITEM_BOOTS: "Boots",
            c.ITEM_RING: "Ring",
        }
        base_name = base_names.get(self.item_type, "Unknown Item")

        # Add rarity prefix for non-common items
        if self.rarity != "common":
            rarity_name = self.rarity.capitalize()
            base_name = f"{rarity_name} {base_name}"

        return base_name
