import pygame
import sys

# Pygame の初期化
pygame.init()

# 画面の設定
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Multi-Font Example")

# フォントの読み込み
hiragana_font_path = "ll/font/msmincho001.ttf"
hangul_font_path = "ll/font/ChosunGs.TTF"
font_size = 48

hiragana_font = pygame.font.Font(hiragana_font_path, font_size)
hangul_font = pygame.font.Font(hangul_font_path, font_size)

# テキストを定義
text = "こんにちは 안녕하세요"

# 文字に応じてフォントを切り替えて描画
def render_text(surface, text, pos):
    x, y = pos
    for char in text:
        if 'ぁ' <= char <= 'ん':  # 平仮名の範囲
            font = hiragana_font
        elif '가' <= char <= '힣':  # ハングルの範囲
            font = hangul_font
        else:
            font = hiragana_font  # デフォルトのフォント

        char_surface = font.render(char, True, (255, 255, 255))
        surface.blit(char_surface, (x, y))
        x += char_surface.get_width()

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 背景を黒色に塗りつぶす
    screen.fill((0, 0, 0))

    # テキストを画面に描画
    render_text(screen, text, (100, 100))

    # 画面更新
    pygame.display.flip()

# Pygame の終了
pygame.quit()
sys.exit()
