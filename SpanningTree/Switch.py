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
        self.sid_to_root = idNum

        self.active_links = {}
        self.ttl = None

        # self.active_links = set(neighbors)  # Initially, all links are active
        # self.neighbor_info = {neighbor: {'root': neighbor, 'distance': 0} for neighbor in neighbors}

    def print_self(self):
        if self.switchID != 6:
            return        
        print(f"{self.switchID}:", f"self=[{self.root}: {self.distance}, {self.switchID}, {self.active_links}, {self.sid_to_root}, {self.ttl}]")

    def print_msg(self, msg: Message):
        if self.switchID != 6:
            return
        root = msg.root
        distance = msg.distance
        origin = msg.origin
        destination = msg.destination
        pathThrough = msg.pathThrough
        ttl = msg.ttl

        print(f"{self.switchID}: msg= [{root}, {distance}, {origin}, {destination}, {pathThrough}, {ttl}]")


    def remove_active_link(self, id, msg: Message, loc=''):
        print(f'>> {self.switchID}: remove link: {id} {loc}')
        self.print_msg(msg)
        self.print_self()
        if id in self.active_links:
            del self.active_links[id]
    
    def add_active_link(self, id, msg: Message, loc = ''):   
        print(f'>> {self.switchID}: add link: {id} {loc}')
        self.print_msg(msg)        
        self.print_self()
        self.active_links[id] = True

    def print_count(self):
        # global_vars.cnt += 1
        # print(f'# {global_vars.cnt}: {incoming_msg.origin}->{incoming_msg.destination} ###')
        pass

    def process_message(self, incoming_msg: Message):
        self.print_count()
        self.print_msg(incoming_msg)
        self.print_self()

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
        old_sid_to_root = self.sid_to_root
        updated = False
        # incomming root lower -> self.root, self.distance update, self.sid_to_root
        if root < self.root:
            self.remove_active_link(self.sid_to_root, incoming_msg, 'root')
            self.add_active_link(origin, incoming_msg, 'root')
            
            self.root = root
            self.distance = distance + 1

            # update active link
            self.sid_to_root = origin
            updated = True
        elif root == self.root:
            # 2-a-2
            # root sanme, distance shorter -> self.distance, self.sid_to_root
            if distance + 1 < self.distance: 
                self.distance = distance + 1
                self.remove_active_link(self.sid_to_root, incoming_msg, 'shorter path')
                self.add_active_link(origin, incoming_msg, 'shorter path')

                self.sid_to_root = origin
                updated = True
            # 5-b-1
            # root same, distance same, origin small -> self.sid_to_root
            elif distance + 1 == self.distance:
                if origin < self.sid_to_root:
                    self.remove_active_link(self.sid_to_root, incoming_msg, 'lower sid')
                    self.add_active_link(origin, incoming_msg, 'lower sid')

                    self.sid_to_root = origin
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
            if self.sid_to_root != origin :
                self.remove_active_link(origin, incoming_msg, 'pathThrough')
                pass


        self.print_self()
        print('---', incoming_msg.ttl)
        print('---')
        # stop condition
        if incoming_msg.ttl <= 0:
            return
        
        for new_destination in self.links:

            outgoing_msg = Message(self.root,
                                   self.distance, 
                                   self.switchID, 
                                   new_destination, 
                                   
                                self.root == root 
                                and self.sid_to_root == new_destination,
                                #    pathThrough or self.root is root, 
                                #    self.root is new_destination, 
                                   ttl - 1)
            self.send_message(outgoing_msg)
            # print('curr_switch:: ', self.switchID)
            # print('from [', incoming_msg.root, incoming_msg.distance, incoming_msg.origin, incoming_msg.destination, incoming_msg.pathThrough, incoming_msg.ttl, ']')
            # print('self: ', self.root, self.distance, self.switchID, self.sid_to_root, self.active_links)
            # print('to   [', outgoing_msg.root, outgoing_msg.distance, outgoing_msg.origin, outgoing_msg.destination, outgoing_msg.pathThrough, outgoing_msg.ttl, ']')
            # print(f'>> {incoming_msg.origin} - {self.switchID} - {outgoing_msg.destination}')
            # print('----')

    def generate_logstring(self):
        """
        Logs this Switch's list of Active Links in a SORTED order

        returns a String of format:
            SwitchID - ActiveLink1, SwitchID - ActiveLink2, etc.
        """
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked
        #      only after the simulation is complete.  Output the links included in the
        #      spanning tree by INCREASING destination switch ID on a single line.
        #
        #      Print links as '(source switch id) - (destination switch id)', separating links
        #      with a comma - ','.
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #
        #      A full example of a valid output file is included (Logs/) in the project skeleton.

        sorted_links = sorted(self.active_links)
        print("log: ", self.switchID, self.active_links)
        return ", ".join([f"{self.switchID} - {link}" for link in sorted_links])
