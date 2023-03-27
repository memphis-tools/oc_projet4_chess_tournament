from colorama import Fore, Style
import view
from clients.console import Console
from exceptions import exceptions

if __name__ == "__main__":
    while True:
        try:
            console = Console(view)
            console.get_root_menu()
        except exceptions.AttributeDoesNotExistsException:
            print(f"{Fore.RED}{Style.BRIGHT}ATTRIBUT N'EXISTE PAS{Style.RESET_ALL}")
        except exceptions.BlankFieldException:
            print(f"{Fore.RED}{Style.BRIGHT}SAISIE VIDE NON AUTORISEE{Style.RESET_ALL}")
        except exceptions.ClubIdDoesNotExistsException:
            print(f"{Fore.RED}{Style.BRIGHT}PAS DE CLUB AVEC CET ID{Style.RESET_ALL}")
        except exceptions.ClubIdAlreadyExistsException:
            print(f"{Fore.RED}{Style.BRIGHT}UN CLUB EXISTE DEJA AVEC CET ID{Style.RESET_ALL}")
        except exceptions.ClubIdExistsInTournamentException:
            print(f"{Fore.RED}{Style.BRIGHT}CLUB ID CONNU DANS TOURNOI(S), ARCHIVAGE DU CLUB{Style.RESET_ALL}")
        except exceptions.ClubStatusNotActiveException:
            print(f"{Fore.RED}{Style.BRIGHT}LE CLUB DOIT ETRE ACTIF POUR QUE LE JOUEUR LE SOIT{Style.RESET_ALL}")
        except exceptions.IneDoesNotExistsException:
            print(f"{Fore.RED}{Style.BRIGHT}AUCUN JOUEUR AVEC CET INE{Style.RESET_ALL}")
        except exceptions.IneAlreadyExistsException:
            print(f"{Fore.RED}{Style.BRIGHT}UN JOUEUR EXISTE DEJA AVEC CET INE{Style.RESET_ALL}")
        except exceptions.IneCanNotBeUpdateException:
            print(f"{Fore.RED}{Style.BRIGHT}INE EST NON MODIFIABLE{Style.RESET_ALL}")
        except exceptions.IneDoesNotExistsInTournament:
            print(f"{Fore.RED}{Style.BRIGHT}INE ABSENT DU TOURNOI{Style.RESET_ALL}")
        except exceptions.IneDoesNotRespectPatternException:
            print(f"{Fore.RED}{Style.BRIGHT}INE SAISI NE RESPECTE PAS LE PATTERN PREVU{Style.RESET_ALL}")
        except exceptions.IneExistsInTournamentException:
            print(f"{Fore.RED}{Style.BRIGHT}INE(S) CONNU(S) DANS UN TOURNOI, ARCHIVAGE DE JOUEUR{Style.RESET_ALL}")
        except exceptions.MatchDoesNotExistsException:
            print(f"{Fore.RED}{Style.BRIGHT}MATCH N'EXISTE PAS/PLUS{Style.RESET_ALL}")
        except exceptions.NoClubsRecordedException:
            print(f"{Fore.RED}{Style.BRIGHT}AUCUN CLUB ENREGISTRE ACTUELLEMENT{Style.RESET_ALL}")
        except exceptions.NoPlayersRecordedException:
            print(f"{Fore.RED}{Style.BRIGHT}AUCUN JOUEUR ENREGISTRE ACTUELLEMENT{Style.RESET_ALL}")
        except exceptions.NotDigitException:
            print(f"{Fore.RED}{Style.BRIGHT}SAISIE AUTRE QUE CHIFFRE/NOMBRE NON AUTORISEE{Style.RESET_ALL}")
        except exceptions.RoundIdDoesNotExistsException:
            print(f"{Fore.RED}{Style.BRIGHT}PAS DE ROUND AVEC CET ID{Style.RESET_ALL}")
        except exceptions.RoundIdAlreadyExistsException:
            print(f"{Fore.RED}{Style.BRIGHT}UN ROUND EXISTE DEJA AVEC CET ID{Style.RESET_ALL}")
        except exceptions.ScoreSetupStoppedException:
            print(f"{Fore.RED}{Style.BRIGHT}SAISIE ROUND DU TOURNOI INTERROMPUE{Style.RESET_ALL}")
        except exceptions.StatusDoesNotExistsException:
            print(f"{Fore.RED}{Style.BRIGHT}STATUT N'EXISTE PAS{Style.RESET_ALL}")
        except exceptions.TournamentCancelledException:
            print(f"{Fore.RED}{Style.BRIGHT}TOURNOI ANNULE{Style.RESET_ALL}")
        except exceptions.TournamentEndedException:
            print(f"{Fore.RED}{Style.BRIGHT}TOURNOI FINI, PAS DE ROUND A METTRE A JOUR{Style.RESET_ALL}")
        except exceptions.TournamentIdAlreadyExistsException:
            print(f"{Fore.RED}{Style.BRIGHT}UN TOURNOI EXISTE DEJA AVEC CET ID{Style.RESET_ALL}")
        except exceptions.TournamentIdDoesNotExistsException:
            print(f"{Fore.RED}{Style.BRIGHT}PAS DE TOURNOI AVEC CET ID{Style.RESET_ALL}")
        except exceptions.TournamentStatusNotInProgressException:
            print(f"{Fore.RED}{Style.BRIGHT}TOURNOI N'EST PAS AU STATUT 'ACTIVE/IN PROGRESS'{Style.RESET_ALL}")
        except exceptions.UpdatePlayersScoresException:
            print(f"{Fore.RED}{Style.BRIGHT}PAUSE DANS SAISIE SCORES{Style.RESET_ALL}")
