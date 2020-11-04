# !/usr/bin/python
# <begin of the license chapter>
# Copyright (c) 2020 by Igor Royzis.
# The program can be freely used, distributed and modified if:
# a) this note, as a whole chapter, is not removed or modified from the readme, documentation and the source code;
# b) the program or its derived work is not used for commercial purposes. For a commercial license please contact the author.
# The official project page: https://github.com/royzis/paswd_import
# <end of the license chapter>
import datetime, uuid, csv, argparse


class PassParserError(Exception):
    pass

class PassEntry:
    def __init__(self, title = 'title', url='', uname='', password='', notes=''):
        self.title = title
        self.url = url
        self.uname = uname
        self.password = password
        self.notes = notes

    def __eq__(self, obj):
        if isinstance(obj, self.__class__):
            return (self.title == obj.title or self.title == obj.url or self.url == obj.title) and self.url == obj.url and self.uname == obj.uname and self.password == obj.password and self.notes == obj.notes
        else: return NotImplemented

    def __str__(self):
        return f"url:{self.url}, user:{self.uname}, password: {self.password}, title: {self.title}"

    def make_firefox_entry(self, test=False):
        if test:
            g = '{00000000-0000-0000-0000-000000000000}'
            t = 123456789012
        else:
            g = '{' + str(uuid.uuid4()) + '}'
            t = int(datetime.datetime.now().timestamp())*1000   # Firefox stores the unix time in miliseconds
        return f'"{self.url}","{self.uname}","{self.password}",,"{self.url}","{g}","{t}","{t}","{t}"'

    def make_lastpass_entry(self):
        return f"{self.url},{self.uname},{self.password},,{self.title},,0"

    def make_dropbox_entry(self):
        return f"{self.title},{self.url},{self.uname},{self.password},"

    def parse_csv(self, s, length):
        try:
            l = list(csv.reader([s]))[0]
        except csv.Error(e):
            raise PassParserError('Error parsing CSV')
        if len(l) != length:
            raise PassParserError(f'Invalid CSV forrmat, {length} columns expected instead of {len(l)}')
        return l

    def parse_firefox_entry(self, s):
        l = self.parse_csv(s, 9)
        self.url = l[0].strip()
        self.uname = l[1].strip()
        self.password = l[2].strip()
        self.title = l[0].strip()
        self.notes = ''

    def parse_lastpass_entry(self, s):
        l = self.parse_csv(s, 7)
        self.url = l[0].strip()
        self.uname = l[1].strip()
        self.password = l[2].strip()
        self.title = l[4].strip()
        self.notes = ''

    def parse_dropbox_entry(self, s):
        l = self.parse_csv(s, 5)
        self.title = l[0].strip()
        self.url = l[1].strip()
        self.uname = l[2].strip()
        self.password = l[3].strip()
        self.notes = ''

def unit_test():
    t1 = PassEntry('test1.com','test1.com', 'user1', 'password1')
    t1_ff = '"test1.com","user1","password1",,"test1.com","{00000000-0000-0000-0000-000000000000}","123456789012","123456789012","123456789012"'
    t1_lp = "test1.com,user1,password1,,Test1,,0"
    t1_dp = "Test1,test1.com,user1,password1,"
    t1_1 = PassEntry()
    t1_1.parse_firefox_entry(t1_ff)
    if t1_1 == t1:
        print("Test 1.1 passed")
        t1_2 = t1_1.make_firefox_entry(test=True)
        if t1_2 != t1_ff:
            print(f"Test 1.2 failed. Expected '{t1_ff}'\nRecevied '{t1_2}'")
        else:
            print(f"Test 1.2 passed")

            t2_1 = PassEntry()
            t2_1.parse_lastpass_entry(t1_lp)
            if t2_1 == t1:
                print("Test 2.1 passed")
                t2_2 = t2_1.make_lastpass_entry()
                if t2_2 != t1_lp:
                    print(f"Test 2.2 failed. Expected '{t1_lp}'\nRecevied '{t2_2}'")
                else:
                    print(f"Test 2.2 passed")

                    t3_1 = PassEntry()
                    t3_1.parse_dropbox_entry(t1_dp)
                    if t3_1 == t1:
                        print("Test 3.1 passed")
                        t3_2 = t3_1.make_dropbox_entry()
                        if t3_2 != t1_dp:
                            print(f"Test 3.2 failed. Expected '{t1_dp}'\nRecevied '{t3_2}'")
                        else:
                            print("Test 3.2 passed")
                    else:
                        print(f"Test 3.1 failed\n{t1}\n{t3_1}")
            else:
                print(f"Test 2.1 failed\n{t1}\n{t2_1}")
    else:
        print(f"Test 1.1 Failed\n{t1}\n{t1_1}")

def perform(input, inp_format, output, out_format, verbose):
    try:
        with open(input, 'r') as f:
            data = f.readlines()
    except IOError:
            print(f'error: reading file {input}')
            return -1
    e = PassEntry()
    with open(output, 'w') as f:
        if out_format == 'ff':
            # FF requires the header in the CSV file
            f.write('"url","username","password","httpRealm","formActionOrigin","guid","timeCreated","timeLastUsed","timePasswordChanged"\n')
        elif out_format == 'lp':
            # So does LastPass
            f.write('url,username,password,extra,name,grouping,fav\n')
        elif out_format == 'dp':
            # And probably the Dropbox Passwords
            f.write('title,website,login,password,notes\n')
        for l in data[1:]:                  # Skipping the 1st line which is the header
            try:
                ls = l.strip()
                if inp_format == 'dp':
                    e.parse_dropbox_entry(ls)
                elif inp_format == 'ff':
                    e.parse_firefox_entry(ls)
                elif inp_format == 'lp':
                    e.parse_lastpass_entry(ls)
                else:
                    print(f'error: Invalid format {inp_format}')
                    return -1
            except PassParserError:
                if verbose > 0:
                    print(f"Warning: cant parse a line: '{l}'")
            if out_format == 'dp':
                s = e.make_dropbox_entry()
            elif out_format == 'ff':
                s = e.make_firefox_entry()            
            elif out_format == 'lp':
                s = e.make_lastpass_entry()
            else:
                print(f'error: Invalid format {out_format}')
                return -1
            f.write(s+'\n')
    return 0


def main():
    formats = ['ff','lp','dp']
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help ="Input CSV file", type=str)
    parser.add_argument('inp_format', help ="Input CSV format ff|lp|dp", choices=formats)
    parser.add_argument('output', help ="Output CSV file", type=str)
    parser.add_argument('out_format', help ="Output CSV format ff|lp|dp", choices=formats)
    parser.add_argument("-v", "--verbose", help="Verbose level", action='count', default=0)
    args = parser.parse_args()
    if args.inp_format == args.out_format:
        print("error: The input and output formats must differ")
    else:
        perform(args.input, args.inp_format, args.output, args.out_format, args.verbose)


if __name__ == "__main__":
    main()