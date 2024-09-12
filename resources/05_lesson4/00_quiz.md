SPs can be categorized into three tiers or types
access ISPs (or Tier-3), regional ISPs (or Tier-2), and large global scale ISPs (or Tier-1).


Large-scale Tier-1 ISPs
- operate on a global scale
- form the "backbone" network over which smaller networks can connect.
- Some example Tier-1 ISPs include AT&T, NTT, Level-3, and Sprint.



Previous
Play
Next
Rewind 10 seconds
Move forward 10 seconds
Unmute
0:01
/
0:15
Full screen
Brainpower
Read More
Regional ISP and Local ISPs
regional ISPs connect to Tier-1 ISPs, and smaller access ISPs connect to regional ISPs.


IXPs are
interconnection infrastructures, which provide the physical infrastructure, where multiple networks (e.g., ISPs and CDNs) can interconnect and exchange traffic locally.


CDNs
Content Distribution Networks

- goal of having greater control of how the content is delivered to the end-users while reducing connectivity costs. Some examples of CDNs are Google and Netflix.

- networks have multiple data centers, and each one of them may be housing hundreds of servers that are distributed across the world.


Is the internet topography Hierarchial or flat
at beginning was hierarchial but today is more flat because of the dominant IXPs and CDNs


Autonomous Systems: (AS)

One or more networks that are governed by a single protocol, which provides routing for the Internet backbone.

An AS is a group of routers (including the links among them) that operate under the same administrative authority.

An ISP, for example, may operate as a single AS, or it may operate through multiple ASes.

Each AS implements its own set of policies, makes its own traffic engineering decisions and interconnection strategies, and determines how the traffic leaves and enters its network.


What is the Protocols for routing traffic between and within ASes

The border routers of the ASes use the Border Gateway Protocol (BGP) to exchange routing information with one another.


An autonomous System is a group of routers that operate under ________ administrative ____________
the same , authority


ASers Provider-Customer relationship (or transit)

Based on a financial settlement that determines how much the customer will pay the provider. The provider forwards the customer's traffic to destinations found in the provider's routing table (including the opposite direction of the traffic).


ASers Peering relationship

- two ASes share access to a subset of each other's routing tables.

- routes shared between two peers are often restricted to the respective customers of each one

- agreement holds as long as the traffic exchanged between the two peers is not highly asymmetric.

- Peering relationships are formed between Tier-1 ISPs but also between smaller ISPs


How do AS providers charge customers>?
1. Based on a fixed price, given that the bandwidth used is within a predefined range.

2. Based on the bandwidth used. The bandwidth usage is calculated based on periodic measurements, e.g., five-minute intervals. The provider then charges by taking the 95th percentile of the distribution of the measurements.



Types of Routes an ASer will export
Routes learned from customers: These are the routes X receives as advertisements from its customers. Since provider X is getting paid to provide reachability to a customer AS, it makes sense that X wants to advertise these customer routes to as many other neighboring ASes as possible. This will likely cause more traffic towards the customer (through X) and, hence, more revenue for X.

Routes learned from providers: hese are the routes X receives as advertisements from its providers. Advertising these routes does not make sense since X does not have the financial incentive to carry traffic for its provider's routes. Therefore, these routes are withheld from X's peers and other X's providers, but they are advertised to X's customers.

Routes learned from peers: These are routes that X receives as advertisements from its peers. As we saw earlier, it does not make sense for X to advertise to provider A the routes it receives from provider B. Because in that case, providers A and B will use X to reach the advertised destinations without X making revenue. The same is true for the routes that X learns from peers.



Types of Routes an ASer will import
based on which neighboring AS advertises them and the type of business relationship established.

AS receives multiple route advertisements towards the same destination from multiple ASes, it needs to rank the routes before selecting which one to import. In order of preference, the imported routes are the customer routes, then the peer routes, and finally the provider routes.



Reasons behind ranking routes on import based on customer, peer, provider
1. wants to ensure that routes towards its customers do not traverse other ASes unnecessarily generating costs,

2. uses routes learned from peers since these are usually "free" (under the peering agreement),

3. and finally resorts to importing routes learned from providers as these will add to costs.


What are the design goals of BGP Protocal?
Scalability:As the size of the Internet grows, the same is true for the number of ASes, the number of prefixes in the routing tables, the network churn, and the BGP traffic exchanged between routers. Goal is to manage the complications of this growth

Express routing policies:BGP has defined route attributes that allow ASes to implement policies (which routes to import and export) through route filtering and route ranking

Allow cooperation among ASes: dividual AS can still make local decisions (which routes to import and export)

Security:



BGP peers
The routers at the end of a TCP connection that happens in a BGP.


BGP session
two BGP routers ("peers") exchange BGP messages over semi-permanent TCP Connection.


external BGP (eBGP) session
A BGP session between a pair of routers in two different ASes


Internal BGP (iBGP) session
BGP session between routers that belong to the same AS


Two Types of BGP Messages
The UPDATE messages contain information about the routes that have changed since the previous update. There are two kinds of updates:

- Announcements are messages that advertise new routes and updates to existing routes. They include several standardized attributes.

- Withdrawals messages inform that receive that a previously announced route is no longer available. The removal could be due to some failure or a change in the routing policy.

The KEEPALIVE messages are exchanged between peers to keep a current session going



BGP Prefix Reachability:

In the BGP protocol, destinations are represented by IP prefixes. Each prefix represents a subnet or a collection of subnets that an AS can reach.


Path Attributes and BGP Routes

ASPATH: Each AS is identified by its autonomous system number (ASN). As an announcement passes through various ASes, their identifiers are included in the ASPATH attribute. This attribute prevents loops and is used to choose between multiple routes to the same destination, the route with the shortest path.

NEXT HOP: This attribute refers to the next-hop router's IP address (interface) along the path towards the destination. Internal routers use the field to store the IP address of the border router. Internal BGP routers will forward all traffic bound for external destinations through the border router. Suppose there is more than one such router on the network, and each advertises a path to the same external destination. In that case, NEXT HOP allows the internal router to store in the forwarding table the best path according to the AS routing policy.



eBGP and iBGP
eBGP (for sessions are between border routers of neighboring ASes) and iBGP (for sessions between internal routers of the same AS).


Router Decision Process
A router compares a pair of routes by going through the list of attributes, as shown in the figure below. For each attribute, it selects the route with the attribute value that will help apply the policy. If for a specific attribute, the values are the same, then it goes to the next attribute.


LocalPref
The LocalPref attribute is used to prefer routes learned through a specific AS over other ASes.


MED (Multi-Exit Discriminator) attribute
used by ASes connected by multiple links to designate which links are preferred for inbound traffic. For example, the network operator of AS B will assign different MED values to its routes advertised to AS A through R1 and different MED values to its routes advertised through R2


Flap damping
To apply this technique, an AS will track the number of updates to a specific prefix over a certain amount of time. If the tracked value reaches a configurable value, the AS can suppress that route until a later time.

Because this can affect reachability, an AS can be strategic about how it uses this technique for certain prefixes. For example, more specific prefixes could be more aggressively suppressed (lower thresholds), while routes to known destinations that require high availability could be allowed higher thresholds.


What are IXPs?
IXPs are physical infrastructures that provide the means for ASes to interconnect and directly exchange traffic with one another.


participant ASes
Are the ASes that interconnect at an IXP


Where are IXPs located?
in facilities such as data centers, which provide reliability, sufficient power, and physical security.


What is BGP?
Border Gateway Protocol is the primary Routing protocol used on the internet. ISP's must use BGP.


Why have IXPs become increasingly popular?

- IXPs are interconnection hubs handling large traffic volumes:

- An important role in mitigating DDoS attacks:

- “Real-world” infrastructures with a plethora of research opportunities: Studying this peering ecosystem, the end-to-end flow of network traffic, and the traffic that traverses these facilities can help us understand how the Internet landscape is changing.

- IXPs are active marketplaces and technology innovation hubs: Most notably are DDoS mitigation and SDN-based services



How are IXPs important in DDoS
They can observe the traffic to/from an increasing number of participant ASes. In this role, IXPs can play the role of a "shield" to mitigate DDoS attacks and stop the DDoS traffic before it hits a participant AS.


Why do networks choose to peer at IXPs?

- they are keeping local traffic local. In other words, the traffic exchanged between two networks do not need to travel unnecessarily through other networks if both networks are participants in the same IXP facility.

- Lower costs. Typically peering at an IXP is offered at a lower cost than relying on third parties to transfer the traffic, which is charged based on volume.

- Network performance is improved due to reduced delay.

- Incentives. Critical players in today’s Internet ecosystem often “incentivize” other networks to connect at IXPs. For example, a prominent content provider may require another network to be present at a specific IXP or IXPS in order to peer with them



What services are offered at IXPs?

Public peering: two networks use the IXP’s network infrastructure to establish a connection to exchange traffic based on their bilateral relations and traffic requirements.

Private peering: allows direct traffic exchange between the two parties, and doesn’t use the IXP’s public peering infrastructure. commonly used when the participants want a well-provisioned, dedicated link capable of handling high-volume,

Route servers and Service level agreements: 

Remote peering through resellers: Third parties resell IXP ports wherever they have infrastructure connected to the IXP.

Mobile peering: scalable solution for the interconnection of mobile GPRS/3G networks.

DDoS blackholing: customer triggered; dallows users to alleviate the effects of DDoS attacks against their network.

Free value-added services: like Internet Routing Registry (IRR), consumer broadband speed tests9, DNS root name servers, country-code top-level domain (ccTLD) nameservers



bilateral BGP session

- two ASes exchange traffic through the switching fabric utilize a two-way BGP session

- Because rising number of BGP sessions this option does not scale with many participants


How does a Route Server (RS mitigate Bilateral BGP Session)

- collects and shares routing information from its peers or participants of the IXP that connect to the RS.

- executes its own BGP decision process and re-advertises the resulting information (e.g., best route selection) to all RS's peer routers.


How does a route server (RS) maintain multi-lateral peering sessions?

-


Route servers maintain two types of route filters what are they
Import filters are applied to ensure that each member AS only advertises routes that it should advertise.

export filters are typically triggered by the IXP members themselves to restrict the set of other IXP member ASes that receive their routes.



Example where AS X and AS Z exchange routes through a multi-lateral peering session
1. In the first step, AS X advertises a prefix p1 to the RS, which is added to the route server's RIB specific to AS X.

2. The route server uses the peer-specific import filter to check whether AS X is allowed to advertise p1. If it passes the filter, the prefix p1 is added to the Master RIB.

3. The route server applies the peer-specific export filter to check if AS X allows AS Z to receive p1, and if true, it adds that route to the AS Z-specific RIB.

4. Lastly, the route server advertises p1 to AS Z with AS X as the next hop.