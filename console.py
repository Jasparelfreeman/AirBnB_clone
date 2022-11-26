#!/usr/bin/python3
"""
Console Module
"""

import cmd
import re
import sys
import shlex
from models.__init__ import storage
from models.base_model import BaseModel


def parse_cmd(argv: str) -> list:
    """
    Parse or split a string (argv) based on some pattern example, spaces, brackects

    :param argv: string
    :return:  a list of words representing the parsed string
    """
    braces = re.search(r"\{(.*?)}", argv)
    brackets = re.search(r"\[(.*?)]", argv)
    if not braces:
        if not brackets:
            return [i.strip(",") for i in shlex.split(argv)]
        else:
            var = shlex.split(argv[:brackets.span()[0]])
            retval = [i.strip(",") for i in var]
            retval.append(brackets.group())
            return retval
    else:
        var = shlex.split(argv[:braces.span()[0]])
        retval = [i.strip(",") for i in var]
        retval.append(braces.group())
        return retval


class HBNBCommand(cmd.Cmd):
    """functionality for HBNB console"""
    prompt = "(hbnb) " if sys.__stdin__.isatty() else ""

    classes = {
        "BaseModel": BaseModel
    }

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        exit()

    def do_quit(self, argv):
        """Method to exit out of HBNB console"""
        exit()

    def do_create(self, arg):
        """
        Create an Instance of a class
        [USAGE]: create <classname>
        [Return]: id of the created class
        """
        if not arg:
            print("** class name missing **")
            return
        elif arg not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        instance = HBNBCommand.classes[arg]()
        storage.save()
        print(instance.id)
        storage.save()

    def do_show(self, argv):
        """
        Prints the string representation of an instance based on the class name and id
        [USAGE]: show <classname> <id>
        """
        cmd_arg = argv.partition(" ")
        cmd_id = cmd_arg[2]

        if cmd_id and " " in cmd_id:
            cmd_id = cmd_id.partition(" ")[0]
        if not cmd_arg[0]:
            print("** class name is missing **")
            return
        if cmd_arg[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not cmd_id:
            print("** instance id missing **")
            return
        key = "{}.{}".format(cmd_arg[0], cmd_id)
        if key not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[key])

    def do_destroy(self, argv):
        """
        Deletes an instance based on the class name and id
        [USAGE]: destroy <classname> <id>
        """
        cmd_arg = argv.partition(" ")
        cmd_id = cmd_arg[2]

        if cmd_id and " " in cmd_id:
            cmd_id = cmd_id.partition(" ")[0]
        if not cmd_arg[0]:
            print("** class name is missing **")
            return
        if cmd_arg[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not cmd_id:
            print("** instance id missing **")
            return
        key = "{}.{}".format(cmd_arg[0], cmd_id)
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, argv):
        """
        Prints all string representation of all instances
        [USAGE]: all <classname>
        """
        arg_list = shlex.split(argv)
        objects = storage.all().values()
        if not arg_list:
            print([str(obj) for obj in objects])
        else:
            if arg_list[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            else:
                print([str(obj) for obj in objects if arg_list[0] in str(obj)])

    def do_update(self, argv):
        """
        Updates an instance based on the class name and id by adding or updating attribute
        [USAGE]: update <classname> <id> <attribute name> "<attribute value>"
        """
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
