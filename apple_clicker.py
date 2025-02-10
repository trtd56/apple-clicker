import pyxel
import random

class AppleGame:
    def __init__(self):
        self.width = 160
        self.height = 120

        # Pyxelの初期化
        pyxel.init(self.width, self.height, title="Apple Clicker")

        # apple.pyxres をロード
        pyxel.load("apple.pyxres")

        # スコアやりんごの座標などの初期化
        self.score = 0
        self.game_over = False  # ゲームオーバーフラグ
        self.reset_apple()

        # メインループ開始
        pyxel.run(self.update, self.draw)

    def reset_apple(self):
        """
        りんごの状態をリセットし、新しいりんごの位置をランダム配置する
        """
        # りんごの中心座標をランダムで決める (半径8～10px程度と想定)
        self.apple_x = random.randint(8, self.width - 8)
        self.apple_y = random.randint(8, self.height - 8)

        # りんごが食べられたかどうか
        self.is_eaten = False
        # 食べられりんご表示用タイマー (例: 15フレーム)
        self.eaten_timer = 0

    def update(self):
        """
        毎フレーム呼び出される更新処理
        """
        # ゲームオーバーになっていたら操作を受け付けない
        if self.game_over:
            # ゲームオーバー画面の時に何か操作したい場合はここに処理を書く
            # 例: ボタンを押したら終了 or リセット
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            return

        # スコアが10になったらゲームオーバー
        if self.score >= 10:
            self.game_over = True
            return

        # 左クリック判定
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            # (mx, my) と (self.apple_x, self.apple_y) の距離が半径8以内かどうかで当たり判定
            if (mx - self.apple_x)**2 + (my - self.apple_y)**2 <= 8**2:
                self.score += 1
                self.is_eaten = True
                self.eaten_timer = 15

        # 食べられ状態が続く間はカウントダウンし、0になったら次のりんごへ
        if self.is_eaten:
            self.eaten_timer -= 1
            if self.eaten_timer <= 0:
                self.reset_apple()

    def draw(self):
        """
        毎フレーム呼び出される描画処理
        """
        # 背景クリア (0番色で塗り潰し)
        pyxel.cls(0)

        if self.game_over:
            # ゲームオーバー画面
            pyxel.text(60, 50, "Clear!!!", 7)
            pyxel.text(40, 70, "Press Q to Quit", 7)
            return

        # スコア表示
        pyxel.text(5, 5, f"Score: {self.score}", 7)

        # りんご描画
        if not self.is_eaten:
            # まだ食べられていない → 丸いりんご
            # pyxel.blt(x, y, img_bank, u, v, w, h, [colkey])
            pyxel.blt(self.apple_x - 8, self.apple_y - 8,
                      0,    # 画像バンク(0)  
                      0, 0, # 画像上の切り出し座標 (左上が (0,0)) 
                      16, 16, # 幅, 高さ
                      scale=2,
                      colkey=0)   # colkey=0 で"0番色"を透明扱い
        else:
            # 食べられたりんご
            pyxel.blt(self.apple_x - 8, self.apple_y - 8,
                      0,    # 画像バンク(0)
                      16, 0,# こちらは (16,0)から16x16 を取り出す想定
                      16, 16,
                      scale=2,
                      colkey=0)

# ゲームを実行
if __name__ == "__main__":
    AppleGame()
