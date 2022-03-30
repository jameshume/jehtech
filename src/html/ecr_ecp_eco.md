There are two distinct entities here, which have been conflated by similar language:
•	A **Change Request**, which typically comes from a customer or product owner, and is a request for requirements change, typically on a project. Legally and effectively this is a contract change (since the requirements are a normative reference from the contract that defines the project). The fact that CWMD calls them ECRs is just confusing. A **Change Proposal** is then a response to a **Change Request** from the supplier proposing an implementation of the requirements change, together with a cost and timescale.
•	An **Engineering Change Request** can be thought of as a request to make a change to a Product. The response to an ECR is an **Engineering Change Order**, which may or may not change the requirements, but does change the configuration of one or more deliverables (it could be just a replacement part due to obsolescence, for example).

So from a software perspective, a customer or product manager can make a **Change Request** to alter the requirements of a project in flight, or initiate a new project to (for example) add features or fix bugs in a product.

If the corresponding **Change Proposal** is accepted, it will typically involve at least one **Engineering Change Request**, since it will normally change the deliverable configuration of the product (but see below). However, the **Change proposal** can result in zero, one or more than one **Engineering Change Order**.

To numerate the extremes:
•	If the **Change Proposal** only results in additional testing (say to pass a new test standard), it will not require an **ECO** at all.
•	If the **Change Proposal** contains a shopping list of changes that affects to hardware, software and firmware, several **ECOs** may be generated.

The way this is normally handled is with a **Systems** approach: boundaries between disciplines are managed as separate sub-contracts under a main project umbrella, and the dependencies between the sub-contracts are defined and baselined. It sounds bureaucratic, but internal sub-contracts can be very simple, and it allows for different disciplines to use their own best practices, without being forced into one-size-fits-all processes, which are ultimately inefficient and self-defeating.

A Systems approach also handles another weakness frequently exposed by projects in this company: from the top down, the **Stage and Gate** process looks like it will structure and organise a large project effectively; In practice, unless a Systems approach is adopted, PDR and CDR gates are effectively impossible to pass, because there is no way to validate the disciplinary boundaries (like Software/Hardware) until integration testing, by which time it is far too late.

Copious examples are available, if required.
