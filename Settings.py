
MULTIPLIER_TYPES = ["DLS",  # Double letter score
                    "TLS",  # Triple letter score
                    "DWS",  # Double word score
                    "TWS"]  # Triple word score

CELL_TYPES = MULTIPLIER_TYPES + ["STANDARD"]

# RGB color codes
MULTIPLIER_COLORS = {"DLS": (30, 144, 255),
                     "TLS": (15, 82, 186),
                     "DWS": (255, 87, 51),
                     "TWS": (139, 0, 0),
                     "STANDARD": (136, 136, 136)}

# Grid entries
MULTIPLIER_ARRANGEMENT = {"DLS": [(0, 3), (0, 11),
                                  (2, 6), (2, 8),
                                  (3, 0), (3, 7), (3, 14),
                                  (6, 2), (6, 6), (6, 8), (6, 12),
                                  (7, 3), (7, 11),
                                  (8, 2), (8, 6), (8, 8), (8, 12),
                                  (11, 0), (11, 7), (11, 14),
                                  (12, 6), (12, 8),
                                  (14, 3), (14, 11)],

                          "TLS": [(1, 5), (1, 9),
                                  (5, 1), (5, 5), (5, 9), (5, 13),
                                  (9, 1), (9, 5), (9, 9), (9, 13),
                                  (13, 5), (13, 9)],

                          "DWS": [(1, 1), (1, 13),
                                  (2, 2), (2, 12),
                                  (3, 3), (3, 11),
                                  (4, 4), (4, 10),
                                  (10, 4), (10, 10),
                                  (11, 3), (11, 11),
                                  (12, 2), (12, 12),
                                  (13, 1), (13, 13)],

                          "TWS": [(0, 0), (0, 7), (0, 14),
                                  (7, 0), (7, 7), (7, 14),
                                  (14, 0), (14, 7), (14, 14)]}

ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
            "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
            "W", "X", "Y", "Z", " "]

# Using https://en.wikipedia.org/wiki/Scrabble_letter_distributions
LETTER_DISTRIBUTION = {
                       " ": 2,                                                                           # 0 points
                       "E": 12, "A": 9, "I": 9, "O": 8, "N": 6, "R": 6, "T": 6, "L": 4, "S": 4, "U": 4,  # 1 point
                       "D": 4, "G": 3,                                                                   # 2 points
                       "B": 2, "C": 2, "M": 2, "P": 2,                                                   # 3 points
                       "F": 2, "H": 2, "V": 2, "W": 2, "Y": 2,                                           # 4 points
                       "K": 1,                                                                           # 5 points
                       "J": 1, "X": 1,                                                                   # 8 points
                       "Q": 1, "Z": 1,                                                                   # 10 points
                       }

POINT_DISTRIBUTION = {
                      " ": 0,
                      "E": 1, "A": 1, "I": 1, "O": 1, "N": 1, "R": 1, "T": 1, "L": 1, "S": 1, "U": 1,
                      "D": 2, "G": 2,
                      "B": 3, "C": 3, "M": 3, "P": 3,
                      "F": 4, "H": 4, "V": 4, "W": 4, "Y": 4,
                      "K": 5,
                      "J": 8, "X": 8,
                      "Q": 10, "Z": 10,
                        }