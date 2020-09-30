from ops.first_run import first_run


def main():
    state, conn = first_run()

    # Check differences for each moodle
    # for config in state:
    #     check_contents(conn, config)


if __name__ == '__main__':
    main()
