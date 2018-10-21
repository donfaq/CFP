from CFP import CellFormationProblem, CFPSolution
import numpy as np
from itertools import combinations


class GeneralVNS:
    def __init__(self, problem: CellFormationProblem):
        self.problem = problem

    def _divide_clusters(self, solution: CFPSolution):
        res = solution.copy()
        is_feasible = False
        while not is_feasible:
            res = solution.copy()
            new_cluster = max(res.clusters) + 1
            random_machines = np.random.choice(range(len(res.machines)),
                                               np.random.randint(0, int(res.machines.shape[0] / 2)),
                                               replace=False)
            res.machines[random_machines] = new_cluster
            random_parts = np.random.choice(range(len(res.parts)),
                                            np.random.randint(0, int(res.parts.shape[0] / 2)),
                                            replace=False)
            res.parts[random_parts] = new_cluster
            is_feasible = res.is_feasible
        return res

    def _merge_clusters(self, solution: CFPSolution):
        res = solution.copy()
        is_feasible = False
        while not is_feasible:
            a, b = np.random.choice(solution.clusters, 2, replace=False).tolist()
            res.machines[res.machines == b] = a
            res.parts[res.parts == b] = a
            is_feasible = res.is_feasible
        return res

    def _swap_machines(self, sol: CFPSolution):
        best = sol.copy()
        for a, b in combinations(range(len(sol.machines)), 2):
            new_sol = best.copy()
            new_sol.machines[[a, b]] = new_sol.machines[[b, a]]
            if new_sol.is_feasible and new_sol > best:
                best = new_sol
        return best

    def _swap_parts(self, sol: CFPSolution):
        best = sol.copy()
        for a, b in combinations(range(len(sol.parts)), 2):
            new_sol = best.copy()
            new_sol.parts[[a, b]] = new_sol.parts[[b, a]]
            if new_sol.is_feasible and new_sol > best:
                best = new_sol
        return best

    def solve(self):
        shaking_functions = [self._divide_clusters, self._merge_clusters]
        vnd_functions = [self._swap_parts, self._swap_machines]
        best_sol = CFPSolution(self.problem)
        not_upd = 0
        while not_upd <= 10:
            not_upd += 1
            k = 0
            while k < len(shaking_functions):
                new_sol = shaking_functions[k](best_sol.copy())
                l = 0
                while l < len(vnd_functions):
                    opt_new_sol = vnd_functions[l](new_sol.copy())
                    l += 1
                    if opt_new_sol > new_sol:
                        new_sol = opt_new_sol
                        l = 0
                k += 1
                if new_sol > best_sol:
                    best_sol = new_sol
                    not_upd = 0
                    k = 0
                    print(best_sol, '\n', best_sol.objective_function)
        return best_sol
