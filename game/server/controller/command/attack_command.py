from game.model.entity.character import Hero
from game.server.controller.command import Command


class AttackCommand(Command):

    def __init__(self, attacker, target, model):
        self.attacker = attacker
        self.target = target
        self.model = model

    def execute(self):
        damage = self.attacker.deal_damage(self.target)
        self.target.accept_damage(damage)

        if self.target.is_destroyed():
            if isinstance(self.attacker, Hero):
                coef = self.target.stats.level / self.attacker.stats.level
                self.attacker.update_experience(self.target.stats.reward * coef)
            self.target.on_destroy(self.model)
