from languages.asp.asp_input_program import ASPInputProgram


from embasp.base.output import Output
from embasp.languages.asp.asp_input_program import ASPInputProgram
from embasp.languages.asp.asp_mapper import ASPMapper
from embasp.platforms.desktop.desktop_handler import DesktopHandler
from embasp.specializations.dlv2.desktop.dlv2_desktop_service import \
    DLV2DesktopService

import os

class Player():

    @staticmethod
    def init() -> None:
        file_name = "ai_asp.asp"
        current_script_path = os.path.abspath(__file__).removesuffix(os.path.basename(__file__))
        file_path = os.path.join(current_script_path, file_name)

        Player.solver = ASPInputProgram()
        Player.handler = DesktopHandler(DLV2DesktopService("executables\dlv2.exe"))

        Player.loadedProgram = ""

        # Load the ASP program from the file
        with open(file_path, "r") as f:
            for l in f.readlines():
                if l != "\n" and l != "" and l != "%":
                    Player.loadedProgram += l

        Player.atoms = ""
                    

    def __getAtoms() -> str:
        atoms = Player.atoms

        Player.atoms = ""
        return atoms
    
    @staticmethod
    def addCard(level, pos, value) -> None:
        _id = level * 10 + pos
        Player.atoms += f"cardsEnabled({_id},{value}). idPosLev({_id}, {level}, {pos}).\n"

    @staticmethod
    def addPileCard(value) -> None:
        _id = 999 # -1 * 10 + 0
        Player.atoms += f"cardsEnabled({_id},{value}). isPileCard({_id}). idPosLev({_id}, -1,  0).\n"
        
    
    @staticmethod
    def get_next_actions() -> list:
        Player.solver.clear_all()

        atoms = Player.__getAtoms()

        Player.solver.add_program(atoms)
        Player.solver.add_program(Player.loadedProgram)

        Player.handler.add_program(Player.solver)


        #result = Player.handler.start_sync().get_optimal_answer_sets() 
        result = Player.handler.start_sync().get_answer_sets()

        if len(result) == 0:
            return []

       # return result[0].get_answer_set()
        return result
    
    @staticmethod
    def get_next_actionsOptimal() -> list:
        Player.solver.clear_all()

        atoms = Player.__getAtoms()

        Player.solver.add_program(atoms)
        Player.solver.add_program(Player.loadedProgram)

        Player.handler.add_program(Player.solver)


        result = Player.handler.start_sync().get_optimal_answer_sets()


        if len(result) == 0:
            return []

        return result[0].get_answer_set()
