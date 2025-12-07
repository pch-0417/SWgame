import pygame
import firebase_admin
from firebase_admin import credentials, storage
import io  
import database

class Character(pygame.sprite.Sprite):

  def __init__ (self, name, color, x, y, hp, skills = None):

    # 부모 클래스 받아오기
    super().__init__()

    # 이미지 처리
    self.name = name
    self.image = pygame.Surface((50, 50))
    self.image.fill(color)
    self.rect = self.image.get_rect()

    # 데이터 처리 
    self.max_hp = hp
    self.current_hp = hp
    if skills:
      self.skills = skills 
    else:
      self.skills = [None] * 4

  # 스킬 추가 함수
  def set_skills(self, new_skills):
        for i in range(min(len(new_skills), 4)):
            self.skills[i] = new_skills[i]
  
  def get_skill(self, slot_index):
        # [수정 4] 인덱스 범위 수정 (0, 1, 2, 3 이니까 < 4)
        if 0 <= slot_index < 4:
            return self.skills[slot_index]
        else:
            print("잘못된 스킬 슬롯입니다.")
            return None

  def take_damage(self, amount):
    self.current_hp -= amount
    print(f"으악! {self.name}가 {amount} 데미지를 입었습니다. (남은 체력: {self.hp})")
     
  def attack(self, target, slot_index):

    skill = self.get_skill(slot_index)

    if skill is None:
      print(f"{self.name}의 {slot_index}번 슬롯이 비어있습니다!")
      return
    damage_amount = skill.get('damage', 0) # 없으면 0
    target.take_damage(damage_amount)
    
    

