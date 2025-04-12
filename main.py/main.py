‏import requests
‏from flask import Flask, request, jsonify

‏app = Flask(__name__)

‏TOKEN = 'f9LHodD0cOKNuzxSmZv2KHqLH_mwNI_5Onlhfqy8AjYM0hQ-jsKdGsa9KVZcWyqZwdXqC8L-XugSKS5W9JN_Tg'
‏API_URL = f'https://botapi.tamtam.chat'

‏game_state = {
‏    'board': [['➖', '➖', '➖'],
              ['➖', '➖', '➖'],
              ['➖', '➖', '➖']],
‏    'turn': '❌'
}

‏def draw_board():
‏    return "\n".join(["".join(row) for row in game_state['board']])

‏def check_winner():
‏    b = game_state['board']
‏    lines = b + list(map(list, zip(*b))) + [[b[i][i] for i in range(3)], [b[i][2-i] for i in range(3)]]
‏    for line in lines:
‏        if line[0] != '➖' and line.count(line[0]) == 3:
‏            return line[0]
‏    return None

‏def is_full():
‏    return all(cell != '➖' for row in game_state['board'] for cell in row)

‏def send_message(chat_id, text):
‏    data = {
‏        'chat_id': chat_id,
‏        'text': text
    }
‏    headers = {'Content-Type': 'application/json'}
‏    requests.post(f'{API_URL}/messages?access_token={TOKEN}', json=data, headers=headers)

‏@app.route('/', methods=['POST'])
‏def webhook():
‏    data = request.json
‏    if 'message' in data:
‏        chat_id = data['message']['recipient']['chat_id']
‏        text = data['message']['text']
        
‏        if text == '/start':
‏            game_state['board'] = [['➖'] * 3 for _ in range(3)]
‏            game_state['turn'] = '❌'
‏            send_message(chat_id, f"لعبة XO بدأت!\n{draw_board()}\nدور: {game_state['turn']}")
‏        elif text.startswith('/play'):
‏            try:
‏                _, row, col = text.split()
‏                row, col = int(row), int(col)
‏                if game_state['board'][row][col] == '➖':
‏                    game_state['board'][row][col] = game_state['turn']
‏                    winner = check_winner()
‏                    if winner:
‏                        send_message(chat_id, f"{draw_board()}\nالفائز هو: {winner}!")
‏                    elif is_full():
‏                        send_message(chat_id, f"{draw_board()}\nتعادل!")
‏                    else:
‏                        game_state['turn'] = '⭕' if game_state['turn'] == '❌' else '❌'
‏                        send_message(chat_id, f"{draw_board()}\nدور: {game_state['turn']}")
‏                else:
‏                    send_message(chat_id, "الخانة مشغولة، جرّب غيرها.")
‏            except Exception:
‏                send_message(chat_id, "اكتب الأمر بالشكل الصحيح: /play 0 2")
‏        else:
‏            send_message(chat_id, "أكتب /start للبدء أو /play [صف] [عمود]")

‏    return jsonify({'ok': True})