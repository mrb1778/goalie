from goalie import run_from_arg_parse, goal, GoalParam


def main():
    run_from_arg_parse(goal_manager=goal)
    print("Done")


if __name__ == "__main__":
    main()
