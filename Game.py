import Environment

game = Environment.Bus_environment

game.initialize(game, 'bus_schedule.txt','map_info.txt')

game.manual_run(game)

