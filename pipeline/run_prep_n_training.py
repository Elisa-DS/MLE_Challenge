#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 23:51:49 2022

@author: echimenton
"""
import MP_Preprocessing as pre
import MP_Training as mpt


def main():
    """ Full training pipeline and model serialization"""

    # Data Clean
    pre.dataClean()
    
    # Run Training
    mpt.runTraining()
    
if __name__ == '__main__':
    main() 