class ConsoleMenu:
    root_menu = [
        ("0", "QUITTER APPLICATION", "QUIT"),
        ("1", "CLUB", "CLUB"),
        ("2", "JOUEUR", "PLAYER"),
        ("3", "TOURNOI", "TOURNAMENT"),
        ("4", "RAPPORT", "REPORT"),
    ]

    cruda_menu = [
        ("0", "RETOUR ARRIERE"),
        ("1", "VOIR"),
        ("2", "CREER"),
        ("3", "SUPPRIMER"),
        ("4", "MODIFIER"),
    ]

    one_or_many_menu_get = [
        ("0", "RETOUR ARRIERE"),
        ("1", "RECHERCHER UN"),
        ("2", "RECHERCHER TOUS"),
    ]

    one_or_many_player_menu_get = [
        ("0", "RETOUR ARRIERE"),
        ("1", "RECHERCHER UN JOUEUR"),
        ("2", "RECHERCHER TOUS LES JOUEURS"),
        ("3", "RECHERCHER TOUS LES JOUEURS D'UN CLUB"),
    ]

    one_or_many_menu_delete = [
        ("0", "RETOUR ARRIERE"),
        ("1", "SUPPRIMER UN"),
        ("2", "SUPPRIMER TOUS"),
    ]

    update_tournament_menu = [
        ("0", "RETOUR ARRIERE"),
        ("1", "MODIFIER INFORMATIONS"),
        ("2", "ACTUALISER TOURS/MATCHS"),
    ]

    odd_tournament_players_list_menu = [
        ("0", "ANNULER TOURNOI"),
        ("1", "AJOUTER JOUEUR"),
        ("2", "RETIRER JOUEUR"),
    ]

    quit_menu = [
        ("0", "RETOUR ARRIERE"),
        ("1", "QUITTER"),
    ]

    report_menu = [
        ("0", "RETOUR ARRIERE"),
        ("1", "LISTE DE TOUS LES JOUEURS PAR ORDRE ALPHABETIQUE"),
        ("2", "LISTE DE TOUS LES TOURNOIS"),
        ("3", "NOM ET DATES D'UN TOURNOI DONNE"),
        ("4", "LISTE DES JOUEURS DU TOURNOI PAR ORDRE ALPHABETIQUE"),
        ("5", "LISTE DE TOUS LES TOURS DU TOURNOI ET DE TOUS LES MATCHS DU TOUR"),
    ]

    report_output_format = [
        ("0", "RETOUR ARRIERE"),
        ("1", "TEXT"),
        ("2", "HTML"),
    ]

    yes_no_menu = [
        ("0", "RETOUR ARRIERE"),
        ("1", "OUI"),
        ("2", "NON"),
    ]

    def display_menu(self, menu_name):
        for i in eval(f"ConsoleMenu.{menu_name}"):
            print(f"{i[0]}: {i[1]}")

    def get_caption(self, choice, caption_type="human"):
        if caption_type == "computer":
            return eval(f"ConsoleMenu.root_menu[{choice}][2]")
        return eval(f"ConsoleMenu.root_menu[{choice}][1]")
