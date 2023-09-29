from flask import Flask, jsonify, render_template, request, jsonify, url_for, flash, abort, redirect
import os
import requests
import random
import pandas as pd


HEADERS = {
    "Authorization": f"Bearer {os.environ.get('api-key')}"
}
BASE_URL = "https://the-one-api.dev/v2/"
CHARACTER = None
CORRECT = False
QUOTE_REQUEST = requests.get(url=BASE_URL + "quote", headers=HEADERS)
ALL_CHARACTERS_REQUEST = requests.get(url=BASE_URL + "character/", headers=HEADERS)
print(ALL_CHARACTERS_REQUEST)
data_frame = pd.DataFrame(QUOTE_REQUEST.json()["docs"])
data_frame_2 = pd.DataFrame(ALL_CHARACTERS_REQUEST.json()["docs"])
data_frame_2 = data_frame_2[["_id", "name", "race", "gender"]]
data_frame = data_frame.set_index("character")
unique_movie_characters = data_frame.index.unique()
data_frame_4 = pd.DataFrame(unique_movie_characters)
data_frame_4 = data_frame_4.merge(data_frame_2, how="left", left_on="character", right_on="_id")[['_id', 'name', 'race', 'gender']]
UNIQUE_MOVIE_CHARACTER_NAMES_AND_IDS = data_frame_4.set_index("_id").transpose().to_dict()



app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home_page():
    global CHARACTER
    global QUOTE_REQUEST
    global UNIQUE_MOVIE_CHARACTER_NAMES_AND_IDS
    if request.method == "GET":
        quote = random.choice(QUOTE_REQUEST.json()["docs"])
        character_id = quote["character"]
        CHARACTER = UNIQUE_MOVIE_CHARACTER_NAMES_AND_IDS[character_id]["name"]
        random_characters = random.choices([UNIQUE_MOVIE_CHARACTER_NAMES_AND_IDS[key]["name"] for key in UNIQUE_MOVIE_CHARACTER_NAMES_AND_IDS.keys()], k=4)
        random_characters.append(UNIQUE_MOVIE_CHARACTER_NAMES_AND_IDS[character_id]["name"])
        return render_template("index.html", quote=quote["dialog"], possible_characters=random_characters, question_answered=False)

    elif request.method == "POST":
        # global CHARACTER
        if request.form.get("character") != None:
            global CORRECT
            answer = request.form.get("character")
            if CHARACTER.lower() == answer.lower():
                CORRECT = True
            else:
                CORRECT = False
            return render_template("index.html", question_answered=True, correct=CORRECT)
        else:
            return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.run(debug=True)