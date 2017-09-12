#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cmd
import re
import os
from tinydb import TinyDB, Query

class Cli(cmd.Cmd):
    #add_pattern = re.compile('')

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.intro = "Hello\nType 'help' for help"
        self.doc_header ="List of commands (type 'help %command%' for help on certain command)"
        
        self.aliases = {
                         'q'  : self.do_quit    ,
                         'h'  : self.do_help    ,
                         'a'  : self.do_add     ,
                         'l'  : self.do_list    ,
                         'd'  : self.do_advance ,
                         'rm' : self.do_remove
                       }

        self.db = TinyDB('db.json')

    def do_quit(self, line):
        '''Exit the program.'''
        return True

    def do_help(self, args):
        #'''List available commands.'''
        if len(args) == 0:
            cmd.Cmd.do_help(self, '')
            return False

        line = args[0]
        if line in self.aliases:
            line = self.aliases[line].__name__[3:]
        cmd.Cmd.do_help(self, line)

    def parse_args(self, line):
        args = line.split()
        return args[0], args[1:]

    def default(self, line):
        cmd, args = self.parse_args(line)
        if cmd in self.aliases:
            return self.aliases[cmd](args)
        else:
            print('Unknown command: {}'.format(line))

    def get_free_id(self):
        return len(self.db.all()) + 1

    def do_add(self, args):
        '''add task'''
        if len(args) == 0:
            print('Wrong number of arguments. See help.')
            return False

        id = self.get_free_id()
        desc = ' '.join(args)
        self.db.insert({'id': id, 'line': desc, 'done': 0})
        print('Entry {} was added with id {}'.format(desc, id))

    def do_list(self, line):
        '''list tasks'''
        rows, columns = os.popen('stty size', 'r').read().split()
        list = self.db.all()

        if len(list) == 0:
            print('(empty)')
            return False

        for task in list:
            l = '    {}) {} '.format(task['id'], task['line'])
            l = l.ljust(int(columns) - 12) + '(' + str(task['done']) + '/10)'
            print(l)

    def do_advance(self, args):
        if len(args) != 2:
            print('Wrong amount of arguments. See help')
            return False
        id = args[0]

        Task = Query()
        res = self.db.search(Task.id == id)
        if len(res) == 0:
            print('There is no tasks with such id')
            return False

        amount = max(0, args[1] + res['done'])
        if amount >= 10:
            print('Task \'{}\' completed! Congratulations!'.format(res['desc']))
            self.db.remove(Task.id == id)
            return False
        self.db.update({'done': amount}, Task.id == id)
        print('Task \'{}\' advanced! New progress is ({}/10)'.format(res['desc'], amount))

    def do_remove(self, args):
        if len(args) != 1:
            print('Wrong amount of arguments. See help.')
            return False
        Task = Query()

        res = self.db.search(Task.id == id)
        if len(res) == 0:
            print('There is no tasks with such id')
        else:
            self.db.remove(Task.id == int(args[0]))
            print('Task \'{}\' removed'.format(res['desc']))


def main():
    cli = Cli()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("Terminating...")

if __name__ == '__main__':
    main()
