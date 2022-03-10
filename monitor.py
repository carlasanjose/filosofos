#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:18:47 2022

@author: Lasjimenez
"""
from multiprocessing import Process, \
  BoundedSemaphore, Semaphore, Lock, Condition,\
  current_process, \
  Value, Array, Manager


class Table():
    
    def __init__(self, nphil: int, manager):
        self.mutex = Lock()
        self.nphil = nphil
        self.manager = manager
        self.phil = self.manager.list([False]*nphil)
        self.eating = Value('i',0)
        self.current_proc =  None
        self.free_fork = Condition(self.mutex)

    def no_comen_lados(self):
        n = self.current_proc
        return ((not self.phil[(n-1)%(self.nphil)]) and (not self.phil[(n+1)%(self.nphil)]))
    
    def set_current_phil(self,num):
        self.current_proc=num

    def wants_eat(self,num):
        self.mutex.acquire()
        self.current_proc = num
        self.free_fork.wait_for(self.no_comen_lados)
        self.phil[num] = True
        self.eating.value+=1
        self.mutex.release()

    

    
    def wants_think(self,num):
        self.mutex.acquire()
        self.phil[num]= False
        self.eating.value-=1
        self.free_fork.notify()
        self.mutex.release()
    
    
    