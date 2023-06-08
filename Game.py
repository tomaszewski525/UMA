import Environment

game = Environment.Bus_environment

game.initialize(game, 'Maps/2/bus_schedule.txt','Maps/2/map_info.txt')

game.manual_run(game)

