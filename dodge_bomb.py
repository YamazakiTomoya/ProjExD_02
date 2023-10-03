import random
import sys
import pygame as pg

WIDTH, HEIGHT = 1600, 900
data = { #練習3:移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5,0)
}

def check_bound(obj_rct: pg.Rect):
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果、ｋ縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: #横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: #縦方向判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    
    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400) #練習3：こうかとんの初期座標を設定する
    
    """ばくだん"""
    accs = [a for a in range(1, 11)]
    bd_imgs = []
    for r in range(1, 11):
        bd_img = pg.Surface((20*r, 20*r)) #練習1：爆弾Surfaceを作成する
        pg.draw.circle(bd_img, (255, 0, 0), (10*r, 10*r), 10*r) 
        bd_imgs.append(bd_img)
    vx, vy = +5, +5 #練習2：爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
    bd_img = bd_imgs[min(tmr//500, 9)]
    bd_img.set_colorkey((0, 0, 0)) #練習1：黒い部分を透明にする
    bd_rct = bd_img.get_rect() #練習1：SurfaceからRectを抽出する
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bd_rct.center = (x, y) #練習1：Rectにランダムな座標を設定する。
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bd_rct): #練習5：ぶつかってたら
            print("ゲームオーバー")
            return

        screen.blit(bg_img, [0, 0])
        
        """こうかとん"""
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in data.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #練習3：横方向の合計移動量
                sum_mv[1] += mv[1] #練習3：縦方向の合計移動量
            
        kk_rct.move_ip(sum_mv[0], sum_mv[1]) #練習3：移動させる
        if check_bound(kk_rct) != (True, True): #練習4：はみ出し判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct) #練習3：移動後の座標に表示させる
        """ばくだん"""
        bd_rct.move_ip(avx, avy) #練習2：横方向にはみ出たら
        yoko, tate = check_bound(bd_rct)
        if not yoko: #練習4：横方向にはみ出たら
            avx *= -1
        if not tate: #練習4：縦方向にはみ出たら
            avy *= -1

        screen.blit(bd_img, bd_rct) #練習1：Rectを使って試しにblit
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()