import argparse
import os

from CFP import CellFormationParser, GeneralVNS, CFPSolution


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Solving CFP with Variable Neighborhood Search metaheuristic')
    parser.add_argument('problem_file', type=str, help='Problem file')
    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()
    problem = CellFormationParser(args.problem_file).parse()

    print(problem)

    sol = CFPSolution(problem)
    print(sol)
    print(sol.objective_function)
    sol = GeneralVNS(problem).solve()
    if not os.path.exists('results/'):
        os.mkdir('results')
    with open(f"results/{os.path.basename(args.problem_file).split('.')[0]}.sol", "w") as f:
        f.write(str(sol))
