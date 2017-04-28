#!/usr/bin/env python3


class HSTerm:

    @staticmethod
    def term(message: str):
        """
        Print a message on the terminal.
        """
        print(message)

    @staticmethod
    def clear_exec():
        """
        Clear the exec file to write new content into it.
        """
        with open('exec_file.txt', 'w') as file:
            file.write('')

    @staticmethod
    def term_exec(message: str):
        """
        Write a line into the exec file and append a html and normal line break.
        """
        with open('exec_file.txt', 'a') as file:
            file.write(message + '<br>\n')

    @staticmethod
    def exec_filename() -> str:
        """
        Return the exec filename.
        """
        return 'exec_file.txt'
