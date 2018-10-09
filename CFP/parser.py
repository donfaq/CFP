import os
import numpy as np
from CFP.entities import CellFormationProblem


class CellFormationParser:
    def __init__(self, problem_path):
        assert os.path.exists(problem_path), "Problem file does not exist"
        self.problem_path = problem_path

    def parse(self):
        with open(self.problem_path, 'r') as f:
            machines_num, parts_num = list(map(int, f.readline().split()))
            machine_part = np.zeros((machines_num, parts_num), dtype=int)
            for line in f:
                line = list(map(int, line.split()))
                machine, parts = line[0] - 1, np.array(line[1:]) - 1
                machine_part[machine, parts] = 1
        return CellFormationProblem(machine_part)
