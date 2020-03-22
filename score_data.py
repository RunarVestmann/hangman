class ScoreData:
    __slots__ = 'username', 'score', 'wins', 'losses', 'date'
    def __init__(self, username, score, wins, losses, date):
        self.username = username
        self.score = score
        self.wins = wins
        self.losses = losses
        self.date = date