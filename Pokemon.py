from flask import Flask, request, g
from flask import render_template
import csv
import os
import sys

app = Flask(__name__)

app.config.from_object(__name__)

with open('pokemon.csv', encoding="utf-16") as f:
    csv_reader = csv.reader(f)
    reader = list(csv_reader)
    print(reader[4][0], file=sys.stdout)

@app.route('/')
def search():
    global poke_names
    return render_template('textboxes.html')

@app.route('/', methods=['POST'])
def comparison():
    poke1 = str(request.form['text1']).lower()
    poke2 = str(request.form['text2']).lower()

    for i in range(len(reader)):
        if str(reader[i][2]).lower() == poke1:
            num1 = i
        if str(reader[i][2]).lower() == poke2:
            num2 = i

    attack1 = reader[num1][14]
    defense1 = reader[num1][15]
    hp1 = reader[num1][13]
    spattack1 = reader[num1][16]
    spdefense1 = reader[num1][17]
    speed1 = reader[num1][18]
    type11 = reader[num1][4]
    type12 = reader[num1][5]
    total1 = hp1 + attack1 + defense1 + spattack1 + spdefense1 + speed1

    attack2 = reader[num2][14]
    defense2 = reader[num2][15]
    hp2 = reader[num2][13]
    spattack2 = reader[num2][16]
    spdefense2 = reader[num2][17]
    speed2 = reader[num2][18]
    type21 = reader[num2][4]
    type22 = reader[num2][5]
    total2 = hp2 + attack2 + defense2 + spattack2 + spdefense2 + speed2

    return render_template('display.html', pokemon1 = poke1, pokemon2 = poke2, attack1 = attack1, attack2 = attack2, total1 = total1, total2 = total2, defense1 = defense1, defense2 = defense2, hp1 = hp1, hp2 = hp2, spattack1 = spattack1, spattack2 = spattack2, spdefense1 = spdefense1, spdefense2 = spdefense2, speed1 = speed1, speed2 = speed2, type11 = type11, type12 = type12, type21 = type21, type22 = type22)




#Keep this at end of code
if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host="0.0.0.0", port=port)
