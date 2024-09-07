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

    def process_message(self, incoming_msg: Message):
        """
        Processes the messages from other switches. Updates its own data (members),
        if necessary, and sends messages to its neighbors, as needed.

        message: Message
            the Message received from other Switches
        """
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.


        '''


        # when to send messages to its neighbors?
        1. set pathThrough = True only when
            ?????????
            1. When sending messages, pathThrough should only be TRUE if the
                destinationID switch is the neighbor that the originID switch goes
                through to get to the claimedRoot. Otherwise, pathThrough should
                be FALSE


                # pathThrough = 
                # Boolean value indicating 
                #   the path 
                #       from the message’s origin
                #       to the claimed root 
                #   passes through the message’s destination
                # how to check this??????????????

                Message(claimed root, distance, origin switch, dest switch, pathThrough, ttl)
                1. dest switch id is the neighbor
                2. 


        2. send until ttl > 0
        '''

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
            self.root = root
            self.distance = distance
            self.sid_to_root = origin
            updated = True
        elif root == self.root:
            # 2-a-2
            # root sanme, distance shorter -> self.distance, self.sid_to_root
            if distance < self.distance: 
                self.distance = distance
                self.sid_to_root = origin
                updated = True
            # 5-b-1
            # root same, distance same, origin small -> self.sid_to_root
            elif distance  == self.distance:
                if origin < self.sid_to_root:
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
        
        if (self.sid_to_root is 5 or self.sid_to_root is 6) and (origin is 5 or origin is 6):
            print(f"Received message: root={root}, distance={distance}, origin={origin}, destination={destination}, pathThrough={pathThrough}, ttl={ttl}")
            print(f"Updated active links: from: {origin}, {self.active_links}")
        
        
        
        if old_sid_to_root != self.sid_to_root:
            self.active_links[self.sid_to_root] = True
            if old_sid_to_root in self.active_links:
                # print('sid updated: ', old_sid_to_root, 'root:', self.root, self.sid_to_root, self.active_links, incoming_msg)
                del self.active_links[old_sid_to_root]
        elif pathThrough:
            self.active_links[origin] = True
        elif self.root is not root and origin in self.active_links:
        # elif origin in self.active_links:
            # print('false: ', self.switchID, 'root:', self.root, origin, self.active_links, incoming_msg)
            del self.active_links[origin]


        # TODO stop condition
        if incoming_msg.ttl <= 0:
            return
        
        for new_destination in self.links:

            outgoing_msg = Message(self.root,
                                   self.distance, 
                                   self.switchID, 
                                   new_destination, 
                                   incoming_msg.pathThrough or self.root is new_destination, 
                                   incoming_msg.ttl - 1)
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
