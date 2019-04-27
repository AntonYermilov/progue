from game.controller.command import Command


class AttackCommand(Command):

    def __init__(self, attacker, target, model):
        self.attacker = attacker
        self.target = target
        self.model = model

    def execute(self):
        damage = self.attacker.attack_damage_for_target(self.target)
        self.target.deal_damage(damage)

        if self.target.is_destroyed():
            self.target.on_destroy(self.model)
