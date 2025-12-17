import pygame as pg
import settings as set
from character import Monster, BattleManager
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time





def main():
  cred = credentials.Certificate("swgame.json")

  if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

  db = firestore.client()
  pg.init()

  screen = pg.display.set_mode((set.Screen_Width, set.Screen_Heigth))
  pg.display.set_caption("Woosong Sw gmae v 1.0 ")  
  clock = pg.time.Clock()
  font = pg.font.SysFont('malgungothic', 20)
  screen.fill((255, 255, 255))
  loading_text = font.render("클라우드에서 데이터를 불러오는 중...", True, (0,0,0))
  screen.blit(loading_text, (250, 280))
  pg.display.flip()

  all_skills_data = {}

  skills_ref = db.collection('skills')
  for doc in skills_ref.stream():
    all_skills_data[doc.id] = doc.to_dict()
        
  
  all_monsters_data = {}

  monsters_ref = db.collection('monsters')
  for doc in monsters_ref.stream():
    all_monsters_data[doc.id] = doc.to_dict()

  print("데이터 로딩 완료.")

  if "m_01" not in all_monsters_data or "m_02" not in all_monsters_data:
    print("오류: DB에 'm_01' 또는 'm_02' 문서가 없습니다. 콘솔을 확인해주세요.")
    while True:
      for event in pg.event.get():
        if event.type == pg.QUIT: return

  player = Monster(all_monsters_data["m_01"], all_skills_data)
  enemy = Monster(all_monsters_data["m_02"], all_skills_data)
    
  battle = BattleManager(player, enemy)
  def draw_screen():
    screen.fill((250, 250, 250)) # 초기화
        
    # 플레이어 그리기
    pg.draw.rect(screen, player.color, (100, 300, 150, 150))
    p_name = font.render(player.name, True, (0,0,0))
    p_hp = font.render(f"HP: {player.current_hp} / {player.max_hp}", True, (255, 0, 0))
    screen.blit(p_name, (100, 270))
    screen.blit(p_hp, (100, 460))

    # 적 그리기
    pg.draw.rect(screen, enemy.color, (550, 50, 150, 150))
    e_name = font.render(enemy.name, True, (0,0,0))
    e_hp = font.render(f"HP: {enemy.current_hp} / {enemy.max_hp}", True, (255, 0, 0))
    screen.blit(e_name, (550, 20))
    screen.blit(e_hp, (550, 210))

    #로그 박스 및 텍스트
    pg.draw.rect(screen, (220, 220, 220), (50, 500, 700, 80))
    log_text = font.render(battle.log, True, (0,0,0))
    screen.blit(log_text, (70, 530))

    # 턴 안내 

    if battle.turn == "PLAYER":
      guide_text = font.render("[당신의 턴] 스킬을 입력 해주세요!", True, (0, 0, 255))
      screen.blit(guide_text, (100, 480))
    else:
      guide_text = font.render("[적의 턴] 상대방이 생각 중입니다...", True, (255, 0, 0))
      screen.blit(guide_text, (550, 230))
      

  running = True
  while running:
    
    draw_screen()
    pg.display.flip()
    clock.tick(60)

    for event in pg.event.get():
      if event.type == pg.QUIT:
        running = False
            
      if event.type == pg.KEYDOWN and battle.turn == "PLAYER":
        skill_idx = -1
        if event.key == pg.K_1: skill_idx = 0
        elif event.key == pg.K_2: skill_idx = 1
        elif event.key == pg.K_3: skill_idx = 2
        elif event.key == pg.K_4: skill_idx = 3

        if skill_idx != -1:
          battle.use_skill(player, enemy, skill_idx)
          draw_screen()
          pg.display.flip()
          pg.time.delay(1000)         
          #턴 넘기기
          battle.turn = "ENEMY"

    if battle.turn == "ENEMY" and enemy.is_alive() and player.is_alive():
      battle.use_skill(enemy, player, 0) # 적은 0번 스킬(공격)만 사용한다고 가정
      draw_screen()
      pg.display.flip()
      pg.time.delay(1000)
      battle.turn = "PLAYER"

  pg.quit()
  sys.exit()

if __name__ == "__main__":
  main()