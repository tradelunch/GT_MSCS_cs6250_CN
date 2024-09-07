"""
/*
 * Copyright © 2022 Georgia Institute of Technology (Georgia Tech). All Rights Reserved.
 * Template code for CS 6250 Computer Networks
 * Instructors: Maria Konte
 * Head TAs: Johann Lau and Ken Westdorp
 *
 * Georgia Tech asserts copyright ownership of this template and all derivative
 * works, including solutions to the projects assigned in this course. Students
 * and other users of this template code are advised not to share it with others
 * or to make it available on publicly viewable websites including repositories
 * such as GitHub and GitLab. This copyright statement should not be removed
 * or edited. Removing it will be considered an academic integrity issue.
 *
 * We do grant permission to share solutions privately with non-students such
 * as potential employers as long as this header remains in full. However,
 * sharing with other current or future students or using a medium to share
 * where the code is widely available on the internet is prohibited and
 * subject to being investigated as a GT honor code violation.
 * Please respect the intellectual ownership of the course materials
 * (including exam keys, project requirements, etc.) and do not distribute them
 * to anyone not enrolled in the class. Use of any previous semester course
 * materials, such as tests, quizzes, homework, projects, videos, and any other
 * coursework, is prohibited in this course.
 */
"""

# Spanning Tree Protocol project for GA Tech OMSCS CS-6250: Computer Networks
#
# Copyright 2023 Vincent Hu
#           Based on prior work by Sean Donovan, Jared Scott, James Lohse, and Michael Brown

from Message import Message
from StpSwitch import StpSwitch

# import global_vars

class Switch(StpSwitch):
    """
    This class defines a Switch (node/bridge) that can send and receive messages
    to converge on a final, loop-free spanning tree. This class
    is a child class of the StpSwitch class. To remain within the spirit of
    the project, the only inherited members or functions a student is permitted
    to use are:

    switchID: int
        the ID number of this switch object)
    links: list
        the list of switch IDs connected to this switch object)
    send_message(msg: Message)
        Sends a Message object to another switch)

    Students should use the send_message function to implement the algorithm.
    Do NOT use the self.topology.send_message function. A non-distributed (centralized)
    algorithm will not receive credit. Do NOT use global variables.

    Student code should NOT access the following members, otherwise they may violate
    the spirit of the project:

    topolink: Topology
        a link to the greater Topology structure used for message passing
    self.topology: Topology
        a link to the greater Topology structure used for message passing
    """

    def __init__(self, idNum: int, topolink: object, neighbors: list):
        """
        Invokes the super class constructor (StpSwitch), which makes the following
        members available to this object:

        idNum: int
            the ID number of this switch object
        neighbors: list
            the list of switch IDs connected to this switch object
        """
        super(Switch, self).__init__(idNum, topolink, neighbors)
        # TODO: Define class members to keep track of which links are part of the spanning tree

        self.root = idNum
        self.distance = 0
        self.sid_pass_through = idNum

        self.active_links = {}
        self.ttl = None

    def find_path_through(self, sid_out_going):
        if self.sid_pass_through == sid_out_going:
            return True
        return False

    def process_message(self, incoming_msg: Message):
        # self.print_count()
        # self.print_msg(incoming_msg)
        # self.print_self()

        root = incoming_msg.root
        distance = incoming_msg.distance
        origin = incoming_msg.origin
        destination = incoming_msg.destination
        pathThrough = incoming_msg.pathThrough
        ttl = incoming_msg.ttl

        # self switch root info update
        # 1. should update self.root
        #     1. lower claimedRoot.
        # 2. update self.distance 
        #     1. root updated
        #     2. shorter distance existing
        

        '''
        1. 2-a-i
        - update root
            incoming root is lower than current root: update
        - update distance
            - root updated
            - same root, but shorter path
        '''
        
        updated = False
        # incomming root lower -> self.root, self.distance update, self.sid_to_root
        if root < self.root:
            self.remove_active_link(self.sid_pass_through, incoming_msg, 'root')
            self.add_active_link(origin, incoming_msg, 'root')
            
            self.root = root
            self.distance = distance + 1

            # update active link
            self.sid_pass_through = origin
            updated = True
        elif root == self.root:
            # 2-a-2
            # root sanme, distance shorter -> self.distance, self.sid_to_root
            if distance + 1 < self.distance: 
                self.distance = distance + 1
                self.remove_active_link(self.sid_pass_through, incoming_msg, 'shorter path')
                self.add_active_link(origin, incoming_msg, 'shorter path')

                self.sid_pass_through = origin
                updated = True
            # 5-b-1
            # root same, distance same, origin small -> self.sid_to_root
            elif distance + 1 == self.distance:
                if origin < self.sid_pass_through:
                    self.remove_active_link(self.sid_pass_through, incoming_msg, 'lower sid')
                    self.add_active_link(origin, incoming_msg, 'lower sid')

                    self.sid_pass_through = origin
                    updated = True

        # self active_links update
        # 1. find a new path through a different neighbor
        #     1. add the new link to active_links
        #     2. remove the old link from active_links
        # 2. if pathThrough = True
        #     1. incoming_msg.origin not in active_links -> 
        #         1. add incoming.origin to self.active_links
        # 3. if pathThrough = False
        #     1. incoming_msg.origin in self.active_links
        #         1. remove incoming_msg.origin from self.active_links
        #

        if updated:
            self.ttl = ttl

        if pathThrough:
            self.add_active_link(origin, incoming_msg, 'pathThrough')
        else:
            if self.sid_pass_through != origin:
                self.remove_active_link(origin, incoming_msg, 'pathThrough')
                pass


        # self.print_self()
        # print('---', incoming_msg.ttl)
        # print('---')

        # stop condition
        if incoming_msg.ttl <= 0:
            return
        
        for new_destination in self.links:
            out_going_path_through = self.find_path_through(new_destination)
            outgoing_msg = Message(self.root,
                                   self.distance, 
                                   self.switchID, 
                                   new_destination,
                                   out_going_path_through,
                                   ttl - 1)
            self.send_message(outgoing_msg)

    def generate_logstring(self):
        sorted_links = sorted(self.active_links)
        return ", ".join([f"{self.switchID} - {link}" for link in sorted_links])

    # util functions for my self
    def print_self(self):  
        print(f"{self.switchID}:", f"self=[{self.root}: {self.distance}, {self.switchID}, {self.active_links}, {self.sid_pass_through}, {self.ttl}]")

    def print_msg(self, msg: Message):
        root = msg.root
        distance = msg.distance
        origin = msg.origin
        destination = msg.destination
        pathThrough = msg.pathThrough
        ttl = msg.ttl

        print(f"{self.switchID}: msg= [{root}, {distance}, {origin}, {destination}, {pathThrough}, {ttl}]")

    def remove_active_link(self, id, msg: Message, loc=''):
        # print(f'>> {self.switchID}: remove link: {id} {loc}')
        # self.print_msg(msg)
        # self.print_self()
        if id in self.active_links:
            del self.active_links[id]
    
    def add_active_link(self, id, msg: Message, loc = ''):   
        # print(f'>> {self.switchID}: add link: {id} {loc}')
        # self.print_msg(msg)        
        # self.print_self()
        self.active_links[id] = True

    def print_count(self):
        # print('==>> new')
        # global_vars.cnt += 1
        # print(f'# {global_vars.cnt}: {incoming_msg.origin}->{incoming_msg.destination} ###')
        pass