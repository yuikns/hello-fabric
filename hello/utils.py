# -*- coding: utf-8 -*-
import os


def mkdirs(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception as e:
        raise e
