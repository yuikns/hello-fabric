# -*- coding: utf-8 -*-

from hello.config import DefaultConfig


if __name__ == "__main__":
    print("starting service %s from file: %s"%(DefaultConfig.PROJECT, __file__))

