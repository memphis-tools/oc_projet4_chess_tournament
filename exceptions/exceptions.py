class AttributeDoesNotExistsException(Exception):
    pass


class BlankFieldException(Exception):
    pass


class ClubIdDoesNotExistsException(Exception):
    pass


class ClubIdAlreadyExistsException(Exception):
    pass


class ClubIdExistsInTournamentException(Exception):
    pass


class ClubStatusNotActiveException(Exception):
    pass


class IneAlreadyExistsException(Exception):
    pass


class IneCanNotBeUpdateException(Exception):
    pass


class IneDoesNotExistsException(Exception):
    pass


class IneDoesNotExistsInTournament(Exception):
    pass


class IneDoesNotRespectPatternException(Exception):
    pass


class IneExistsInTournamentException(Exception):
    pass


class MatchDoesNotExistsException(Exception):
    pass


class MatchIsNotScoredException(Exception):
    pass


class NoClubsRecordedException(Exception):
    pass


class NotDigitException(Exception):
    pass


class NoPlayersRecordedException(Exception):
    pass


class OddPlayersListNumberException(Exception):
    pass


class PlayerStatusDoesNotExistsException(Exception):
    pass


class PlayerStatusNotActiveException(Exception):
    pass


class RoundIdAlreadyExistsException(Exception):
    pass


class RoundIdDoesNotExistsException(Exception):
    pass


class ScoreSetupStoppedException(Exception):
    pass


class StatusDoesNotExistsException(Exception):
    pass


class TournamentCancelledException(Exception):
    pass


class TournamentEndedException(Exception):
    pass


class TournamentIdAlreadyExistsException(Exception):
    pass


class TournamentIdDoesNotExistsException(Exception):
    pass


class TournamentNbRoundNotDigit(Exception):
    pass


class TournamentStatusNotInProgressException(Exception):
    pass


class UpdatePlayersScoresException(Exception):
    pass
