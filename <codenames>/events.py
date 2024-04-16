from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import request, render_template, Blueprint, session, redirect, url_for
from game import Room
from room_name_generator.name_generator import generate_room_name

game = Blueprint('game', __name__)

turns = [0]

socketio = SocketIO()

rooms = {}
users = []
user_data = {}

@game.route("/room/<room_name>")
def roomPage(room_name):
    _user_id = session.get('user_id')
    _user_id = f'user_{_user_id}'
    if room_name in rooms:
        if _user_id in rooms[room_name].players:
            return render_template("game.html", room_name=room_name, create=True)
        else:
            return render_template("game.html", room_name=room_name, create=False)

    return redirect(url_for('lounge'))

@socketio.on("connect")
def handle_connection():
    user_id = session.get("user_id")
    user_data[user_id] =  {'room_name': "", 'nickname': "", 'color': ""}
    user_room_name = f'user_{user_id}'
    users.append(user_room_name)
    join_room(user_room_name)
    print("client connected")
    
@socketio.on("create_room")
def create_room(_user_data):
    _user_id = f'user_{session.get("user_id")}'
    _nickname = _user_data['nickname']
        
    new_room_name = generate_room_name()
    rooms[new_room_name] = Room(new_room_name)
    
    current_room = rooms[new_room_name]
    current_room.join_game(_user_id)
    
    join_room(_user_id)
    join_room(new_room_name)
    
    user_data[_user_id] = {'room_name': new_room_name, 'nickname': _nickname, 'color': ""}
    
    emit('redirect', url_for('game.roomPage', room_name=new_room_name), room=[_user_id])



@socketio.on("join_game_room")
def join_game_room(_user_data):
    _room_name = _user_data['room_name']
    _user_id = session.get("user_id")
    _user_id = f'user_{_user_id}'
    _nickname = _user_data['nickname']
        
    user_data[_user_id] = {'room_name': _room_name, 'nickname': _nickname, 'color': ""}
    rooms[_room_name].players.append(_user_id)
    
    join_room(_user_id)
    join_room(_room_name)
    # Get user room
    game_data = get_game_data(_room_name)
    
    
    emit('player_update', { 'game_data': game_data }, to=rooms[_room_name].players)

@socketio.on("start_game")
def start_game(user_data):
    _user_id = session.get("user_id")
    _user_id = f'user_{_user_id}'
    _room_name = user_data['room_name']
    
    # Get user room
    user_room = rooms[_room_name]

    game_neutral_words = user_room.words
    game_spymaster_words = user_room.spymaster_words
    red_spymaster, blue_spymaster, red_operatives, blue_operatives, red_points, blue_points = user_room
    
    neutral_teams = red_operatives + blue_operatives
    if (len(neutral_teams) > 0):
        emit('start_game', { 'words': game_neutral_words, 'red_points': red_points, 'blue_points': blue_points }, to=neutral_teams);
    emit('start_game', { 'words': game_spymaster_words, 'red_points': red_points, 'blue_points': blue_points }, to=[red_spymaster, blue_spymaster]);
    emit('give_clue', to=red_spymaster)

@socketio.on("join_blue_operatives")
def join_blue_operatives(_user_data):
    _user_id = session.get("user_id")
    _user_id = f'user_{_user_id}'
    _room_name = _user_data['room_name']

    # Get room
    current_room = rooms[_room_name]
    
    if (_user_id in current_room.players):
        current_room.join_blue_operatives(_user_id)
    
    user_data[_user_id]['color'] = 'blue'
    user_room = user_data[_user_id]['room_name']
    game_data = get_game_data(user_room)
    
    emit("player_update", { 'game_data': game_data }, to=current_room.players)

@socketio.on("join_blue_spymaster")
def join_blue_spymaster(_user_data):
    _user_id = session.get("user_id")
    _user_id = f'user_{_user_id}'
    _room_name = _user_data['room_name']

    # Get room
    current_room = rooms[_room_name]
    
    if (_user_id in current_room.players):
        current_room.join_blue_spymaster(_user_id)
    
    user_data[_user_id]['color'] = 'blue'
    user_room = user_data[_user_id]['room_name']
    game_data = get_game_data(user_room)
    
    emit("player_update", { 'game_data': game_data }, to=current_room.players)
    
@socketio.on("join_red_operatives")
def join_red_operatives(_user_data):
    _user_id = session.get("user_id")
    _user_id = f'user_{_user_id}'
    _room_name = _user_data['room_name']

    # Get room
    current_room = rooms[_room_name]
    
    if (_user_id in current_room.players):
        current_room.join_red_operatives(_user_id)
    
    user_data[_user_id]['color'] = 'red'
    user_room = user_data[_user_id]['room_name']
    game_data = get_game_data(user_room)
    
    emit("player_update", { 'game_data': game_data }, to=current_room.players)

@socketio.on("join_red_spymaster")
def join_red_spymaster(_user_data):
    _user_id = session.get("user_id")
    _user_id = f'user_{_user_id}'
    _room_name = _user_data['room_name']
    
    # Get room
    current_room = rooms[_room_name]
    if (_user_id in current_room.players):
        current_room.join_red_spymaster(_user_id)
    
    user = user_data[_user_id]
    user['color'] = 'red'
    game_data = get_game_data(_room_name)
    
    emit("player_update", { 'game_data': game_data }, to=current_room.players)

@socketio.on("click_word")
def click_word(action_data):
    _user_id = session.get("user_id")
    _user_id = f'user_{_user_id}'
    _word = action_data['word']
    _room_name = action_data['room_name']

    # Get user room
    user_room = rooms[_room_name]
    user_color = user_data[_user_id]['color']
    user_nickname = user_data[_user_id]['nickname']
    
    print(user_color)
    # Get Word Color
    word_color = user_room.get_color(_word)
    
    if word_color == user_color:
        user_room.give_points(user_color)
        user_room.click_card()
        
        if user_room.allowed_clicks == 0:
            next_turn = user_room.updateTurn()
            id = user_room.get_id(next_turn)
            id = id if id else ['']
            
            print("CLICKED SAME COLOR CARDNEXT_TURN", next_turn)
            emit('end_turn', to=user_room.players)
            if 'spymaster' in next_turn:
                emit('give_clue', to=id)
            elif 'operatives' in next_turn:
                emit('your_turn', to=id)
    else:
        user_room.reset_clicks()
        other_color = 'blue' if user_color == 'red' else 'red'
        
        if word_color == "neutral":
            next_turn = user_room.updateTurn()
            id = user_room.get_id(next_turn)
            id = id if id else ['']
            
            print("CLICKED NEUTRAL CARD NEXT TURN", id, next_turn)
            emit('end_turn', to=user_room.players)
            if 'spymaster' in next_turn:
                emit('give_clue', to=id)
            elif 'operatives' in next_turn:
                emit('your_turn', to=id)
        elif word_color == "black":
            print("CLICKED BLACK CARD END GAME")
            red_points, blue_points = user_room.get_points()
            winner = "red" if red_points == 0 else "blue"
            emit("word_clicked", { 'word': _word, 'color': word_color, 'red_points': red_points, 'blue_points': blue_points, 'user_color': user_color, 'nickname': user_nickname}, to=user_room.players)
            emit('end_game', { 'color': winner }, to=user_room.players)
            return
        else:
            print("CLICKED THE OTHER COLOR CARD")
            user_room.give_points(other_color)
            next_turn = user_room.updateTurn()
            id = user_room.get_id(next_turn)
            id = id if id else ['']
            print("NEXT TURN", id, next_turn)
            
            emit('end_turn', to=user_room.players)
            if 'spymaster' in next_turn:
                emit('give_clue', to=id)
            elif 'operatives' in next_turn:
                emit('your_turn', to=id)

    
    red_points, blue_points = user_room.get_points()
    emit("word_clicked", { 'word': _word, 'color': word_color, 'red_points': red_points, 'blue_points': blue_points, 'user_color': user_color, 'nickname': user_nickname}, to=user_room.players)
    
    if user_room.red_points == 0 or user_room.blue_points == 0:
        print("END GAME --- ADD EVENT")
        red_points, blue_points = user_room.get_points()
        winner = "red" if red_points == 0 else "blue"
        emit('end_game', { 'color': winner }, to=user_room.players)
    #if _user_id in rooms[user_data[_user_id]].

@socketio.on("give_clue")
def give_clue(action_data):
    _user_id = f'user_{session.get("user_id")}'
    _word = action_data['word']
    _number = action_data['number']
    
    # Get user room & user color
    user_room_name = user_data[_user_id]['room_name']
    nickname = user_data[_user_id]['nickname']
    user_room = rooms[user_room_name]
    user_color = user_data[_user_id]['color']

    # Change allowed clicks to number + 1
    user_room.give_clue(int(_number))
    user_room.updateTurn()
    
    # Get operatives
    red_spymaster, blue_spymaster, red_operatives, blue_operatives, red_points, blue_points = user_room
    
    current_operatives = []
    if user_color == "red":
        current_operatives = user_room.red_operatives
    else:
        current_operatives = user_room.blue_operatives
    
    neutral_teams = red_operatives + blue_operatives
    if (len(neutral_teams) > 0):
        emit('clue_given', { 'word': _word, 'number': _number, 'nickname': nickname }, to=user_room.players);

    emit("your_turn", {"word": _word, "number": _number, }, to=current_operatives)


def get_game_data(room_name):
     # Get all players in user_room
    current_room = rooms[room_name]
    game_data = {'red_spymaster': '', 'blue_spymaster': '', 'red_operatives': [], 'blue_operatives': []}
    
    
    # Get game usernames
    red_spymaster, blue_spymaster, red_operatives, blue_operatives, red_points, blue_points = current_room
    
    # Get spymaster nickname
    game_data['red_spymaster'] = user_data[red_spymaster]['nickname'] if red_spymaster  != "" else ''
    game_data['blue_spymaster'] = user_data[blue_spymaster]['nickname'] if blue_spymaster  != "" else ''
    
    
    # Get operatives nicknames
    for i in red_operatives:
        game_data['red_operatives'].append(user_data[i]['nickname'])
        
    for i in blue_operatives:
        game_data['blue_operatives'].append(user_data[i]['nickname'])
        
    return game_data