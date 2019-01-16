from flask import Flask, request, render_template
import urllib

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shapereader

from io import BytesIO

import pandas as pd
import math

app = Flask(__name__)

#csvデータ読み込み
df = pd.read_csv("data.csv", index_col = 0, header = [0,1,2])
#国名を揃える
df.rename(index={"Bahamas":"The Bahamas"}, inplace=True)
df.rename(index={"Bolivia (Plurinational State of)":"Bolivia"}, inplace=True)
df.rename(index={"Brunei Darussalam":"Brunei"}, inplace=True)
df.rename(index={"Congo":"Republic of the Congo"}, inplace=True)
df.rename(index={"Côte d'Ivoire":"Ivory Coast"}, inplace=True)
df.rename(index={"Democratic People's Republic of Korea":"North Korea"}, inplace=True)
df.rename(index={"Eswatini":"eSwatini"}, inplace=True)
df.rename(index={"Iran (Islamic Republic of)":"Iran"}, inplace=True)
df.rename(index={"Lao People's Democratic Republic":"Laos"}, inplace=True)
df.rename(index={"Republic of Korea":"South Korea"}, inplace=True)
df.rename(index={"Republic of Moldova":"Moldova"}, inplace=True)
df.rename(index={"Russian Federation":"Russia"}, inplace=True)
df.rename(index={"Serbia":"Republic of Serbia"}, inplace=True)
df.rename(index={"Syrian Arab Republic":"Syria"}, inplace=True)
df.rename(index={"The former Yugoslav republic of Macedonia":"Macedonia"}, inplace=True)
df.rename(index={"Timor-Leste":"East Timor"}, inplace=True)
df.rename(index={"United Kingdom of Great Britain and Northern Ireland":"United Kingdom"}, inplace=True)
df.rename(index={"Venezuela (Bolivarian Republic of)":"Venezuela"}, inplace=True)
df.rename(index={"Viet Nam":"Vietnam"}, inplace=True)

#地図データ読み込み
shpfilename = shapereader.natural_earth(resolution="110m", category="cultural", name="admin_0_countries")
reader = shapereader.Reader(shpfilename)

#csvデータと地図データを結合してDataFrameを作成
geometries=[]
countries=[]
for country in reader.records():
    geometries.append(country.geometry)
    countries.append(country.attributes["SOVEREIGNT"])

s=pd.Series(geometries, index=countries, name='geometry')
counter = len(s)

df2 = pd.concat([s, df], axis=1, join_axes=[s.index])

#Figure, Subplot生成
ax = plt.axes(projection=ccrs.PlateCarree())

#カラーマップ
cmap = plt.cm.Blues
sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(100,0))
sm._A = []
cax = plt.colorbar(sm)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/plot/map")
def plot_map():
    #Obtain query parameters
    year = request.args.get("year", type=str)
    level = request.args.get("level", type=str)
    area = request.args.get("area", type=str)

    #国のパッチで埋める(データ無しは灰色)
    for i in range(counter):
        geometry = df2.iloc[i]["geometry"]
        rate = df2.iloc[i][year, level, area]
        if pd.isnull(rate):
            color="gray"
        else:
            color = cmap(rate/100)
        ax.add_geometries(geometry, ccrs.PlateCarree(), edgecolor="black", linestyle=":", facecolor=color)

    #カラーバーのサイズ調整
    plt.savefig(BytesIO())
    ax_pos=ax.get_position()
    cax_pos0=cax.ax.get_position()
    cax_pos1=[cax_pos0.x0, ax_pos.y0, cax_pos0.x1-cax_pos0.x0, ax_pos.y1-ax_pos.y0]
    cax.ax.set_position(cax_pos1)

    #画像データを返す
    png_out = BytesIO()
    plt.savefig(png_out, format="png", bbox_inches="tight")
    img_data = urllib.parse.quote(png_out.getvalue())
    return "data:image/png:base64," + img_data

if __name__ == "__main__":
    app.run(debug=True, port=5000)
