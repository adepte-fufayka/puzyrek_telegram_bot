import datetime
class UserProfile:
    user_id: int
    nickname: str
    fraction_emoji: str
    fraction_name: str
    gang_name: str
    max_hp: int
    damage: int
    armor: int
    strength: int
    accuracy: int
    charisma: int
    dexterity: int
    max_energy: int
    zen: int
    updated_at: datetime.datetime

    def __init__(self, user_id, nickname, fraction_emoji, fraction_name, gang_name, max_hp, damage, armor, strength,accuracy, charisma, dexterity, max_energy, zen, updated_at):
        self.dexterity = dexterity
        self.charisma = charisma
        self.accuracy = accuracy
        self.user_id = user_id
        self.nickname = nickname
        self.fraction_emoji = fraction_emoji
        self.fraction_name = fraction_name
        self.gang_name = gang_name
        self.max_hp = max_hp
        self.damage = damage
        self.armor = armor
        self.strength = strength
        self.max_energy = max_energy
        self.zen = zen
        self.updated_at = updated_at

    def bm(self):
        return self.max_hp+self.strength+self.accuracy+self.dexterity+self.charisma
    def __str__(self):
        return """{}{} 🏵{}
🤟{}

🎓{}
❤️{} 🔋{}
⚔️{} 🛡{}
💪{} 🤸🏽‍♂️{}
🎯{} 🗣{}

📟{}""".format(self.fraction_emoji, self.nickname, self.zen, self.gang_name, self.bm(),self.max_hp,self.max_energy, self.damage, self.armor, self.strength,self.dexterity, self.accuracy, self.charisma, self.updated_at)


