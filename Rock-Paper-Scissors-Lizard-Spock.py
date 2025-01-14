class Participant:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.choice = ""

    def choose(self):
        choices = ["rock", "paper", "scissor", "lizard", "spock"]
        while True:
            self.choice = input(f"{self.name}, select rock, paper, scissor, lizard, or spock: ").lower()
            if self.choice in choices:
                break
            print("Invalid choice. Please choose again.")
        print(f"{self.name} selects {self.choice}")

    def toNumericalChoice(self):
        switcher = {
            "rock": 0,
            "paper": 1,
            "scissor": 2,
            "lizard": 3,
            "spock": 4
        }
        return switcher[self.choice]

    def incrementPoint(self):
        self.points += 1


class GameRound:
    def __init__(self, p1, p2):
        self.rules = [
            [0, -1, 1, 1, -1],
            [1, 0, -1, -1, 1],
            [-1, 1, 0, 1, -1],
            [-1, 1, -1, 0, 1],
            [1, -1, 1, -1, 0]
        ]

        p1.choose()
        p2.choose()

        result = self.compareChoices(p1, p2)
        print(f"Round resulted in a {self.getResultAsString(result)}")

        if result > 0:
            p1.incrementPoint()
        elif result < 0:
            p2.incrementPoint()
        else:
            print("No points for anybody.")

    def compareChoices(self, p1, p2):
        return self.rules[p1.toNumericalChoice()][p2.toNumericalChoice()]

    def getResultAsString(self, result):
        res = {
            0: "draw",
            1: "win",
            -1: "loss"
        }
        return res[result]


class Game:
    def __init__(self):
        self.endGame = False
        self.participant = Participant("Player 1")
        self.secondParticipant = Participant("Player 2")

    def start(self):
        while not self.endGame:
            GameRound(self.participant, self.secondParticipant)
            self.checkEndCondition()

    def checkEndCondition(self):
        answer = input("Continue game? (y/n): ").lower()
        if answer == 'y':
            return
        else:
            print(f"Game ended, {self.participant.name} has {self.participant.points} points, and {self.secondParticipant.name} has {self.secondParticipant.points} points.")
            self.determineWinner()
            self.endGame = True

    def determineWinner(self):
        if self.participant.points > self.secondParticipant.points:
            print(f"Winner is {self.participant.name}")
        elif self.participant.points < self.secondParticipant.points:
            print(f"Winner is {self.secondParticipant.name}")
        else:
            print("It's a Draw")


if __name__ == "__main__":
    game = Game()
    game.start()
