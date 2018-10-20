from copy import copy
from functools import total_ordering

import numpy as np


class CellFormationProblem:
    def __init__(self, machines_part: np.ndarray):
        self.machines_part: np.ndarray = machines_part
        self.total_ones = np.sum(self.machines_part)

    def __repr__(self):
        return str(self.machines_part)


@total_ordering
class CFPSolution:
    def __init__(self, problem: CellFormationProblem, machines=None, parts=None):
        self.problem: CellFormationProblem = problem
        self.machines = machines
        self.parts = parts
        if not self.machines or not self.parts:
            self.parts = np.ones(self.problem.machines_part.shape[1])
            self.machines = np.ones(self.problem.machines_part.shape[0])

    @property
    def values_in(self):
        zeros, ones = 0, 0
        for i, machine in enumerate(self.machines):
            for j, part in enumerate(self.parts):
                if machine == part:
                    if self.problem.machines_part[i, j] == 0:
                        zeros += 1
                    else:
                        ones += 1
        return zeros, ones

    @property
    def is_feasible(self):
        clusters = {c: 0 for c in np.unique([self.parts, self.machines])}
        for i, machine in enumerate(self.machines):
            for j, part in enumerate(self.parts):
                if machine == part:
                    clusters[machine] += self.problem.machines_part[i, j]
        return all([clusters[c] > 1 for c in clusters])

    @property
    def obj_func(self):
        zeros_in, ones_in = self.values_in
        return ones_in / (self.problem.total_ones + zeros_in)

    def copy(self):
        return copy(self)

    def __copy__(self):
        return type(self)(self.problem, self.machines.tolist(), self.parts.tolist())

    def __gt__(self, other):
        return self.obj_func > other.obj_func

    def __eq__(self, other):
        return self.obj_func == other.obj_func

    def __repr__(self):
        return f"{self.machines}\n{self.parts}"
