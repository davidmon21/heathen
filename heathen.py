#!/usr/bin/env python
import os
import random
import argparse
import configparser
from datetime import datetime
import pydoc
import re

try:
    from pysword.modules import SwordModules
    from pysword.bible import SwordBible
    import pysword
except:
    print("You are missing pysword, to install: pip install [--user] pysword\nOr check your repository")
    exit(1)

class Heathen():
    programpath = os.path.dirname(os.path.realpath(__file__))
    heathenconfig =  os.path.join(programpath,".heathen")
    version = "DRC"
    bible = None
    sword = None
    heathenconf = configparser.ConfigParser()
    available_versions = None

    def __init__(self, conf = heathenconfig):
        if os.path.exists(conf):
            self.heathenconfig = conf
            self.heathenconf.read(self.heathenconfig)
            self.sword = SwordModules(self.heathenconf['MAIN']['swordpath'])
            self.available_versions = self.sword.parse_modules()
            self.bible = self.sword.get_bible_from_module(self.heathenconf['MAIN']['version'])

    def open_bible(version):
        self.bible = self.sword.get_bible_from_module(version)
   
    def return_verse(self, book, chapter,verses = None):
        if verses != None:
            verses = verses.split("-")
            if len(verses) > 1:
                selected = list(range(int(verses[0]), int(verses[1])+1))
            else:
                selected = [int(verses[0])]
        else:
            selected = list(range(1,self.bible.get_structure().find_book(book)[1].chapter_lengths[chapter-1]+1))
        return self.bible.get(books=[book],  chapters=int(chapter), verses=selected)

    # def heathen_first_run(self):
    #     self.displayer("Welcome to heathen!")
    #     answer = self.handlingfunction("Do you have an existing sword path?(y/n)").lower()

    #     if 'y' in answer:
    #         answer = self.handlingfunction("Enter your sword directory path: ")
    #         self.biblepath = answer.strip().rstrip()


    #         self.pyrepoz = pysword_repo.PyswordRepo(swrdpath=self.biblepath,repoconf=".heathenrepo")

    #         answer = self.handlingfunction("Would you like heathen to manage your repo?(y/n): ")
    #         if 'y' in answer:
    #             installedmodules = self.pyrepoz.bootstrap_ibm()
    #             repo_management = 'y'
    #         elif 'n' in answer:
    #             installedmodules = self.pyrepoz.find_installed_modules()
    #             repo_management = 'n'
    #         installedmodules = self.pyrepoz.list_installed_modules()
    #         installedmodslen = range(0,len(installedmodules))
    #         for x in installedmodslen:
    #             self.displayer(str(x+1)+": "+installedmodules[x])
    #         answer = self.handlingfunction("Select module as default version: ")
    #         if answer.isdigit and (int(answer)-1) in installedmodslen:
    #             self.version = installedmodules[int(answer)-1][0]
    #         self.heathenconf['MAIN'] = {'swordpath':self.biblepath, 'version':self.version, 'repo management':repo_management }

    #     elif 'n' in answer:
    #         self.biblepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),".bibles")
    #         if not os.path.exists(self.biblepath):
    #             os.makedirs(self.biblepath)
    #         self.pyrepoz = pysword_repo.PyswordRepo(swrdpath=self.biblepath,repoconf=".heathenrepo")
    #         self.pyrepoz.initiate_repo()
    #         self.pyrepoz.update_repo_list()
    #         self.pyrepoz.download_repos()
    #         self.pyrepoz.install_module('drc.conf-drc')
    #         self.version = 'drc.conf-drc'
    #         self.heathenconf['MAIN'] = { 'swordpath':self.biblepath, 'version':self.version, 'repo management':'y' }


    #     with open(self.heathenconfig,'w') as conf2:
    #         self.heathenconf.write(conf2)
