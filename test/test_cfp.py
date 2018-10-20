import numpy as np
import pytest

from CFP import *


@pytest.fixture
def problem():
    return CellFormationParser('test.txt').parse()


def test_init_solution(problem):
    sol = CFPSolution(problem)
    assert np.all(sol.parts == 1) and np.all(sol.machines == 1)


def test_exact_solution(problem):
    sol = CFPSolution(problem, [1, 2, 3, 3, 1, 1], [3, 1, 2, 2, 1, 3])
    assert sol.obj_func == 1


def test_feasible_solution(problem):
    sol = CFPSolution(problem, [1, 2, 3, 3, 1, 1], [3, 1, 2, 2, 1, 3])
    assert sol.is_feasible


def test_non_feasible_solution(problem):
    sol = CFPSolution(problem, [2, 1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1])
    assert not sol.is_feasible


def test_eq_solutions(problem):
    sol_a, sol_b = CFPSolution(problem), CFPSolution(problem)
    assert sol_a == sol_b


def test_lt_solution(problem):
    sol_a, sol_b = CFPSolution(problem, [1, 2, 3, 3, 1, 1], [3, 1, 2, 2, 1, 3]), CFPSolution(problem)
    assert sol_b < sol_a


def test_sol_copy(problem):
    sol = CFPSolution(problem)
    sol_cp = sol.copy()
    sol_cp.machines = [1, 2, 3, 3, 1, 1]
    sol_cp.parts = [3, 1, 2, 2, 1, 3]
    assert sol != sol_cp
