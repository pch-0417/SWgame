import pygame

class Skill: 

  def __init__ (self, name, power):

    self.name = name
    self.power = power

class Character(pygame.sprite.Sprite):

  def __init__ (self, name, color, x, y, hp):

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
    self.skills = [None, None, None, None]

  # 스킬 추가 함수
  def Set_Skill(self, Slot_index, skill):
    if 0 <= Slot_index < 4:
      self.skills[Slot_index] = skill
    else:
      print("스킬 없다고")
    
  def Get_Skill(self, Slot_index):
    if 0 <= Slot_index < 3:
      return None

  def attack(self, target, Slot_index):
    Skill = self.Get_Skill(Slot_index)
  
    if Skill is None:
      return f"{self.name}의 스킬이 비어있습니다!"
    self.target = 
    

    
    

