from flask import Flask, request, g
from flask import render_template
import csv

app = Flask(__name__)

app.config.from_object(__name__)

with open('pokemon.csv') as f:
    csv_reader = csv.reader(f)
    reader = list(csv_reader)

@app.route('/')
def search():
    global poke_names
    return render_template('textboxes.html')

@app.route('/', methods=['POST'])
def comparison():
    poke1 = str(request.form['text1']).lower()
    poke2 = str(request.form['text2']).lower()

    for i in range(len(reader)):
        if str(reader[i][4]).lower() == poke1:
            num1 = i
        if str(reader[i][4]).lower() == poke2:
            num2 = i

    attack1 = reader[num1][0]
    total1 = reader[num1][1]
    defense1 = reader[num1][2]
    hp1 = reader[num1][3]
    spattack1 = reader[num1][5]
    spdefense1 = reader[num1][6]
    speed1 = reader[num1][7]
    type11 = reader[num1][8]
    type12 = reader[num1][9]

    attack2 = reader[num2][0]
    total2 = reader[num2][1]
    defense2 = reader[num2][2]
    hp2 = reader[num2][3]
    spattack2 = reader[num2][5]
    spdefense2 = reader[num2][6]
    speed2 = reader[num2][7]
    type21 = reader[num2][8]
    type22 = reader[num2][9]

    return render_template('display.html', pokemon1 = poke1, pokemon2 = poke2, attack1 = attack1, attack2 = attack2, total1 = total1, total2 = total2, defense1 = defense1, defense2 = defense2, hp1 = hp1, hp2 = hp2, spattack1 = spattack1, spattack2 = spattack2, spdefense1 = spdefense1, spdefense2 = spdefense2, speed1 = speed1, speed2 = speed2, type11 = type11, type12 = type12, type21 = type21, type22 = type22)































#Keep this at end of code
if __name__ == '__main__':
 app.run(debug=True)
