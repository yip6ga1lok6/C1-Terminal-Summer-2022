import gamelib
import random
import math
import warnings
from sys import maxsize
import json


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""


class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP, ENEMY_MAP, FRIENDLY_MAP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        ENEMY_MAP = [[13, 27], [14, 27], [12, 26], [13, 26], [14, 26], [15, 26], [11, 25], [12, 25], [13, 25], [14, 25], [15, 25], [16, 25], [10, 24], [11, 24], [12, 24], [13, 24], [14, 24], [15, 24], [16, 24], [17, 24], [9, 23], [10, 23], [11, 23], [12, 23], [13, 23], [14, 23], [15, 23], [16, 23], [17, 23], [18, 23], [8, 22], [9, 22], [10, 22], [11, 22], [12, 22], [13, 22], [14, 22], [15, 22], [16, 22], [17, 22], [18, 22], [19, 22], [7, 21], [8, 21], [9, 21], [10, 21], [11, 21], [12, 21], [13, 21], [14, 21], [15, 21], [16, 21], [17, 21], [18, 21], [19, 21], [20, 21], [6, 20], [7, 20], [8, 20], [9, 20], [10, 20], [11, 20], [12, 20], [13, 20], [14, 20], [15, 20], [16, 20], [17, 20], [18, 20], [19, 20], [20, 20], [21, 20], [5, 19], [6, 19], [7, 19], [8, 19], [9, 19], [10, 19], [11, 19], [12, 19], [13, 19], [14, 19], [15, 19], [16, 19], [17, 19], [18, 19], [19, 19], [20, 19], [21, 19], [22, 19], [4, 18], [5, 18], [6, 18], [7, 18], [8, 18], [9, 18], [10, 18], [11, 18], [12, 18], [13, 18], [14, 18], [15, 18], [16, 18], [17, 18], [
            18, 18], [19, 18], [20, 18], [21, 18], [22, 18], [23, 18], [3, 17], [4, 17], [5, 17], [6, 17], [7, 17], [8, 17], [9, 17], [10, 17], [11, 17], [12, 17], [13, 17], [14, 17], [15, 17], [16, 17], [17, 17], [18, 17], [19, 17], [20, 17], [21, 17], [22, 17], [23, 17], [24, 17], [2, 16], [3, 16], [4, 16], [5, 16], [6, 16], [7, 16], [8, 16], [9, 16], [10, 16], [11, 16], [12, 16], [13, 16], [14, 16], [15, 16], [16, 16], [17, 16], [18, 16], [19, 16], [20, 16], [21, 16], [22, 16], [23, 16], [24, 16], [25, 16], [1, 15], [2, 15], [3, 15], [4, 15], [5, 15], [6, 15], [7, 15], [8, 15], [9, 15], [10, 15], [11, 15], [12, 15], [13, 15], [14, 15], [15, 15], [16, 15], [17, 15], [18, 15], [19, 15], [20, 15], [21, 15], [22, 15], [23, 15], [24, 15], [25, 15], [26, 15], [0, 14], [1, 14], [2, 14], [3, 14], [4, 14], [5, 14], [6, 14], [7, 14], [8, 14], [9, 14], [10, 14], [11, 14], [12, 14], [13, 14], [14, 14], [15, 14], [16, 14], [17, 14], [18, 14], [19, 14], [20, 14], [21, 14], [22, 14], [23, 14], [24, 14], [25, 14], [26, 14], [27, 14]]
        FRIENDLY_MAP = [[0, 13], [1, 13], [2, 13], [3, 13], [4, 13], [5, 13], [6, 13], [7, 13], [8, 13], [9, 13], [10, 13], [11, 13], [12, 13], [13, 13], [14, 13], [15, 13], [16, 13], [17, 13], [18, 13], [19, 13], [20, 13], [21, 13], [22, 13], [23, 13], [24, 13], [25, 13], [26, 13], [27, 13], [1, 12], [2, 12], [3, 12], [4, 12], [5, 12], [6, 12], [7, 12], [8, 12], [9, 12], [10, 12], [11, 12], [12, 12], [13, 12], [14, 12], [15, 12], [16, 12], [17, 12], [18, 12], [19, 12], [20, 12], [21, 12], [22, 12], [23, 12], [24, 12], [25, 12], [26, 12], [2, 11], [3, 11], [4, 11], [5, 11], [6, 11], [7, 11], [8, 11], [9, 11], [10, 11], [11, 11], [12, 11], [13, 11], [14, 11], [15, 11], [16, 11], [17, 11], [18, 11], [19, 11], [20, 11], [21, 11], [22, 11], [23, 11], [24, 11], [25, 11], [3, 10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10], [9, 10], [10, 10], [11, 10], [12, 10], [13, 10], [14, 10], [15, 10], [16, 10], [17, 10], [18, 10], [19, 10], [20, 10], [21, 10], [22, 10], [23, 10], [
            24, 10], [4, 9], [5, 9], [6, 9], [7, 9], [8, 9], [9, 9], [10, 9], [11, 9], [12, 9], [13, 9], [14, 9], [15, 9], [16, 9], [17, 9], [18, 9], [19, 9], [20, 9], [21, 9], [22, 9], [23, 9], [5, 8], [6, 8], [7, 8], [8, 8], [9, 8], [10, 8], [11, 8], [12, 8], [13, 8], [14, 8], [15, 8], [16, 8], [17, 8], [18, 8], [19, 8], [20, 8], [21, 8], [22, 8], [6, 7], [7, 7], [8, 7], [9, 7], [10, 7], [11, 7], [12, 7], [13, 7], [14, 7], [15, 7], [16, 7], [17, 7], [18, 7], [19, 7], [20, 7], [21, 7], [7, 6], [8, 6], [9, 6], [10, 6], [11, 6], [12, 6], [13, 6], [14, 6], [15, 6], [16, 6], [17, 6], [18, 6], [19, 6], [20, 6], [8, 5], [9, 5], [10, 5], [11, 5], [12, 5], [13, 5], [14, 5], [15, 5], [16, 5], [17, 5], [18, 5], [19, 5], [9, 4], [10, 4], [11, 4], [12, 4], [13, 4], [14, 4], [15, 4], [16, 4], [17, 4], [18, 4], [10, 3], [11, 3], [12, 3], [13, 3], [14, 3], [15, 3], [16, 3], [17, 3], [11, 2], [12, 2], [13, 2], [14, 2], [15, 2], [16, 2], [12, 1], [13, 1], [14, 1], [15, 1], [13, 0], [14, 0]]
        self.current_structure_map = [False for pos in FRIENDLY_MAP]
        self.preemptive_destroying_location = []
        self.preemptive_rebuilding_location = []
        MP = 1
        SP = 0
        # This is a good place to do initial setup

        # define structure locations here

        # s
        self.wall_build_core = [[0, 13], [1, 13], [26, 13], [27, 13], [2, 12], [4, 12], [5, 12], [22, 12], [23, 12], [25, 12], [2, 11], [6, 11], [21, 11], [25, 11], [
            7, 10], [20, 10], [7, 9], [20, 9], [7, 8], [20, 8], [8, 7], [19, 7], [9, 6], [18, 6], [10, 5], [11, 5], [12, 5], [13, 5], [14, 5], [15, 5], [16, 5], [17, 5]]

        # s u
        self.turret_build_core = [[4, 11], [1, 12], [26, 12], [23, 11]]

        # u
        self.wall_upgrade_core1 = [[4, 12], [5, 12],
                                   [22, 12], [23, 12], [6, 11], [21, 11]]

        self.wall_upgrade_core2 = [[0, 13], [1, 13], [26, 13], [27, 13], [2, 12], [
            25, 12], [2, 11], [25, 11]]

        self.wall_upgrade_core3 = [
            [7, 10], [20, 10], [7, 9], [20, 9], [7, 8], [20, 8]]
        # s u
        self.turret_build_s1 = [[5, 11], [22, 11]]
        self.wall_build_core2 = [[2, 13], [25, 13], [6, 12], [21, 12]]

        self.interceptor_path_left = [[5, 10], [5, 9], [9, 5]]
        self.interceptor_path_right = [[22, 10], [22, 9], [18, 5]]
        self.support_left_core = [[7, 11], [8, 11], [9, 11], [10, 11]]
        self.support_left_core2 = [[8, 10], [9, 10], [10, 10]]
        self.support_left_core3 = [[8, 9], [9, 9], [10, 9]]
        self.support_left_core4 = [[8, 8], [9, 8], [10, 8]]
        self.support_right_core = [[20, 11], [19, 11], [18, 11], [17, 11]]
        self.support_right_core2 = [[19, 10], [18, 10], [17, 10]]
        self.support_right_core3 = [[19, 9], [18, 9], [17, 9]]
        self.support_right_core4 = [[19, 8], [18, 8], [17, 9]]

        self.interceptor_attack_right = [[21, 7], [20, 6], [19, 5]]
        self.interceptor_attack_left = [[6, 7], [7, 6], [8, 5]]

        self.default_spawn_right_fast = [[24, 10]]
        self.default_spawn_right_slow = [[23, 9]]
        self.default_spawn_left_fast = [[3, 10]]
        self.default_spawn_left_slow = [[4, 9]]
        self.scored_on_locations = []

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(
            game_state.turn_number))
        # Comment or remove this line to enable warnings.
        game_state.suppress_warnings(True)

        self.cloverfield_strategy(game_state)

        game_state.submit_turn()

    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """

    def cloverfield_strategy(self, game_state):
        """
        Strategy based on predictions of enemy behaviours
        """
        self.destructive_interceptors_count = 0
        self.enemy_shielding_power = 0
        self.preemptive_destroying_location = []
        self.enemy_vertical_opens = [True for i in range(28)]
        self.enemy_left_open = False
        self.enemy_right_open = False
        self.cf_preflight(game_state)
        self.cf_build_core(game_state)
        self.cf_deploy_core(game_state)

    def cf_preflight(self, game_state) -> None:
        """
        Analyse the current game conditions:
        1. If enemy has MP > 10, prepare self destructive interceptors
        2. If enemy's total effective shielding amount > 40, prepare more destructive interceptors
        3. Rebuild the pre-emptively destroyed structures
        4. Define the frontline units that should be pre-emptively destroyed in this round
        5. Scan enemy defense line for any new holes to be opened next round
        6. Determine enemy's side of openings
        """

        # 1. If enemy has MP > 10, prepare self destructive interceptors
        if game_state.get_resource(1, 1) >= 10:
            self.destructive_interceptors_count += 1
        # gamelib.debug_write("Enemy has {} MP".format(
        #     game_state.get_resource(1, 1)))

        # 2. If enemy's total effective shielding amount > 25, prepare more destructive interceptors
        # health for scout is 15, 25+15 will require an additional interceptor (40)
        for enemyLocation in ENEMY_MAP:
            unit = game_state.contains_stationary_unit(enemyLocation)
            if unit != False:
                if unit.unit_type == "EF":
                    self.enemy_shielding_power += self.cf_calculate_support_power(
                        unit.y, unit.upgraded)
        self.destructive_interceptors_count += (
            self.enemy_shielding_power+25)//40
        # gamelib.debug_write("Enemy has {} effective shielding".format(
        #     self.enemy_shielding_power))

        # 3. Rebuild the pre-emptively destroyed structures
        for rebuild_unit in self.preemptive_rebuilding_location:
            gamelib.debug_write("Rebuilding {}".format(rebuild_unit))
            unit_type = rebuild_unit.unit_type
            if(unit_type == "FF"):
                unit_type = WALL
            elif(unit_type == "EF"):
                unit_type = SUPPORT
            elif(unit_type == "DF"):
                unit_type = TURRET
            else:
                game_state.warn(
                    "Unknown structure type: {}".format(unit_type))
                continue
            game_state.attempt_spawn(
                unit_type, [rebuild_unit.x, rebuild_unit.y])
            if(rebuild_unit.upgraded):
                game_state.attempt_upgrade([rebuild_unit.x, rebuild_unit.y])

        # 4. Define the frontline units that should be pre-emptively repaired in this round
        # load the current structure state before the coming round start
        # game_state.attempt_spawn(WALL, [[5, 10], [6, 10], [5, 11], [7, 12]])
        # game_state.attempt_spawn(TURRET, [[5, 9], [6, 9]])
        # game_state.attempt_upgrade([[5, 10], [6, 10], [5, 11]])
        # game_state.attempt_upgrade([[6, 9]])
        self.current_structure_map = [game_state.contains_stationary_unit(
            pos) for pos in FRIENDLY_MAP]
        for structure in self.current_structure_map:
            if(structure != False):
                # remove a structure if its current health is less than 60% of its maximum health
                maxhealth = 1
                if(structure.unit_type == "FF"):
                    if(structure.upgraded):
                        # source code bug: init a upgraded wall but health is still recorded as 12 in the first round
                        if(structure.health == 12):
                            maxhealth = 12
                        else:
                            maxhealth = 120
                    else:
                        maxhealth = 12
                elif(structure.unit_type == "EF"):
                    maxhealth = 30
                elif(structure.unit_type == "DF"):
                    maxhealth = 75
                else:
                    game_state.warn(
                        "Unknown structure type: {}".format(structure.unit_type))
                    continue

                if(structure.health/maxhealth <= 0.6):
                    self.preemptive_destroying_location.append(structure)
                    game_state.attempt_remove([structure.x, structure.y])
        # record the removed structures, rebuild next round
        self.preemptive_rebuilding_location = self.preemptive_destroying_location
        # gamelib.debug_write(
        #     "Pre-emptively destroying {} structures".format(self.preemptive_destroying_location))

        # 5. Scan enemy defense line for any new holes to be opened next round
        # 6. Determine enemy's side of openings
        self.cf_compute_line_continuity(game_state, True, 0, [])
        if(self.enemy_vertical_opens[0:14].count(True)):
            self.enemy_right_open = True
        if(self.enemy_vertical_opens[14:28].count(True)):
            self.enemy_left_open = True
        gamelib.debug_write(
            "Left open is {} (our perspective)".format(self.enemy_right_open))
        gamelib.debug_write(
            "Right open is {} (our perspective)".format(self.enemy_left_open))

    def cf_compute_line_continuity(self, game_state, fullScan: bool, line: int, coordinates: list):
        """
        Compute the continuity of the enemy defense line
        Record any holes for mobile units to pass
        """
        # end of recursion
        if(line == 28):
            return
        # receive the coordinates of interests from the previous iteration
        checkCoordinates = []
        nextCoordinates = []
        nextfullScan = True
        if(fullScan):
            # scan the whole verticle line
            checkCoordinates = [pos for pos in ENEMY_MAP if pos[0] == line]
        else:
            # scan the next round's coordinates
            checkCoordinates = coordinates
        xCoord = line
        for coordinate in checkCoordinates:
            coordinateContent = game_state.contains_stationary_unit(coordinate)
            if(coordinateContent != False):
                yCoord = coordinateContent.y
                nextCoordinates.append(tuple([xCoord+1, yCoord-1])
                                       )
                nextCoordinates.append(tuple(
                    [xCoord+1, yCoord]))
                nextCoordinates.append(tuple([xCoord+1, yCoord+1])
                                       )
                nextfullScan = False
                self.enemy_vertical_opens[xCoord] = False
                yExtension = yCoord+1
                while(game_state.contains_stationary_unit([xCoord, yExtension]) != False):
                    nextCoordinates.append(tuple([xCoord+1, yExtension+1]))
                    yExtension += 1
                yExtension = yCoord-1
                while(game_state.contains_stationary_unit([xCoord, yExtension]) != False):
                    nextCoordinates.append(tuple([xCoord+1, yExtension-1]))
                    yExtension -= 1
        nextCoordinates = list(set(nextCoordinates))
        nextCoordinatesList = []
        for tp in nextCoordinates:
            nextCoordinatesList.append(list(tp))
        nextCoordinatesList = [
            coord for coord in nextCoordinatesList if coord[1] >= 14]
        gamelib.debug_write("check these next {}".format(nextCoordinatesList))
        self.cf_compute_line_continuity(
            game_state, nextfullScan, xCoord+1, nextCoordinatesList)
        return

    def cf_calculate_support_power(self, y: int, upgraded: bool) -> int:
        """
        calculate the shield a particular enemy support provides
        """
        if (upgraded):
            return 2 + (27 - y) * 0.34
        else:
            return 3

    def cf_build_core(self, game_state):
        game_state.attempt_spawn(WALL, self.wall_build_core)
        game_state.attempt_spawn(TURRET, self.turret_build_core)
        game_state.attempt_spawn(TURRET, self.turret_build_s1)
        if(self.enemy_right_open):
            game_state.attempt_spawn(WALL, self.interceptor_path_left)
        if(self.enemy_left_open):
            game_state.attempt_spawn(WALL, self.interceptor_path_right)
        game_state.attempt_upgrade(self.wall_upgrade_core2)
        game_state.attempt_upgrade(self.wall_upgrade_core1)
        game_state.attempt_upgrade(self.turret_build_core)
        game_state.attempt_upgrade(self.turret_build_s1)
        game_state.attempt_spawn(WALL, self.wall_build_core2)
        game_state.attempt_upgrade(self.wall_build_core2)

        # Reactive build starts here
        if(self.enemy_right_open):
            game_state.attempt_spawn(WALL, self.interceptor_path_left)
            if(game_state.turn_number > 12):
                game_state.attempt_spawn(SUPPORT, self.support_left_core)
                game_state.attempt_upgrade(self.support_left_core)
                game_state.attempt_spawn(SUPPORT, self.support_left_core2)
                game_state.attempt_upgrade(self.support_left_core2)
                game_state.attempt_spawn(SUPPORT, self.support_left_core3)
                game_state.attempt_upgrade(self.support_left_core3)
                game_state.attempt_spawn(SUPPORT, self.support_left_core4)
                game_state.attempt_upgrade(self.support_left_core4)
        else:
            game_state.attempt_remove(self.interceptor_path_left)

        if(self.enemy_left_open):
            game_state.attempt_spawn(WALL, self.interceptor_path_right)
            if(game_state.turn_number > 12):
                game_state.attempt_spawn(SUPPORT, self.support_right_core)
                game_state.attempt_upgrade(self.support_right_core)
                game_state.attempt_spawn(SUPPORT, self.support_right_core2)
                game_state.attempt_upgrade(self.support_right_core2)
                game_state.attempt_spawn(SUPPORT, self.support_right_core3)
                game_state.attempt_upgrade(self.support_right_core3)
                game_state.attempt_spawn(SUPPORT, self.support_right_core4)
                game_state.attempt_upgrade(self.support_right_core4)
        else:
            game_state.attempt_remove(self.interceptor_path_right)

        if(game_state.turn_number > 20):
            game_state.attempt_upgrade(self.wall_upgrade_core3)

    def cf_deploy_core(self, game_state):
        if game_state.turn_number <= 5:
            game_state.attempt_spawn(
                DEMOLISHER, self.default_spawn_left_slow, 2)
        else:
            if(not self.enemy_left_open and not self.enemy_right_open):
                # enemy fully blocked off
                return
            elif(self.enemy_left_open and self.enemy_right_open):
                # interceptorCount = self.destructive_interceptors_count
                # while(interceptorCount > 0):
                #     game_state.attempt_spawn(
                #         INTERCEPTOR, self.interceptor_attack_left[1:2])
                #     game_state.attempt_spawn(
                #         INTERCEPTOR, self.interceptor_attack_right[1:2])
                #     interceptorCount -= 1
                game_state.attempt_spawn(
                    INTERCEPTOR, self.interceptor_attack_left[1:2])
                game_state.attempt_spawn(
                    INTERCEPTOR, self.interceptor_attack_right[1:2])
                if game_state.turn_number > 10:
                    for i in range(min(2, game_state.turn_number // 15)):
                        self.cf_deploy_destructive_interceptors(
                            game_state, 0, (i+2) % 3+1)
                        self.cf_deploy_destructive_interceptors(
                            game_state, 1, (i+2) % 3+1)

                if game_state.turn_number % ((game_state.turn_number//20)+5) == 1:
                    game_state.attempt_spawn(
                        DEMOLISHER, self.default_spawn_left_slow, min(4, ((game_state.turn_number//20)+2)))
                    game_state.attempt_spawn(
                        SCOUT, self.default_spawn_left_fast, 1000)

            elif(self.enemy_right_open):
                # interceptorCount = self.destructive_interceptors_count
                # while(interceptorCount > 0):
                #     # game_state.attempt_spawn(
                #     #     INTERCEPTOR, self.interceptor_attack_left[1:2])
                #     game_state.attempt_spawn(
                #         INTERCEPTOR, self.interceptor_attack_left[0:1])
                #     interceptorCount -= 1
                self.cf_deploy_destructive_interceptors(game_state, 0, 2)
                if game_state.turn_number > 10:
                    for i in range(min(4, game_state.turn_number // 12)):
                        self.cf_deploy_destructive_interceptors(
                            game_state, 0, (i+2) % 3+1)

                if game_state.turn_number % ((game_state.turn_number//20)+5) == 1:
                    game_state.attempt_spawn(
                        DEMOLISHER, self.default_spawn_left_slow, min(4, ((game_state.turn_number//20)+2)))
                    game_state.attempt_spawn(
                        SCOUT, self.default_spawn_left_fast, 1000)

            elif(self.enemy_left_open):
                # interceptorCount = self.destructive_interceptors_count
                # while(interceptorCount > 0):
                #     # game_state.attempt_spawn(
                #     #     INTERCEPTOR, self.interceptor_attack_right[1:2])
                #     game_state.attempt_spawn(
                #         INTERCEPTOR, self.interceptor_attack_right[0:1])
                #     interceptorCount -= 1
                self.cf_deploy_destructive_interceptors(game_state, 1, 2)
                if game_state.turn_number > 10:
                    for i in range(min(4, game_state.turn_number // 12)):
                        self.cf_deploy_destructive_interceptors(
                            game_state, 1, (i+2) % 3+1)

                if game_state.turn_number % ((game_state.turn_number//20)+5) == 1:
                    game_state.attempt_spawn(
                        DEMOLISHER, self.default_spawn_right_slow, min(4, ((game_state.turn_number//20)+2)))
                    game_state.attempt_spawn(
                        SCOUT, self.default_spawn_right_fast, 1000)
            else:
                return

    def cf_deploy_destructive_interceptors(self, game_state, side, pos):
        """
        Deploys the destructive interceptors.
        Side:
        0 = Left
        1 = Right

        Pos: 
        1 = Close
        2 = Mid
        3 = Far
        """
        if(side):
            game_state.attempt_spawn(
                INTERCEPTOR, self.interceptor_attack_right[pos-1:pos])
        else:
            game_state.attempt_spawn(
                INTERCEPTOR, self.interceptor_attack_left[pos-1:pos])

    def siphon_strategy(self, game_state):
        """
        Build walls in v shape to direct enemy units into the desired path (right or left side)
        """
        # First turn: Place defences at default location
        if game_state.turn_number == 1:
            self.siphon_build_core_defences(game_state)
        else:
            # Each turn: 1. Rebuild any destroyed core defences 2. Build reactive defenses
            self.siphon_repair_core_defences(game_state)
            self.siphon_build_reactive_defense(game_state)

        # Using the starter algo to deploy mobile units
        # If the turn is less than 5, stall with interceptors and wait to see enemy's base
        if game_state.turn_number < 5:
            self.stall_with_interceptors(game_state)
        else:
            # Now let's analyze the enemy base to see where their defenses are concentrated.
            # If they have many units in the front we can build a line for our demolishers to attack them at long range.
            # if self.detect_enemy_unit(game_state, unit_type=None, valid_x=None, valid_y=[14, 15]) > 10:
            #     self.demolisher_line_strategy(game_state)
            # else:
            # They don't have many units in the front so lets figure out their least defended area and send Scouts there.

            # Only spawn Scouts every other turn
            # Sending more at once is better since attacks can only hit a single scout at a time
            if game_state.turn_number % 2 == 1:
                # To simplify we will just check sending them from back left and right
                scout_spawn_location_options = [[13, 0], [14, 0]]
                best_location = self.least_damage_spawn_location(
                    game_state, scout_spawn_location_options)
                game_state.attempt_spawn(SCOUT, best_location, 1000)

    def siphon_build_core_defences(self, game_state):
        """
        Build basic defenses using hardcoded locations
        """
        gamelib.debug_write("Building core defenses")
        wall_upgrade_locations = [[5, 12], [21, 12]]
        game_state.attempt_spawn(WALL, self.frontline_wall_locations)
        game_state.attempt_spawn(TURRET, self.frontline_turrent_locations)
        game_state.attempt_upgrade(wall_upgrade_locations)
        game_state.attempt_spawn(WALL, self.pathing_wall_locations)
        game_state.attempt_spawn(WALL, self.side_wall_locations)

    def siphon_repair_core_defences(self, game_state):
        """
        Rebuilt any destroyed core defences that were built in the siphon_build_core_defences function
        In order of importancy
        """
        gamelib.debug_write("Attempting to rebuild core defenses")
        game_state.attempt_spawn(WALL, self.frontline_wall_locations)
        game_state.attempt_spawn(WALL, self.pathing_wall_locations)
        game_state.attempt_spawn(TURRET, self.frontline_turrent_locations)
        game_state.attempt_spawn(WALL, self.side_wall_locations)
        game_state.attempt_upgrade(self.frontline_wall_locations)

    def siphon_build_reactive_defense(self, game_state):
        """
        If sustained losses in last turn:
        Enhance defences based on where the enemy scored on us from.
        Focus on enhancing the majority losses side

        Else:
        Enhance defences based on predetermined locations
        """
        lossesPos = self.scored_on_locations
        gamelib.debug_write("scored_on_locations at {}".format(lossesPos))
        if(len(lossesPos) == 0):
            # Enhance based on predetermined locations
            gamelib.debug_write("No losses")
            self.siphon_enhance_defences(game_state, 0)
        else:
            rightCount = 0
            leftCount = 0
            for location in lossesPos:
                if(location[0] > 13):
                    rightCount += 1
                else:
                    leftCount += 1
            if(rightCount > leftCount):
                # Focus enhancement on right side
                gamelib.debug_write("Right side sustained major losses")
                self.siphon_enhance_defences(game_state, 1)
            else:
                # Focus enhancement on left side
                gamelib.debug_write("Left side sustained major losses")
                self.siphon_enhance_defences(game_state, 2)

    def siphon_enhance_defences(self, game_state, side: int):
        """
        Side:
        0 = Balanced enhancement
        1 = Right side focused enhancement
        2 = Left side focused enhancement
        """
        if (side == 0):
            gamelib.debug_write("Balanced enhancement")
        elif (side == 1):
            gamelib.debug_write("Right side focused enhancement")
        else:
            gamelib.debug_write("Left side focused enhancement")

        game_state.attempt_upgrade(self.frontline_wall_locations)
        game_state.attempt_upgrade(self.siphon_extract_side_locations(
            self.side_wall_locations, side))
        if(side == 0):
            game_state.attempt_spawn(SUPPORT, self.support_locations)
        game_state.attempt_spawn(TURRET, self.siphon_extract_side_locations(
            self.side_turrent_locations, side))
        game_state.attempt_upgrade(self.siphon_extract_side_locations(
            self.frontline_turrent_locations, side))
        game_state.attempt_spawn(TURRET,
                                 self.siphon_extract_side_locations(self.frontline_turrent_extension1_locations, side))
        game_state.attempt_upgrade(
            self.siphon_extract_side_locations(self.side_turrent_locations, side))
        game_state.attempt_upgrade(
            self.siphon_extract_side_locations(self.frontline_turrent_extension1_locations, side))
        game_state.attempt_spawn(WALL, self.siphon_extract_side_locations(
            self.side_wall_extension1_locations, side))
        game_state.attempt_spawn(TURRET, self.siphon_extract_side_locations(
            self.frontline_turrent_extension2_locations, side))
        game_state.attempt_upgrade(self.support_locations)
        game_state.attempt_upgrade(self.siphon_extract_side_locations(
            self.side_wall_extension1_locations, side))
        game_state.attempt_upgrade(self.siphon_extract_side_locations(
            self.frontline_turrent_extension2_locations, side))
        game_state.attempt_spawn(SUPPORT, self.support_locations)

    def siphon_extract_side_locations(self, locationList, side: int):
        """
        Side:
        0 = Side neutral
        1 = Right side
        2 = Left side

        Given a list of locations, return a list of locations on the given side of the map
        """
        if (side == 0):
            return locationList
        elif (side == 1):
            return [location for location in locationList if location[0] > 13]
        elif (side == 2):
            return [location for location in locationList if location[0] < 13]

    def starter_strategy(self, game_state):
        """
        For defense we will use a spread out layout and some interceptors early on.
        We will place turrets near locations the opponent managed to score on.
        For offense we will use long range demolishers if they place stationary units near the enemy's front.
        If there are no stationary units to attack in the front, we will send Scouts to try and score quickly.
        """
        # First, place basic defenses
        self.build_defences(game_state)
        # Now build reactive defenses based on where the enemy scored
        self.build_reactive_defense(game_state)

        # If the turn is less than 5, stall with interceptors and wait to see enemy's base
        if game_state.turn_number < 5:
            self.stall_with_interceptors(game_state)
        else:
            # Now let's analyze the enemy base to see where their defenses are concentrated.
            # If they have many units in the front we can build a line for our demolishers to attack them at long range.
            if self.detect_enemy_unit(game_state, unit_type=None, valid_x=None, valid_y=[14, 15]) > 10:
                self.demolisher_line_strategy(game_state)
            else:
                # They don't have many units in the front so lets figure out their least defended area and send Scouts there.

                # Only spawn Scouts every other turn
                # Sending more at once is better since attacks can only hit a single scout at a time
                if game_state.turn_number % 2 == 1:
                    # To simplify we will just check sending them from back left and right
                    scout_spawn_location_options = [[13, 0], [14, 0]]
                    best_location = self.least_damage_spawn_location(
                        game_state, scout_spawn_location_options)
                    game_state.attempt_spawn(SCOUT, best_location, 1000)

                # Lastly, if we have spare SP, let's build some supports
                support_locations = [[13, 2], [14, 2], [13, 3], [14, 3]]
                game_state.attempt_spawn(SUPPORT, support_locations)

    def build_defences(self, game_state):
        """
        Build basic defenses using hardcoded locations.
        Remember to defend corners and avoid placing units in the front where enemy demolishers can attack them.
        """
        # Useful tool for setting up your base locations: https://www.kevinbai.design/terminal-map-maker
        # More community tools available at: https://terminal.c1games.com/rules#Download

        # Place turrets that attack enemy units
        turret_locations = [[0, 13], [27, 13], [
            8, 11], [19, 11], [13, 11], [14, 11]]
        # attempt_spawn will try to spawn units if we have resources, and will check if a blocking unit is already there
        game_state.attempt_spawn(TURRET, turret_locations)

        # Place walls in front of turrets to soak up damage for them
        wall_locations = [[8, 12], [19, 12]]
        game_state.attempt_spawn(WALL, wall_locations)
        # upgrade walls so they soak more damage
        game_state.attempt_upgrade(wall_locations)

    def build_reactive_defense(self, game_state):
        """
        This function builds reactive defenses based on where the enemy scored on us from.
        We can track where the opponent scored by looking at events in action frames 
        as shown in the on_action_frame function
        """
        for location in self.scored_on_locations:
            # Build turret one space above so that it doesn't block our own edge spawn locations
            build_location = [location[0], location[1]+1]
            game_state.attempt_spawn(TURRET, build_location)

    def stall_with_interceptors(self, game_state):
        """
        Send out interceptors at random locations to defend our base from enemy moving units.
        """
        # We can spawn moving units on our edges so a list of all our edge locations
        friendly_edges = game_state.game_map.get_edge_locations(
            game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)

        # Remove locations that are blocked by our own structures
        # since we can't deploy units there.
        deploy_locations = self.filter_blocked_locations(
            friendly_edges, game_state)

        # While we have remaining MP to spend lets send out interceptors randomly.
        while game_state.get_resource(MP) >= game_state.type_cost(INTERCEPTOR)[MP] and len(deploy_locations) > 0:
            # Choose a random deploy location.
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]

            game_state.attempt_spawn(INTERCEPTOR, deploy_location)
            """
            We don't have to remove the location since multiple mobile 
            units can occupy the same space.
            """

    def demolisher_line_strategy(self, game_state):
        """
        Build a line of the cheapest stationary unit so our demolisher can attack from long range.
        """
        # First let's figure out the cheapest unit
        # We could just check the game rules, but this demonstrates how to use the GameUnit class
        stationary_units = [WALL, TURRET, SUPPORT]
        cheapest_unit = WALL
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, game_state.config)
            if unit_class.cost[game_state.MP] < gamelib.GameUnit(cheapest_unit, game_state.config).cost[game_state.MP]:
                cheapest_unit = unit

        # Now let's build out a line of stationary units. This will prevent our demolisher from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.
        for x in range(27, 5, -1):
            game_state.attempt_spawn(cheapest_unit, [x, 11])

        # Now spawn demolishers next to the line
        # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
        game_state.attempt_spawn(DEMOLISHER, [24, 10], 1000)

    def least_damage_spawn_location(self, game_state, location_options):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path the unit will take then checks locations on that path to 
        estimate the path's damage risk.
        """
        damages = []
        # Get the damage estimate each path will take
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy turrets that can attack each location and multiply by turret damage
                damage += len(game_state.get_attackers(path_location, 0)) * \
                    gamelib.GameUnit(TURRET, game_state.config).damage_i
            damages.append(damage)

        # Now just return the location that takes the least damage
        return location_options[damages.index(min(damages))]

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x=None, valid_y=None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
                        total_units += 1
        return total_units

    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at in json-docs.html in the root of the Starterkit.
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly,
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                gamelib.debug_write(
                    "All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
