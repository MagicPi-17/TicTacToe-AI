from AI_Functions import AIEngine, ConvertToPath, check_game
from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdj32t3ah k43jshkjddsfghjs'


@app.route('/', methods=['POST', 'GET'])
def home():
    engine = AIEngine()

    if session.get('UserStartSession') is None:
        session['Game'] = [''] * 9
        session['PlayerSym'] = 0
        session['IsWin'] = None
        session['Last_Call'] = None
        session['UserStartSession'] = True
        session['IsStarted'] = False

    Game = session.get('Game')
    # turn = session.get('turn')
    PlayerSym = session.get('PlayerSym')
    IsWin = session.get('IsWin')
    Last_Call = session.get('Last_Call')
    IsStarted = session.get('IsStarted')


    if request.method == 'POST':

        if Last_Call != request.form:

            if request.form.get('X') == 'X':
                IsStarted = True
                PlayerSym = 1
                IsWin = None
                Game = [''] * 9

            elif request.form.get('O') == 'O':
                IsStarted = True
                PlayerSym = -1
                IsWin = None
                Game = [''] * 9
                AI_Choice = random.choice(range(9))
                Game[AI_Choice] = 'X'


            elif request.form.get('restart') == 'restart':
                IsStarted = False
                PlayerSym = 0
                Game = [''] * 9
                IsWin = None

            for i in range(9):
                IndexData = request.form.get(f'index {i}')
                if IndexData is not None:
                    if Game[int(i)] == '' and IsStarted:
                        if PlayerSym == 1:
                            Game[int(i)] = 'X'
                            if check_game(ConvertToPath(Game)):
                                IsWin = 'X Wins'
                                IsStarted = False
                                break
                            elif Game.count('') == 0:
                                IsWin = 'Draw'
                                IsStarted = False
                                break

                            AI_Choice = engine.Best(ConvertToPath(Game))
                            Game[AI_Choice] = 'O'

                            if check_game(ConvertToPath(Game)):
                                IsWin = 'O Wins'
                                IsStarted = False
                                break

                        elif PlayerSym == -1:
                            Game[int(i)] = 'O'
                            if check_game(ConvertToPath(Game)):
                                IsWin = 'O Wins'
                                IsStarted = False
                                break

                            AI_Choice = engine.Best(ConvertToPath(Game))
                            Game[AI_Choice] = 'X'

                            if check_game(ConvertToPath(Game)):
                                IsWin = 'X Wins'
                                IsStarted = False
                                break
                            elif Game.count('') == 0:
                                IsWin = 'Draw'
                                IsStarted = False
                                break

                        break

        Last_Call = request.form

    session['Game'] = Game
    session['PlayerSym'] = PlayerSym
    session['IsWin'] = IsWin
    session['Last_Call'] = Last_Call
    session['IsStarted'] = IsStarted

    return render_template('index.html', data=session.get('Game'), StartGame=IsStarted, IsWin=IsWin)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
