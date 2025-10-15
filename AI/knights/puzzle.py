from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


A_help = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))
B_help = And(Or(BKnight, BKnave), Not(And(BKnight, BKnave)))
C_help = And(Or(CKnight, CKnave), Not(And(CKnight, CKnave)))
# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    A_help,
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    A_help, B_help,
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Same = Or(And(AKnight, BKnight), And(AKnave, BKnave))
Different = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    A_help, B_help,
    Implication(AKnight, Same),
    Implication(AKnave, Not(Same)),
    Implication(BKnight, Different),
    Implication(BKnave, Not(Different))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

ASaidKnight = Symbol("A said 'I am a Knight'")
ASaidKnave = Symbol("A said 'I am a Knive'")
knowledge3 = And(
   A_help, B_help, C_help,
   Or(ASaidKnight, ASaidKnave),
   Not(And(ASaidKnight, ASaidKnave)),

   Implication(AKnight, Or(And(ASaidKnight, AKnight), And(ASaidKnave, AKnave))),
   Implication(AKnave, Or(And(ASaidKnight, Not(AKnight)), And(ASaidKnave, Not(AKnave)))),

   Implication(BKnight, ASaidKnave),
   Implication(BKnave, Not(ASaidKnave)),
   Implication(BKnight, CKnave),
   Implication(BKnave, Not(CKnave)),

   Implication(CKnight, AKnight),
   Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
