if __name__ == "__main__":
    from pulp import LpStatus
    from pathlib import Path
    from pprint import pprint
    from pandas import read_csv
    from numpy import NaN
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    from internal.parser import create_students_preferences, create_groups
    from internal.debug import show_classes_per_student
    from internal.algorithm import ClassDivider

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-r", "--test-reading", action="store_true", help="test reading CSV")
    parser.add_argument("-p", "--test-parsing", action="store_true", help="test parsing CSV and putting it into the models")
    parser.add_argument("-c", "--test-creation", action="store_true", help="test model creation")
    parser.add_argument("-s", "--test-solution", action="store_true", help="test model solution")
    parser.add_argument("-S", "--test-suite", action="store", default=1, help="choose test suite")
    parser.add_argument("-O", "--test-option", action="store", default=1, help="choose test suite option")
    args = parser.parse_args()

    path = Path(__file__).parent
    groups_df = read_csv(path.joinpath(f"../tests/data/suite_{args.test_suite}/plan{args.test_suite}.csv"),
                            sep=';',
                            lineterminator="\r"
                        ).replace("\n", "", regex=True).replace("", NaN).dropna(how="all")
    students_df = read_csv(path.joinpath(f"../tests/data/suite_{args.test_suite}/podzial{args.test_suite}_{args.test_option}.csv"),
                              sep=';',
                              lineterminator="\r"
                          ).replace("\n", "", regex=True).replace("", NaN).dropna(how="all")


    students = create_students_preferences(students_df)
    groups = create_groups(groups_df)

    if args.test_reading:
        print(students_df)
        print(groups_df)

    if args.test_parsing:
        pprint(students)
        pprint(groups)

    if args.test_creation or args.test_solution:
        model = ClassDivider(students, groups)
        if args.test_creation:
            print(model)
            print('-'*20)
            print(f"No. Variables: {len(model.model.variables())}")
            print(f"No. Constraints: {len(model.model.constraints)}")
            print('-'*20)

        status = model.solve()
        if status == 1:
            print(f"Model solved and is {LpStatus[status]}!")
            if args.test_solution:
                show_classes_per_student(model.model, students, groups)
        else:
            print(f"Model is {LpStatus[status]}!")

