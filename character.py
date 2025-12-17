import pygame
import firebase_admin
from firebase_admin import credentials
import settings as set
cred = credentials.Certificate("swgame.json")
firebase_admin.initialize_app(cred)
class Monster:
  def __init__(self, data, skill_data_ref):
    if data is None: 
      print("어류")
      return

    self.name = data.get('name', 'Unknown')
    self.max_hp = data.get('hp', 100)
    self.current_hp = self.max_hp
    self.color = data.get('color', [set.Black])
    self.skills = []
    raw_skills = data.get('skills', [])
    if isinstance(raw_skills, str):
      raw_skills = [raw_skills]

    for skill_id in raw_skills:
      if skill_id in skill_data_ref:
        self.skills.append(skill_data_ref[skill_id])
      else:
        print(f"오류: '{skill_id}'라는 스킬을 찾을 수 없습니다. (DB 확인 필요)")  
            
  def take_damage(self, amount):
    self.current_hp -= amount
    if self.current_hp < 0:
      self.current_hp = 0

  def heal(self, amount):
    self.current_hp += amount
    if self.current_hp > self.max_hp:
      self.current_hp = self.max_hp
    print(f"{self.name}의 체력이 {self.current_hp}/{self.max_hp}로 회복됨.")
    
  def is_alive(self):
        return self.current_hp > 0
  
class BattleManager():
  def __init__(self, player, enemy):
    self.player = player
    self.enemy = enemy
    self.turn = "PLAYER"
    self.log = "Firestore 연동 성공!"    

  def get_matchup_multiplier(self, attacker, defender):
      multiplier = 1.0
      if attacker.id in self.matchup_data:
          if defender.id in self.matchup_data[attacker.id]:
              multiplier = self.matchup_data[attacker.id][defender.id]
      return multiplier

  def use_skill(self, user, target, skill_index):
    if skill_index >= len(user.skills):
            return
    skill = user.skills[skill_index]
    skill_type = skill.get('type', 'ATTACK') # 타입 없으면 기본 공격으로 처리
    power = skill.get('power', 0)
        
    # 1. 공격 스킬
    if skill_type == 'ATTACK':
      target.take_damage(power)
      self.log = f"[{user.name}] {skill['name']} 사용! -> {target.name}에게 {power} 데미지!"
            
    # 2. 회복 스킬 (대상은 무조건 자기 자신)
    elif skill_type == 'HEAL':
      user.heal(power)
      self.log = f"[{user.name}] {skill['name']} 사용! -> 체력 {power} 회복."