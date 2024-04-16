var activeTeam = 'red'; //default
var activeRole = 'operative'; //default 

var room_name = window.location.href.split('/')[window.location.href.split('/').length - 1]

function giveClue() 
{
    var word = document.getElementById('word').value;
    var number = document.getElementById('number').value;

    socket.emit('give_clue', { 'word': word, 'number': number });

    var guessForm = document.getElementById('guessForm');
    guessForm.style.display = 'none';
}

// function generateUniqueId() {
//     return uuidv4();
// }

function disableAllJoinButtons() {
    joinButtons = document.querySelectorAll('.join-btn')
    joinButtons.forEach(function (button) {
        button.style.display = 'none';
    });
}

function disableAllCardButtons() {
    cardButtons = document.querySelectorAll('.card-btn')
    cardButtons.forEach(function (button) {
        button.style.display = 'none';
    });
    
    // hide p elements
    pElements = document.querySelectorAll('.card-text')
    pElements.forEach(function (p) {
        p.style.display = 'block';
    });

    document.getElementById('word-clue').value = '';
    document.getElementById('number-clue').value = 0 ;

    document.getElementById('clueForm').style.display = 'none';
}

function loadUsers(_game_data) {

    if (_game_data.red_spymaster) {
        red_spymaster_div = document.querySelector('.red-spymaster');
        red_spymaster_p = `<p>${_game_data['red_spymaster']}</p>`
        red_spymaster_div.innerHTML = (red_spymaster_p)

        // Disable red_spymaster button
        red_spymaster_button = document.querySelector('.red-spymaster-btn');
        red_spymaster_button.style.display = 'none';
    }


    if (_game_data.blue_spymaster) {
        blue_spymaster_div = document.querySelector('.blue_spymaster');
        blue_spymaster_p = `<p>${_game_data['blue_spymaster']}</p>`
        blue_spymaster_div.innerHTML = (blue_spymaster_p)
        
        // Disable blue_spymaster button if there's any
        blue_spymaster_button = document.querySelector('.blue-spymaster-btn');
        blue_spymaster_button.style.display = 'none';
    }

    if (_game_data.red_operatives.length > 0) {
        red_operatives_p = ``
        _game_data.red_operatives.forEach((operative) => {
            red_operatives_p += `<p>${operative}</p>`
        })
        red_operative_div = document.querySelector('.red-operatives');
        red_operative_div.innerHTML = (red_operatives_p)
    }

    if (_game_data.blue_operatives.length > 0) {
        blue_operatives_p = ``
        _game_data.blue_operatives.forEach((operative) => {
            blue_operatives_p += `<p>${operative}</p>`
        })
        blue_operatives_div = document.querySelector('.blue_operatives');
        blue_operatives_div.innerHTML = (blue_operatives_p)
    }
}

async function join_room() {
    var username = document.getElementById('nickname').value;
    console.log(username)
    url = window.location.href.split('/')
    await socket.emit('join_game_room', { 'room_name': url[url.length - 1], 'nickname': username});

    var join_game_container = document.querySelector('.join-form-container');
    join_game_container.style.display = 'none';

    var game_container = document.querySelector('.container');
    game_container.style.display = 'flex';

    loadUsers();
}

function join_red_spymaster() {
    url = window.location.href.split('/')
    socket.emit('join_red_spymaster', { room_name: room_name })

    disableAllJoinButtons();
}

function join_red_operatives() {
    url = window.location.href.split('/')
    socket.emit('join_red_operatives', { room_name: room_name })

    disableAllJoinButtons();
}

function join_blue_spymaster() {
    url = window.location.href.split('/')
    socket.emit('join_blue_spymaster', { room_name: room_name })

    disableAllJoinButtons();
}

function join_blue_operatives() {
    socket.emit('join_blue_operatives', { room_name: room_name });

    // joinButton = document.querySelector('.blue-operatives-btn')
    // joinButton.style.display = 'none'
    disableAllJoinButtons();
}

function start_game() {
    socket.emit('start_game', { room_name: room_name });
}

function handleButtonClick(word) {
    console.log(word);
    socket.emit('click_word', { room_name: room_name, word: word });
}

function enableButtons() {

    // hide p elements
    pElements = document.querySelectorAll('.card-text')
    pElements.forEach(function (p) {
        if (!(p.parentElement.classList.contains('clicked'))) p.style.display = 'none';
    });

    cardButtons = document.querySelectorAll('.card-btn')
    cardButtons.forEach(function (button) {
        if (!button.classList.contains('clicked')) {
            button.disabled = false
            button.style.display = 'block';
        };
    });
}

var socket = io();

socket.on('connect', function() {
    console.log("IAM CONNECTED")
});

socket.on("player_update", function(game_data) {
    _game_data = game_data['game_data'];
    loadUsers(_game_data);
});


socket.on("start_game", function(words) {
    game_settings_container = document.querySelector('.game-start-settings');
    game_settings_container.style.display = 'none';
    _words = words['words'];
    _red_points = words['red_points'];
    _blue_points = words['blue_points'];

    var main_container = document.getElementById('cards-container');
    var words_div = document.querySelector('.grid-container');
    Object.entries(_words).forEach(([word, color]) => {
        var divElement = document.createElement('div');
        divElement.id = `word-${word}`
        _color = color ? color : "neutral"
        divElement.className = `grid-item card ${_color}-card`;

        // Create p element
        var pElement = document.createElement('p');
        pElement.className = 'card-text'
        pElement.innerText = word;
      
        // Create a button element with class "grid-item card-btn" and attach a click event
        var buttonElement = document.createElement('button');
        buttonElement.className = 'card-btn';
        buttonElement.textContent = word;
        buttonElement.disabled = true;
        buttonElement.onclick = function() {
          handleButtonClick(word);
        };
        buttonElement.style.display = 'none';

        divElement.appendChild(buttonElement);
        divElement.appendChild(pElement);
        words_div.appendChild(divElement);
    })
    main_container.style.display = 'flex';

    red_points_h1 = document.getElementById('red-points');
    blue_points_h1 = document.getElementById('blue-points');
    red_points_h1.innerText = _red_points;
    blue_points_h1.innerText = _blue_points;
});

socket.on("word_clicked", function(word_data) {
    console.log("WORD CLICKED")
    _word = word_data['word']
    _color = word_data['color']
    _user_color = word_data['user_color']
    _nickname = word_data['nickname']
    _red_points = parseInt(word_data['red_points'])
    _blue_points = parseInt(word_data['blue_points'])

    div = document.getElementById(`word-${_word}`);
    if (div.firstChild) div.removeChild(div.firstChild);
    div.className = `grid-item card ${_color}-card clicked`;
    div.querySelector('.card-text').style.display = 'block';

    red_points_h1 = document.getElementById('red-points');
    blue_points_h1 = document.getElementById('blue-points');
    red_points_h1.innerText = _red_points;
    blue_points_h1.innerText = _blue_points;

    gameLog = document.getElementById('gamelog');
    newLog = document.createElement('p');
    newLog.innerHTML = `<p><em style="color: ${_user_color}">${_nickname}</em> clicks <em style="color: ${_color}">${_word}</em></p>`;
    gameLog.append(newLog)
})

socket.on("turn_done", function() {
    document.getElementById('clueForm').style.display = 'none';
})

socket.on("give_clue", function(color) {
    var form = document.getElementById("guessForm")
    form.style.display = 'block'
})

socket.on("clue_given", function(word_data) {
    console.log("CLUE GIVEN")
    _word = word_data['word']
    _number = word_data['number']
    _nickname = word_data['nickname']

    document.getElementById('guessForm').style.display = 'none';

    document.getElementById('word-clue').value = _word;
    document.getElementById('number-clue').value = _number;

    document.getElementById('clueForm').style.display = 'block';
    
    gameLog = document.getElementById('gamelog');
    newLog = document.createElement('p');
    newLog.innerHTML = `<p class="clue">${_nickname} gives clue <em>${_word} ${_number} </em></p>`
    gameLog.append(newLog)
})

socket.on('your_turn', function(){
    enableButtons();
})

socket.on('end_turn', function(){
    disableAllCardButtons();
})

socket.on('end_game', function(data){
    _color = data['color']
    disableAllCardButtons();
    div = document.querySelector('.end-game')
    p = document.createElement('p');
    p.innerText = `${String(_color).toUpperCase()} WINS`
    div.appendChild(p)
    div.style.display = 'block'
})