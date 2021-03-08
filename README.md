# Calico ACI Integration

This repo documents my steps to deploy a calico Cluster Integrated with ACI.
I use Terraform to deploy the ACI configuration and spin up the required Virtual Machines.

## ACI L3OUT design

The Calico cluster communicates with the ACI fabric via an External L3OUT.
In order to simplify the configuration and support Virtual Machine Mobility the design will adopt use the floating L3OUT feature.

### Floating L3 OUT Introduction

The  floating L3Out feature enables you to configure a L3Out without specifying logical interfaces. The feature saves you from having to configure multiple L3Out logical interfaces to maintain routing when virtual machines (VMs) move from one host to another. Floating L3Out is supported for VMware vSphere Distributed Switch (VDS) with ACI 4.2.(1) and physical domains starting from ACI 5.0(1)

In order to keep the design as flexible as possible and not to dictate the Virtualisation Technology adopted the physical domain approach will be the one used even if the virtualisation environemnt is based on VMware. This is particularly convenient as will allow the user to mix of different Virtualisations and Bare Metal servers at the same time.

For more details on Floating L3 Out refer to the [Cisco ACI Floating L3Out](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/kb/Cisco-ACI-Floating-L3Out.html) documentation.

Terminology refresher:

* Anchor Node: Are the routers where the routing peering is formed. There is no requirement on the number  of leaf switches acting as the anchor leaf node. As of ACI 5.1(3) an ACI leaf can have up to 400 BGP sessions.

* Non-anchor Node:  The non-anchor leaf node does not create any routing sessions for L3Out peering. It acts as a passthrough between the anchor node and the L3Out router. A non-anchor leaf node has the floating IP address and can have a floating secondary IP, if needed.. If it is a VMware vDS VMM domain, the floating IP address is deployed only when the virtual rotuer is connected to the leaf node. If it is a physical domain, and the leaf port uses AEP that has an L3Out domain associated to the floating L3Out, the floating IP address is deployed. The floating IP address is the common IP address for non-anchor leaf nodes. It is used to locate the router virtual machine (VM) if it moves behind any non-anchor leaf node through the data path.

* Floating IP: A common internal IP for non anchor leaf nodes to communicate with anchor leaf node.

### Floating L3 OUT Design

The design choices for the floating L3OUT are as following:

* Physical Domain: The Floating L3 OUT VLAN will be deployed on all the ports that are associated with the Physical Domain. Be carful if you choose to re-use a physical domain as you might end up with the Floating L3 OUT VLAN deplouyed on ports that are not connected to your Calico Nodes.
* Two Anchor Ndoes: A single border leaf can handle up to 400 dynamic routing adjagencies. This allow use to deploy up to 400 Calico Nodes per pair of Anchor Nodes. If more than 400 nodes are required we will instantiate a new set of Anchor nodes to spread the load.
* Non-Anchor nodes: This depends only on the rack layout and VM/BM spread.

## Terraform Configuration Variables for ACI

TBD
