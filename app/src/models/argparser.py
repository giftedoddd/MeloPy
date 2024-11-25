import argparse

class ArgParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.prog = "MeloPy"
        self.usage = "Open-Source Advanced Music Player Written in Python for local and online usages."
        self.description = "Welcome to MeloPy!"
        self.epilog = "Author: Giftedodd\nemail: giftedoddd@gmail.com"
        self.prefix_chars = "-"
        self.add_help = False

    def args_instructor(self):
        self.add_argument("-h", "--help", action="store", nargs=0, help="Show help")
        # self.add_argument("-s", "--setpath", nargs="*", default=)