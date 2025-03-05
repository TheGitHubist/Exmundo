from abc import ABC, abstractmethod

class CardModel(ABC):
    def __init__(self, name, image, effects):
        self.name = name
        self.image = image
        self.effects = effects

    @abstractmethod
    def activate(self):
        pass

    def activate_effects(self, target):
        for effect in self.effects:
            effect.activate(self)

class MonsterCardModel(CardModel):
    def __init__(self, name, image, health, damage, effects):
        super().__init__(name, image, effects)
        self.name = name
        self.health = health
        self.damage = damage
        self.effects = effects

    @abstractmethod
    def attack(self, other):
        pass

    def gain_health(self, amount):
        self.health += amount

    def lose_health(self, amount):
        self.health -= amount

    def activate_effects(self):
        for effect in self.effects:
            effect.activate(self)

    def move(self):
        pass

class BasicMonsterCard(MonsterCardModel):
    def __init__(self, name, image, health, damage, effects, rune_possession):
        super().__init__(name, image, health, damage, effects)
        self.rune_possession = rune_possession

    def attack(self, other):
        other.lose_health(self.damage)

class EliteMonsterCard(MonsterCardModel):
    def __init__(self, name, image, health, damage, effects, rune_possession, rune_cost):
        super().__init__(name, image, health, damage, effects)
        self.rune_possession = rune_possession
        self.rune_cost = rune_cost
        
    def attack(self, other):
        other.lose_health(self.damage)

class BossMonsterCard(MonsterCardModel):
    def __init__(self, name, image, health, damage, effects, rune_possession, rune_cost):
        super().__init__(name, image, health, damage, effects)
        self.rune_possession = rune_possession
        self.rune_cost = rune_cost
        
    def attack(self, other):
        other.lose_health(self.damage)

class SpellCardModel(CardModel):
    def __init__(self, name, image, effects):
        super().__init__(name, image, effects)
        self.name = name
        self.effects = effects
    
    @abstractmethod
    def activate(self):
        pass

    def activate_effects(self, target):
        for effect in self.effects:
            effect.activate(self)

class LinkSpellCard(SpellCardModel):
    def __init__(self, name, image, effects, position, pointed_zones):
        super().__init__(name, image, effects)
        self.position = position
        self.pointed_zones = pointed_zones

    def activate(self):
        for cards in self.pointed_zones:
            self.activate_effects(cards)

class AuraSpellCard(SpellCardModel):
    def __init__(self, name, image, effects, position):
        super().__init__(name, image, effects)
        self.position = position

    def activate(self):
        self.activate_effects()

class FieldSpellCard(SpellCardModel):
    def __init__(self, name, image, effects, field):
        super().__init__(name, image, effects)
        self.field = field

    def activate(self):
        for cards in self.field:
            self.activate_effects(cards)

class NormalSpellCard(SpellCardModel):
    def __init__(self, name, image, effects):
        super().__init__(name, image, effects)

    def activate(self):
        self.activate_effects()