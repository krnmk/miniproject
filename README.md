## プログラムの内容
- 飲用可能な水を利用できる人口割合を[このデータ](http://apps.who.int/gho/data/node.main.WSHWATER?lang=en)からカラーマップにしました。割合の大小は青の濃淡で、データがない場合はグレーで描画されるようにしました。ブラウザから西暦(2000~2015)、水準(最低限飲める水/安全に管理された飲用水)、地域　(全体/都市/田舎)を選択できるように設定しました。

## 工夫したところ
- 人口割合のデータと地図データの国名表記にブレがあったので、jupyter notebook上で検出を実行し、見つかった国名をapp.py内で揃えました。<br>
    **地図データのみに存在する国名を検出するのに用いたプログラム**
```
i = 0
for country1 in reader.records():
    for country2 in df.index:
        if country1.attributes["SOVEREIGNT"] == country2:
            break
    else:
        i+=1
        print(country1.attributes["SOVEREIGNT"])
print(i)
```
   **人口割合データのみに存在する国名を検出するのに用いたプログラム**
```
i = 0
for country1 in df.index:
    for country2 in reader.records():
        if country2.attributes["SOVEREIGNT"] == country1:
            break
    else:
        i+=1
        print(country1)
print(i)
```
- 描画時間が長く、現在表示されている地図が変更前なのか変更後なのか分かりにくかったため、処理中は「描画中...」と表示されるようにしました。
- カラーバーのサイズが地図に揃うように調整しました。

## 苦労した点
- データフレームの操作にてこずりました。地図データはFranceのデータが３つあるなど、国名指定の処理が難しいことに気づくまでエラーばかりで苦労しました。
- 最初plot.jsで「描画中...」の表示を終了するプログラムを書こうとした際、
```
$.get("/plot/map" + "?" + query, function(data) {
    document.getElementById("plotimg").src = data;
});
document.getElementById("waittxt").textContent = ""; 
```    
   と書いたら表示が確認できないくらい一瞬で消え、どうすれば処理中に表示が続くかしばらく悩みました。
```
$.get("/plot/map" + "?" + query, function(data) {
    document.getElementById("plotimg").src = data;
    document.getElementById("waittxt").textContent = ""; 
});
```
   このように位置を変えたら思った通りの動きをするようになりました。

## やりたりなかったこと
- 地図が拡大可能で緯度経度の変更が可能だとサービスとしてより優秀だったと思います。
- 描画速度を速くしたかったです。描画の際に二重ループにしていたのを一重で済ませれば速くなるかと思い、人口割合のデータと地図のジオメトリデータを一つのデータフレームにしてみましたが、描画速度は変わりませんでした。<br>
    **変更前のループ**　(dfは人口割合データのみのデータフレーム)
```
#国のパッチで埋める(データなしは灰色)
for country1 in reader.records():
    geometry = country1.geometry
    for country2 in df.index:
        rate = df[year, level, area][country2]
        if pd.notnull(rate) and country1.attributes["SOVEREIGNT"] == country2:
            color = cmap(rate/100)
            break
    else:
        color="gray"
    ax.add_geometries(geometry, ccrs.PlateCarree(), edgecolor="black", linestyle=":", facecolor=color)
```
   **変更後のループ**　(df2はindexを地図データの国名に合わせて人口割合データとジオメトリデータを結合したデータフレーム)
```
#国のパッチで埋める(データ無しは灰色)
for i in range(counter):
    geometry = df2.iloc[i]["geometry"]
    rate = df2.iloc[i][year, level, area]
    if pd.isnull(rate):
        color="gray"
    else:
        color = cmap(rate/100)
    ax.add_geometries(geometry, ccrs.PlateCarree(), edgecolor="black", linestyle=":", facecolor=color)
```

## コメント
- 描画速度を速めることはできませんでしたが、自分で想定した最低限の機能は入れられたので概ね満足です。「描画中...」の表示を追加できたのが一番良かったと思います。
