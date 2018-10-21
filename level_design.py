
# LEVEL DESIGN ELEMENTS:

# U - User (player)
# B - Bot
# E - Enemy
# R - Rock (solid block)
# P - Platform (with random time [1,9])
# [number] - Platform with this much time
# V, ^, >, < - Spike (and direction its facing)
# W - Water
# F - Finish

levels = [
    # [
    # "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
    # "R                                                                                                       R",
    # "R                                                                                                       R",
    # "R                                                                                                       R",
    # "R            RRRRRRRR                     RRR                  RRRR                                  RRRR",
    # "R            VVVVVVVV                     VVV                  VVVV                      RR          VVVR",
    # "R                                                                                  ^     VV             R",
    # "RB                          ^         ^        <R    E     0^        ^^^0  E       0          ^   ^    FR",
    # "R011111111111111111111111111R111111111R111111111R11111111111111111111RRR1111111111111111111111R111R11111R",
    # "R^^^^^^^^^^^^^^^^^^^^^^^^^^^R^^^^^^^^^R^^^^^^^^^R^^^^^^^^^^^^^^^^^^^^RRR^^^^^^^^^^^^^^^^^^^^^^R^^^R^^^^^R",
    # "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",],
    # [
    # "               RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
    # "               R                                                                        R",
    # "               R                                                                        R",
    # "               R                                                                        R",
    # "               R                                                                        R",
    # "               R                               RRRR                                  RRRR",
    # "               R                               VVVV                      RR          VVVR",
    # "               R                                                   ^     VV             R",
    # "               RB     ^         ^           ^        ^^^0  E       0          ^   ^    FR",
    # "               R1111111111111111111111111111111111111RRR1111111111111111111111R111R11111R",
    # "               R^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^RRR^^^^^^^^^^^^^^^^^^^^^^R^^^R^^^^^R",
    # "               RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",],
    [
    "               RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
    "               R                                                                        R",
    "               R                                                                        R",
    "               R                                                                        R",
    "               R                                                                        R",
    "               R          RRR                  RRRR                      RR          RRRR",
    "               R          VVV                  VVVV                      VV          VVVR",
    "               R                                                   ^                    R",
    "               RB     ^        <R    E     0^        ^^^0          0                   FR",
    "               R111111R111111111R11111111111111111111RRR1111111111111111111111R111R11111R",
    "               R^^^^^^R^^^^^^^^^R^^^^^^^^^^^^^^^^^^^^RRR^^^^^^^^^^^^^^^^^^^^^^R^^^R^^^^^R",
    "               RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",]
]

