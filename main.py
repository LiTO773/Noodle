from ops.check_contents import check_contents
from ops.first_run import first_run


def main():
    state = first_run()
    print(state)
    check_contents(state)


if __name__ == '__main__':
    main()
