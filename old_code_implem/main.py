from src.domain.services.solver import Solver

if __name__ == "__main__":
    files = [
        # "test.easy.csv",
        # "test.easy_2.csv",
        # "test.medium.csv",
        # "test.hard.csv",
        # "test.hard_2.csv",
        # "test.devil.csv",
        # "test.devil_2.csv",
        # "test.devil_3.csv",
        # "test.devil_4.csv",
        # "test.hell.csv",
        # "test.mom.csv"
    ]
    for file in files:
        print("-"*5+"\n"+file)
        solver = Solver.from_csv(file)
        solver.solve()
