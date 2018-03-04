#!/usr/bin/python


class HSTerm:

    @staticmethod
    def term(message):
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
    def term_exec(message):
        """
        Write a line into the exec file and append a html and normal line break.
        """
        with open('exec_file.txt', 'a') as file:
            file.write(message + '\n')

    @staticmethod
    def exec_filename():
        """
        Return the exec filename.
        """
        return 'exec_file.txt'
