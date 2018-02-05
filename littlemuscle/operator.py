from enum import Enum, unique

@unique
class Operator(Enum):
    # Submodel Execution Loop
    F_INIT = 'f_init'
    O_I = 'O_i'
    S = 'S'
    B = 'B'
    O_F = 'O_f'

    # Mappers
    M = 'M'

    def may_receive(self) -> bool:
        receiving_operators = [Operator.F_INIT, Operator.S, Operator.B]
        return self in receiving_operators

    def may_send(self) -> bool:
        sending_operators = [Operator.O_I, Operator.O_F]
        return self in sending_operators



