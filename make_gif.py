import os
from PIL import Image

# 出来上がるファイル名
OUTPUT_NAME = 'animation_clear_v2.gif'
# 画像の切り替えスピード（200ミリ秒 = 0.2秒）
SPEED = 200
# 【新設定】白さの許容範囲（0〜255）。数字が大きいほど、白に近いグレーも透明になります。
# まずは 30 くらいで試してみてください。
THRESHOLD = 30

def create_gif():
    # プログラムがあるフォルダの場所を自動で特定する
    base_dir = os.path.dirname(__file__)
    
    # 画像を取得して名前順に並べる
    valid_extensions = ('.png', '.jpg', '.jpeg')
    # 出力ファイル名が変わるので、前回のファイルも除外リストに入れます
    exclude_files = (OUTPUT_NAME, 'animation_clear.gif')
    files = sorted([f for f in os.listdir(base_dir) if f.lower().endswith(valid_extensions) and f not in exclude_files])
    
    frames = []
    print(f"以下の画像を処理します: {files}")

    for f in files:
        img_path = os.path.join(base_dir, f)
        img = Image.open(img_path)
        
        # リサイズとRGBA変換
        img = img.resize((400, 400))
        img = img.convert('RGBA')
        
        # 【改良点】白に近い色をまとめて透明にする処理
        datas = img.getdata()
        new_data = []
        for item in datas:
            # R, G, B のすべての値が「255 - THRESHOLD」より大きければ透明にする
            # 例: THRESHOLDが30なら、RGBがすべて225以上の明るい色を透明化
            if item[0] > (255 - THRESHOLD) and item[1] > (255 - THRESHOLD) and item[2] > (255 - THRESHOLD):
                new_data.append((255, 255, 255, 0)) # 透明
            else:
                new_data.append(item) # そのまま
        
        img.putdata(new_data)
        frames.append(img)

    if frames:
        output_path = os.path.join(base_dir, OUTPUT_NAME)
        # 透過GIFを書き出す設定
        frames[0].save(
            output_path,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=SPEED,
            loop=0,
            disposal=2,
            transparency=0
        )
        print(f"🎉【成功】改良版の透過GIF {output_path} が作成されました！")
        print(f"現在の閾値は {THRESHOLD} です。まだ白が残る場合は数字を大きくしてみてください。")
    else:
        print(f"❌【エラー】画像が見つかりませんでした。場所：{base_dir}")

if __name__ == "__main__":
    create_gif()