import argparse
from CFP import CellFormationParser, CFPSolution


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Solving CFP with Variable Neighborhood Search metaheuristic')
    parser.add_argument('problem_file', type=str, help='Problem file')
    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()
    problem = CellFormationParser(args.problem_file).parse()
    sol = CFPSolution(problem)
    print(problem)
    print(sol)
    print(sol.obj_func)
