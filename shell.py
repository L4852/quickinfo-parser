from parser import Parser

SHELL_VERSION = (0, 1, 0)


def print_version():
    major_ver, minor_ver, patch_ver = SHELL_VERSION
    print(
        f"""
                       =====================================
                            QUICKINFO SHELL v{major_ver}.{minor_ver}.{patch_ver}
                       =====================================
            """)


def print_help():
    print(
        """
                                     ========
                                       HELP
                                     ========
        
        ==================================================================
        
        This shell allows you to learn the formatting of data or to test
        different inputs quickly.
        
        Enter '-' to start edit mode, and enter key value pairs separated
        by a ':' the same way as formatted in files. Enter another '-' to 
        close the document. Use -{command name} to run a command, or do
        '-list' to list all commands.
        
        ==================================================================
        """)


def print_command_list():
    for command in commands:
        print(command)


commands = {
    'version': print_version,
    'help': print_help,
    'list': print_command_list,
}


def main():
    print_version()
    print_help()

    prompt_timeout = 5

    while True:
        user = input("<qkif>> ")

        if user == "-exit":
            break

        line_buffer = "-"

        if user == '-':
            while True:
                edit_input = input("EDIT> ")

                if edit_input == '-':
                    line_buffer += '\n-'
                    break

                line_buffer += '\n' + edit_input

            print(line_buffer)

            result = Parser(line_buffer).parse()

            print(result)
        elif '-' in user:
            try:
                command_string = user.strip('-').strip(' ')

                if command_string in commands:
                    commands[command_string]()
                else:
                    print("Command not found.")

            except Exception as e:
                print("An error occurred while trying to run a command.")
        else:
            if prompt_timeout - 1 >= 0:
                prompt_timeout -= 1

            if prompt_timeout == 0:
                print("Enter '-help' for more information.")
                prompt_timeout = 5


if __name__ == "__main__":
    main()
