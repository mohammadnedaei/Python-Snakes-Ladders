# random lib is used to generate dice number both for players and CPU.
import random
# os lib is used to remove previously created files from directory.
import os
# time lib is used to make breaks during game.
import time
# Pillow lib is used for Image-based GUI (Graphical User Interface).
from PIL import Image
# psutil lib is used to quit opened image viewer in OS.
import psutil
# playsound lib is used to play sounds.
from playsound import playsound
# ast lib is used to import previously played game and converts string to dict.
import ast
# Colors are used for prints (GUI).
from colors import Colors
# Declaring Variables:

# Snake Points :O   ( for example: there is a snake in step 98 that bites and rolls player back to step 55 )
snake = [[98, 92, 82, 73, 56, 47, 30], [55, 75, 42, 51, 19, 15, 7]]
# Ladder Points :O   ( for example: there is a ladder in step 71 that rolls player up to step 89 )
ladder = [[71, 63, 43, 29, 21, 4], [89, 80, 76, 74, 39, 25]]
# All step positions are calculated from below steps
offset_main = [1, 20, 21, 40, 41, 60, 61, 80, 81, 100]
# All step heights are calculated from below positions
y_offsets = {
    "1": 1750,
    "20": 1580,
    "21": 1385,
    "40": 1190,
    "41": 1000,
    "60": 850,
    "61": 710,
    "80": 410,
    "81": 210,
    "100": 10
}
# Start position of each row
x_start_offset = 0
# dicts for saving player number along with player sign and its position.
players = dict()
player_values = list()


# function quit_images() will quit every image viewer app currently running using psutil processor id
def quit_images():
    for proc in psutil.process_iter():
        # Replace 'eog' by process name in Windows os
        if proc.name() == "eog":
            proc.kill()


# This function runs when snake bites the player
def is_snake(current_player, players):
    current_move = players[current_player][1]
    for index, value in enumerate(snake[0]):
        if value == current_move:
            # Update current player in players dictionary
            players[current_player][1] = snake[1][index]
            player_move = players[current_player][1]
            # Rest of function is just GUI and sounds
            print("Player {} bites by snake :(.\ndown to {}.".format(current_player, player_move))
            snake_layer = Image.new(mode="RGBA", size=(520, 520), color="white")
            snake_img = Image.open("img/snake.png")
            snake_layer.paste(snake_img, (0, 0), snake_img)
            snake_layer.show()
            # pause the game for 2 seconds
            playsound("sound/snake.wav")
            time.sleep(1)
            quit_images()


# This function runs when player got the ladder
def is_ladder(current_player, players):
    current_move = players[current_player][1]
    for index, value in enumerate(ladder[0]):
        if value == current_move:
            # Update current player in players dictionary
            players[current_player][1] = ladder[1][index]
            player_move = players[current_player][1]
            # Rest of function is just GUI and sounds
            print("Player {} got the ladder :).\nUp to {}.".format(current_player, player_move))
            ladder_layer = Image.new(mode="RGBA", size=(520, 520), color="white")
            ladder_img = Image.open("img/ladder.png")
            ladder_layer.paste(ladder_img, (0, 0), ladder_img)
            ladder_layer.show()
            # pause the game for 2 seconds
            playsound("sound/ladder.wav")
            time.sleep(1)
            quit_images()


# Main manu of game with GUI - sounds
def game_board():
    # GUI and sounds
    welcome = Image.open("img/welcome.png")
    board = Image.new(mode="RGBA", size=(1000, 1000), color="pink")
    board.paste(welcome, ((board.width - welcome.width) // 2, (board.height - welcome.height) // 2), welcome)
    board.show("Welcome To Snake And Ladders!!")
    playsound("sound/start-game.wav")
    time.sleep(1)
    quit_images()
    # Main Menu is here
    print(Colors.pink + "****** Welcome To Snake And Ladders Game *******" + Colors.pink + "\n")
    print(Colors.green+ "*1* To start new game!" + Colors.green)
    print(Colors.cyan + "*2* To import previously played game" + Colors.cyan)
    print(Colors.red + "*4* To exit" + Colors.red)
    option = input(Colors.yellow + "Choose Your option..." + Colors.yellow + "\n")
    # New Game with 1
    if option == "1":
        create_players(players, player_values)
    # Import Game with 2
    elif option == "2":
        import_file = open("import.txt")
        saved_game = import_file.read()
        # Convert Import.txt to dictionary
        imported_players = ast.literal_eval(saved_game)
        print(Colors.yellow + "Game Imported successfully, Continuing The Game..." + Colors.yellow)
        time.sleep(3)
        # show imported game to user
        update_game_board_gui(imported_players)
        # Continue game after import
        game_start(imported_players)
    # Quit Game with 4
    elif option == "4":
        # GUI and sounds
        bye_layer = Image.new(mode="RGBA", size=(512, 512), color="pink")
        bye_img = Image.open("img/bye.png")
        bye_layer.paste(bye_img, (0, 0), bye_img)
        bye_layer.show()
        time.sleep(2)
        quit_images()
        quit()


# Calculate current step's space from offset_main steps
def get_space(num):
    spaces = []
    x = 0
    while x < 10:
        y = offset_main[x] - num
        if num < 1:
            if y > -1:
                spaces.append(y)
        else:
            spaces.append(abs(y))
        x += 1
    spaces.sort()
    h = 0
    while h < 10:
        if offset_main[h] == 1 or offset_main[h] == 21 or offset_main[h] == 41 or offset_main[h] == 61 \
                or offset_main[h] == 81:
            z = offset_main[h] + abs(spaces[0])
        else:
            z = offset_main[h] - abs(spaces[0])
        if z == num:
            return offset_main[h], abs(spaces[0])
        h += 1


# Calculate current step's position ( x, y ) from get_space()
def get_offset(player_number, players):
    player_position = players[player_number][1]
    if player_position > 0:
        base, steps = get_space(player_position)
        # set position from get_space() here!
        dim = (x_start_offset + (int(steps)*195), y_offsets[str(base)])
        return dim
    else:
        # dimension for players out of the game
        dim = (-500, -500)
        return dim


# This function actually shows the current layer of players and stats.
def update_game_board_gui(players):
    player1 = Image.open("img/player-1.png")
    player2 = Image.open("img/player-2.png")
    player3 = Image.open("img/player-3.png")
    # If You Want To Play With CPU (ROBOT) Please Play This Game As 4-Player.
    robot = Image.open("img/robot.png")
    board = Image.open("img/board.jpg")
    if len(players) == 1:
        board.paste(player1, get_offset(1, players), player1)
    if len(players) == 2:
        board.paste(player1, get_offset(1, players), player1)
        board.paste(player2, get_offset(2, players), player2)
    if len(players) == 3:
        board.paste(player1, get_offset(1, players), player1)
        board.paste(player2, get_offset(2, players), player2)
        board.paste(player3, get_offset(3, players), player3)
    if len(players) == 4:
        board.paste(player1, get_offset(1, players), player1)
        board.paste(player2, get_offset(2, players), player2)
        board.paste(player3, get_offset(3, players), player3)
        board.paste(robot, get_offset(4, players), robot)
    quit_images()
    board.show()


# This function assigns players and starts the game (Min : 1P , Max: 4P)
# ( can be passed if you want to import the game )
def create_players(players, player_values):
    while True:
        # getting total players
        total_players = input(Colors.yellow + "Choose total number of player (min 1 and max 4): " + Colors.end).strip()
        # if number of players does not meet the conditions
        if total_players not in ['1', '2', '3', '4']:
            print(Colors.red + "Invalid input!" + Colors.end)
        # if number of players meet the conditions
        else:
            print("Total players in the game {}".format(total_players))

            # Set player assign or letter ( only used for players dict and is not necessary )
            total_players = int(total_players)
            for player_index in range(1, total_players + 1):
                while True:
                    set_marker = input("Now set your player sign {}:(alphabet only) ".format(player_index)).strip().upper()
                    if len(set_marker) != 1 or not(set_marker >= "A" and set_marker <= "Z"):
                        print(Colors.red + "Invalid Sign choosen!" + Colors.end)
                    else:
                        # Sign is set
                        player_values.append(set_marker)
                        # initial position of the player on the board is set to the zero
                        player_values.append(0)
                        # every player last move is stored, to display along the current player's move
                        player_values.append("")
                        # player values as a list is stored in the dictionary(players) as its values. 
                        players[player_index] = player_values
                        player_values = []
                        break
            break
    game_start(players)


# Save Game in export.txt
def export_game(players):
    if os.path.exists("export.txt"):
        os.remove("export.txt")
    export_file = open("export.txt", "w")
    export_file.write(str(players))
    export_file.close()
    print(Colors.green + "The game has been saved successfully!!" + Colors.green)


# This actually rolls the dice and checks
# for snakes and ladders and then updates the board (somehow, Everything )
def game_start(players):
    # way to start with first player ( order of playing )
    from_player = len(players) - (len(players) - 1)
    till_player = len(players) + 1
    flag = True
    while flag:
        x = 1
        while from_player <= x < till_player:
            current_player = x
            current_player_sign = players[current_player][0]
            ## Robot Order
            if len(players) == 4 and current_player == 4:
                pass
            else:
                print("*3* To save current game")
                session = input(Colors.blue + "Player " + current_player_sign + " press [ENTER] to roll the dice: " +
                                Colors.end)
                if session == "3":
                    # Save Game
                    export_game(players)
                    # GUI for quit
                    bye_layer = Image.new(mode="RGBA", size=(512, 512), color="pink")
                    bye_img = Image.open("img/bye.png")
                    bye_layer.paste(bye_img, (0, 0), bye_img)
                    bye_layer.show()
                    time.sleep(2)
                    quit_images()
                    quit()
                else:
                    pass

            # random library is used for dice work
            p_move_prize = 0
            player_move = random.randint(1, 6)
            dice_layer = Image.new(mode="RGBA", size=(520, 520), color="white")
            dice_img = Image.open("img/" + str(player_move) +".png")
            dice_layer.paste(dice_img, (0, 0), dice_img)
            if player_move > 5:
                p_move_prize = 1
            dice_layer.show()
            time.sleep(1)
            quit_images()
            print("The Dice Number is " + str(player_move))
            if int(player_move) > 5:
                print(Colors.green + "Yaaaaaay!! You have a prize" + Colors.end)
            if players[current_player][1] == 0 and player_move < 6:
                pass
            else:
                if players[current_player][1] == 0 and player_move > 5:
                    players[current_player][1] += 1
                else:
                    playsound("sound/move.wav")
                    players[current_player][1] += player_move
                # checking for snake or ladder as player moves up
                if players[current_player][1] in snake[0]:
                    is_snake(current_player, players)
                if players[current_player][1] in ladder[0]:
                    is_ladder(current_player, players)

                if players[current_player][1] == 100:
                    player_move = str(players[current_player][1])
                    update_game_board_gui(players)
                    print("Player {} won the game!".format(current_player))
                    flag = False
                    break
                elif players[current_player][1] < 100:
                    player_move = str(players[current_player][1])
                    update_game_board_gui(players)
                    print("Player {} reach to {} position.".format(current_player_sign, player_move))
                    time.sleep(1)
                else:
                    players[current_player][1] -= player_move
                    player_move = str(players[current_player][1])
                    update_game_board_gui(players)
                    continue
            if p_move_prize > 0:
                x -= 1
            x += 1


# from this function game will be start
game_board()
