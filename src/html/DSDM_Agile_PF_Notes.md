## DSDM (AgilePM) Website
The following notes are all based on **[The DSDM Agile Project Framework website resources](https://www.agilebusiness.org/page/TheDSDMAgileProjectFramework)**.

## High Level Overview

### RAD - Rapid App development 
  * NOT formaly specified
  * IS discussions, demos, short feedback loops
  * BUT supportablity and scalability poor - disciplines of analysis and design 
    weak and not up-front. Not big picture.

![RAD Mind Map](##IMG_DIR##/RAD_mindmap.jpeg)


### DSDM
  * Created 1994
  * Addresses problems of waterfall and RAD
  * "Mature agile"
  * Vendor-independent approach
  * Assumes 80% of solution value can be delivered for 20% of the effort that it would take to 
    produce the total solution.
  * Approach encourages detail to emerge over time

![DSDM advantages over RAD](##IMG_DIR##/dsdm_over_rad.jpeg)
![DSDM advantages over Agile](##IMG_DIR##/dsdm_over_agile.jpeg)


### Agile Manifesto
Agile - Term first used 2001 - [The Manifesto](https://agilemanifesto.org/) reads as follows:

  * INDIVIDUALS AND INTERACTIONS over process and tools.
  * WORKING SOFTWARE (SOLUTION) over comprehensive documentation.
      * Break the illusion of security and stability that comes from document driven
        processes.
      * Only need for high-level versions of these artefacts in early phases.
  * CUSTOMER COLLABORATION over contract negotiation.
      * Encourages project teams and the sponsoring business to work collaboratively
        at all times. Contracts need to reflect this.
      * Contracts are  'light touch' and 'guiding' rather than being 'detailed' and
	'prescriptive'.
  * RESPONDING TO CHANGE over following a plan.

Context:

> ...while there is value in the items on the right, we value the items
> on the left more...

It is important not to ignore processes, tools, documentation, contracts and plans but instead
to ensure that they are only created where they add value, and only to the level of detail that
adds value.

### Traditional Project Problems

Problem | Solution DSDM Offers
------- | --------------------
Ineffective communication | Poor comms means high risk of fail. DSDM emphasises *human* interaction over for e.g. emails. Use workshops, daily standups, visual techniques (modelling, prototyping).
Late delivery | Focus on delivery on time - revise scope of delivery ahead of extending deadline.
Does not meet business needs | Includes business representatives as part of SDT (solution dev team).
Wrong thing built | Enables change through iterative development.
Unused features | Keep business priorites at core and using [PRL](#prioritised-requirements-list-prl) only produce whats wanted.
Delayed / Late ROI | Incremental deliver to do most important features first.
Over-engineering | Avoid diminishing returns by producing "must haves" first "should/could haves" second/third.
"Fragile" agile | Place agile concepts in structured/controlled framework.
Pseudo agile | Only do just enough work upfront to ensure clarify and provide foundation. Avoid waterfall in disguise.

## Philosophy & Fundamentals

The DSDM philosophy is that
> best business value emerges when projects are aligned to clear business
> goals, deliver frequently and involve the collaboration of motivated and
> empowered people

An organization amenable to **incremental delivery** of solutions ***into live use*** will benefit from **early return 
on investment**. 

### Composition of DSDM
1. Common sense: 
      1. Sound judgment independent of specialised knowledge or training
      2. Practical judgment
      3. Normal native intelligence.
2. Pragmatism: action or policy dictated by consideration of the immediate practical consequences rather than by theory or dogma.
3. [Process](#dsdm-process)
4. [People](#dsdm-roles)
5. [Products](#dsdm-products)
6. [Practices](#instrumental-success-factors)
7. [Principles](#8-dsdm-principles)
8. Philosophy

<pre style="border:0;">
        PHILOSOPHY
        PRINCIPLES
   P     P     P     P
   R     E     R     R
   O     O     O     A
   C     P     D     C
   E     L     U     T
   S     E     C     I
   S           T     C
               S     E
                     S
Common sense and pragmatism
</pre>

### Project Variables
Traditional:

  * Fix Features & quality.
  * Negotiation on time and/or cost.

DSDM:

  * Fix Time, cost, & quality.
  * Negotiate on features.
    * On time and within budget but solution scope is variable. 
  * Uses MoSCoW and timeboxing.
    * Delivers MUST - **M**inimum **U**sable **S**ubse**T** for worst case scenario.
  * Right product, right time.

![DSDM v.s. Waterfall: What can be negotiated on](##IMG_DIR##/dsdm_vs_waterfall_what_can_be_negotiated.jpg)

## 8 DSDM Principles
**Designed to shape the attitude and mindset of a DSDM team**...

1. Focus on the business need.
     * Understand business priorities,
     * Create business case,
     * Ensure continuous business sponsorship/collaboration,
     * MUST via MoSCoW.
2. Deliver on time.
     * Timebox,
     * Focus on business priorities,
     * Hit deadlines,
     * Confidence through predictable delivery .
3. Collaborate.
     * Right stakeholders at right time,
     * Encourage pro-active business involvement,
     * Empower all team members on behalf of people they represent,
     * One team culture.
4. Quality is never compromised.
     * Agree quality level before development starts,
     * Ensure quality not variable,
     * Test early, continuously at appropriate level.
     * Constant review
     * Design and doc appropriately
5. Incremental build from firm foundations.
     * EDUF - **E**nough **D**esign **U**p **F**ront.
     * Reassess priorities and viability at every increment.
6. Iterative development.
     * Build business feedback into every increment.
7. Communicate continuously and clearly.
     * Informal face to face conversations
     * Daily standup
     * Workshops + facilitator
     * Visual communication: modelling/prototyping
     * Demo solution early and often
     * Document lean and tidy
     * Manage expectations at all levels
     * Honest and transparent comms
8. Control demonstrated all the time.
     * Plans visible to all
     * Meausure progress by deliverables not completed activity
     * Procative management
     * Evaluate viability based on business objectives continually
     * Approriate level of formality for tracking and reporting

**Memory peg:** 

* **I2C3** - **i**ncremental build, **i**terative dev, **c**ommunicate continuously, **c**ontrol demonstrated, **c**ollaborate.
* **BTQ**  - **b**usiness need, **t**imely delivery, **q**uality never compromised.


## Instrumental Success Factors
1. Embrace the DSDM approach,
     * Incompatible values increase risk of failure and should be addressed.
2. Effective SDT,
     * People at heart of successfull project
     * 4 team elements
         * Empowerment: Each role empowered to make descisions based on their expertise and team as a whole empowered within agreed boundaries.
                        E.g. BA should be empowered to make day-to-day decisions wihout referal to higher authorities.
                        **Manage by exception**.
         * Stability: Don't swap in/out team members over iterations.
         * Skills: Technical but also good "soft skills" like communication.
         * Size: Optimal is 7 +/- 2 people. At this size comms can be done with minimum formality, overhead, risk, and maximum benifit/ownership.
3. Business engagement - active and ongoing,
     * Commitment of business time throughout
     * Active Involvement of the business roles
     * Supportive commercial (e.g. contractual) relationship (where appropriate)
5. Interative development, integrated testing and incremental deliver,
6. Transparency
     * Build confidence in *evolving solution*. 
7. PAQ - **P**roject **A**proach **Q**uestionnaire - assessing options and risks. The questions are answered "strongly agree", "agree", "neutral", "disagree" and "strongly disagree". They include:
     * All members of the project understand and accept the DSDM approach (Philosophy, Principles and Practices)
     * The Business Sponsor and the Business Visionary demonstrate clear and proactive ownership of the project.
     * The business vision driving the project is clearly stated and understood by all members of the project team
     * All project participants understand and accept that on-time delivery of an acceptable solution is the primary measure of success for the project
     * The requirements can be prioritised and there is confidence that cost and time commitments can be met by flexing the scope of what's delivered.
     * All members of the project team accept that requirements should only be defined at a high level in the early phases of the project and that detail will emerge as development progresses.
     * All members of the project team accept that change in requirements is inevitable and that it is only by embracing change that the right solution will be delivered.
     * The Business Sponsor and Business Visionary understand that active business involvement is essential and have the willingness and authority to commit appropriate business resources to the project.
     * It is possible for the business and solution development members of the Solution Development Team to work collaboratively throughout the project.
     * Empowerment of all members of the Solution Development Teaam is appropriate and sufficient to support the day-to-day decision-making needed to rapidly evolve the solution in short, focussed Timeboxes
     * The DSDM roles and responsibilities are appropriately allocated and all role holders understand and accept the responsibilities associated with their role.
     * The Solution Development team has the appropriate collective knowledge and skills (soft skills and technical skills) to collaboratively evolve an optimal business solution.
     * Solution Development Team members are allocated to the project at an appropriate and consistent level sufficient to fully support the DSDM timeboxing practice
     * Tools and collaborative working practices within the Solution Development Team are sufficient to allow effective Iterative Development of the solution.
     * All necessary review and testing activity is fully integrated within the Iterative Development practice.
     * Project progress is measured primarily through the incremental, demonstrable delivery of business value.
     * There are no mandatory standards or other constraints in place that will prevent the application of the DSDM Philosophy and Practices on this project.

## DSDM Process

There are 6 main lifecyle phases:

![DSDM Lifecycle phases](##IMG_DIR##/dsdm_lifecyle_phases.jpeg)

1. Pre-Project.
      * Ensure only right projects started.
      * Setup up correctly based on clearly defined objective:
          * High level definition and over-arching business driver defined + top-level objectives.
      * No PM yet, generally. Done by leadership team.
      * Short!
      * **Milestone Output**: Terms of reference 
2. Feasibility.
      * Estiblish if project success likely - technical & cost-effective (business) perspectives.
      * Just enough effort to decide if foundations phase is justified. Plan to resource the foundations phase.
          * Few days or week max.
      * Creates 1 to 10 EPICS. EPIC is placeholder for set of user stories.
      * The visionary owns the business process so s/he approves the feasability phase. Is the project feasible from a business/technical perspective and cost?
      * What are the business requirements and EPICS. EPICS are the feature or functionality originating from the business - placeholders for more granular requirements generated later.     
      * **Milestone Output**: Feasibility assesment.
      * **Evolving Outputs**: Business case, [PRL](#prioritised-requirements-list-prl), [SAD](#solution-architecture-definition-sad), DAD, Delivery plan, MMAD
3. Foundations.
      * Preliminary investigation: fundamental, *not detailed*, undestanding of business need.
      * High-level business solution proposition.
      * How development and delivery will be managed.
      * *Avoid* low-level detail - avoid contraining evolutionary phase!
      * Drill down into user stories with more detailed acceptance criteria and the priorities.
	  * Flesh out the 6 docs created in feasability phase.
	  * Could be weeks. 3 - 4 weeks planning workshops. Flexible not rule.
	  * *No* development. This is just readiness and planning, understanding the MoSCoW's. Do people understand the standards? Is the tool access there? Etc.
      	  * User stories are *not* technical tasks
      	  * *Detailed* acceptance requirements. How many time boxes to complete ev dev for stage 1?
      	  * Timeboxes and length decided for first iteration.
  	  * Product Roles - RACI (Responsible/Accountable/Consulted/Informed) defined.
  	  * SDT added here. Create 100's or user stories.
      * **Milestone Output**: Foundations summary.
      * **Evolving Outputs**: Business case, [PRL](#prioritised-requirements-list-prl), [SAD](#solution-architecture-definition-sad), DAD, Delivery plan, MMAD
4. Evolutionary Development.
      * Built on firm foundations - evolve/grow the solution - converge over time.
      * The technical phase: break the user stories into technical tasks.
      * Apply iterative development, MoSCoW prioritisation, use modelling and facilitated workshops.
      * Timebox: explore low-level detail & deliver on time.
      * Feedback and demos to ensure right solution meets business needs.
      * **Milestone Output**: Timebox review record.
      * **Evolving Outputs**: Business case, [PRL](#prioritised-requirements-list-prl), [SAD](#solution-architecture-definition-sad), DAD, Delivery plan, MMAD
5. Deployment.
      1. Assemble.
           * Make sure deliverable is coherent. E.g. gather supporting information. 
      1. Review.
           *  Approval to deploy.
           *  SDT does *retrospective* for incrment.
           *  Retrospective + formal feview feedback into *project review report* to help guide next increment.
      2. Deploy.
           * Solution deployed into *active* use.
           * Final end-to-end testing during Deployment allows for the testing of back-out procedures.
           * **Milestone Output**: Project review report.
6. Post-Project.
      * Checks how well the expected business benefits have been met
          * Immediate and over a pre-defined period of live use.
      * **Milestone Output**: Benefits assesment.


The lifecycle phases are split into business (red), technical (green) and management (blue) and produce products that document
each stage and can be either milestones or evolving in nature:

![DSDM Lifecycle and products](##IMG_DIR##/dsdm_processes_and_products.jpeg)



## DSDM Roles

* Self-organising, empowered teams that:
    * Respect each other's knowledge, experience, skills and opinions,
    * Take personal responsibility,
    * Have courage to challenge & improve ways of working & collaborating.
* Role not necessarily one person.

![DSDM roles](##IMG_DIR##/dsdm_roles.jpeg)

### Business Sponsor (BS)
* Most senior business level role.
* Responsible for:
    * Business case,
    * Budget,
    * Funds and resources made available as needed,
    * Ensure managing by exception effective and rapid,
    * Empower business roles,
    * Keep self informed of progress and issues. E.g. attend demos.
    * Budget for feasibility investigation
    * Return on investment.
* Project champion
* Person with budget for the feasibility investigation.
* Must be senior enough to resolve financial and business issues.
  
### Business Visionary (BV)
* *Single* individual - clear vision / avoid confusion.
* More involvement than BS
* Interpret needs of BS and communicate these to team - ensure represented in business case
* Ensures:
    * Solution enables benifits described in business case:
        * Ensure that the solution delivered will enable the benefits described in the Business Case to be achieved!
* Owns:
    * Deployed solution abd realisation of benifits
    * Implications of business change
    * Business based risk
* Responsible for:
    * Define business vision - what changed business will look like
        * Ensuring that requirments align with business vision.
        * Ensure delivery of the required business change successful (fit for purpose).
        * Ensure incremental delivery of business value is optimal for business as whole.
    * Communicating business vision to all
    * Monitor progress
    * Contributes to **key** requirements, desgn, review.
    * Define and approve changes to [PRL](#prioritised-requirements-list-prl)
    * Stakeholder collaboration
    * Business resource availablility to project
    * Empower business roles
    * Aritration for SDT w.r.t business differences between business need and evolving solution.

### Technical Coordinator (TC)
* Ensure solution technically fit for purpose, meets standards etc...
* Advise on tech decisions/innovations.
* Technical equivalent of BV.
* Owns:
    * Technical risks.
    * [Solution Architecture Definition (SAD)](#solution-architecture-definition-sad).
* Responsibilities:
    * Agree/control technical architecture.
    * Determine technical architecture.
    * Define technical standards and ensure development best practices applied.
    * With BA, turn business requirements into technical solution.
    * Empower techincal roles.
    * Final arbter of technical differences between SDT members.
    * Ensure incremental delivery of business value is optimal for business as whole.

### Project Manager (PM)
* High level agile-style leadership to SDT.
* Manage working environment.
* High level planning but *leaves detail to SDT members*.
* Responsibilities:
    * Ensure effective/timely comms to project governance authorities (BS, board etc).
    * High level project planning/scheduling - *not detailed - no timebox plan etc*.
    * With SDT and stakeholders, **create Delivery Plan**.
    * Manage risk and issues.
    * Empower teams.
    * Attend stand-up meetings, as appropriate.
    * Ensure project properly set up for predictable delivery of products.
    * Ensure products of the project are delivered.
      * Ensure increments are delivered, predictably within afreed budget/time constraints.

### Business Analyst (BA)
* Support project level roles
* Fully integrated with SDT
* Facilitate relationship between business and technical roles.
    * Not intermidiary - business roles need to be fully involved themselves!
* Ensures business needs modelled, analysed and correctly reflected in solution.
    * Has the skills and experience with eliciting and defining requirements.
    * Resposible for overall design of business process and organisation change.
  
### Team Leader (TL)
* Servant-leader:
    * Shares power, puts needs of employees 1st, helps people develop/perform as highly as possible.
    * Instead of the people working to serve the leader, the leader exists to serve the people.
* With team plans detail and coordinate delivery.
* Leadership, not management.
* Ideally elected by peers: Role normally overlaps with another SDT role TL performs.
* Resonsibilities:
    * Facilitate team focus
    * Ecourage full participation of all members
    * Ensure iterative development process focussed/controll - all ceremonies performed (standups, reviews, retrospectives etc).
    * Ensure testing and review scheduled and done
    * Manage risks/issues at timebox level - escalate as needed.
    * Communicate progress to PM

### Business Ambasador (BAmb)
* Represent business needs in SDT
* Significant input into [PRL](#prioritised-requirements-list-prl) during foundations, then day-to-day detail of requirements during timeboxes.
* During dev, main decision maker on behalf of business - must be empowered.
* Responsibilities:
    * Contribute to **all** requirements
    * Provide business perspective for all day-to-day decisions
    * Organise and controll buiness acceptance testing of soution
    * Create business user and support docs.

### Solution Developer
* Builds it, within the framework setup for the project (Development Approach Definition, for e.g).
* Responsible for creatin solution that satisfies requirements in PRL.

### Solution Tester
* Tests it!
* Provides testing knowledge and expertise.

### Business Advisor (Badv)
* Often peer of BAmb - only called on for specific/specialist input.
* Provide specialist input into relevant requirements, day-to-day decisions
* Speicalist advice/help to develop business user/support docs & deployment.

### Technical Advisor (TA)
* Suport SDT with specialist technical input. Requirements/design/review sessions etc.
* Provides specific input to the project from the *perspective of those who will maintain* the solution.

### Workshop Facilitator (WF)
* Manage workshop process and catalyst for prep and comms.
* Reponsible: organise and facilitator sessions.
    * Agree scope, plan, engage, review, distribut results.
* Independent of desired workshop outcome.
  
### DSDM Coach (DC)
* Providing detailed knowledge and experience of DSDM
* Good for team that has limited experience of using DSDM

## DSDM Products

![DSDM Lifecycle and products](##IMG_DIR##/dsdm_processes_and_products.jpeg)

### Terms Of Reference
* Milestone product
* High-level definition of over-arching business drivers & top-level objectives.
* Scope and justify feasablity phase.
* Governance product: prioritise project within portfolio.

![Who produces, approves and uses Terms Of Reference](##IMG_DIR##/dsdm_terms_of_reference_people.jpeg)

### Business Case
* Evolutionary product.
* Vision and justification for project.
    * Vision describes changed business as expected to be at end and incrementally.
* Justification == *investment appraisal*.
* Outlined in feasability.
* Basis for development at end of foundations.
* Formally reviewed at end of each invrement to determine if continue.

![Who produces, approves and uses Business Case](##IMG_DIR##/dsdm_business_case_people_involved.jpeg)

### Prioritised Requirements List (PRL)
* Evolutionary
* High level requirements
* High level in feasability: 1 - 10 requirements
* User stores in foundations: 10 - 100 stories
    * Baseline in foundations *demarcates scope of project*.
* Tasks in evolutionary development: may be 1000s.
* Detail (depth) emerges over time
* Scope changes (breadth), i.e. add/remove/change high level requirements needs *formal control*!

![Who produces, approves and uses PRL](##IMG_DIR##/dsdm_prl_people.jpeg)

### Solution Architecture Definition (SAD)
* Evolutionary
* High level design framework - business & technical aspects of solution.
* Detail makes solution scope clear but *does not restrict ev dev*.
* Contains *both business and technical* aspects of the solution.

![Who produces, approves and uses SAD](##IMG_DIR##/dsdm_sad_peops.jpeg)

### Development Approach Definition (DAD)
* Evolutionary
* High level definitions of things applied to ev dev:
    * Tools
    * Techniques
    * Customs
    * Practices
    * Standards
        * Describes how quality is assued - test strategy and review etc.

![Who produces, approves and uses DAD](##IMG_DIR##/dsdm_dad_peop.jpeg)
  
### Delivery Plan
* Evolutionary product.
* *High*-level schdule of increments
    * For at least 1st itecrement timeboxes also defined.
  
![Who produces, approves and uses DAD](##IMG_DIR##/dsdm_delivery_plan_peop.jpeg)

### Management Approach Definition (MAD)
* Evolutionary product
* Defines how:
    * project organised/planned,
    * stakeholders engaged, 
    * how progress demonstrated/reported.
* Outlined in feasability and beaslined at ehd of foundations.
    * Generally not modified after.
* *CREATED BY*: PM
* *FOR*: all project participants/stakeholders
* *APPROVED BY*: BS

### Feasibility Assesment
* Milestone.
* Snapshot of solution and products at end of phase.
    * Either executive summary or baselined collection of products.
    * Each product mature enough to allow decision to continue to foundations.
* *BY*: PM
* *FOR*: Project governance authority
* *APPROVED BY*: BS

### Foundations Summary
* Milestone
* For helping to decide whether the investment in the project is worthwhile.
* Snapshot of solution and products at end of phase.
    * Either executive summary or baselined collection of products.
    * Each product mature enough to allow decision to continue to foundations.
* *BY*: PM
* *FOR*: Project governance authority
* *APPROVED BY*: BS

### Evolving Solution
* Evolutionary
* Components of final solution + intermediate deliverables exploring detail of reqs/solution
    * Components can be complete/baseline/work-in-progress
    * Can include: models, prototypes, supporting materials, test/review artefacts etc.
* At end of each increment solution deployed into live use.
* *BY*: SDT
* *FOR*: BS, Solution particicants
* *APPROVED BY*: BV, TC

### Timebox Plan
* Evolutionary
* Depth and detailfor rach timebox in delivery okan
* Elaborates on objectves for timebox and details deliverables - activities and resources req.
* Often represented as Team Board - work todo, in-progress, done.
    * Updated daily in standups
* *BY*: SDT
* *FOR*: SDT
* *APPROVED BY*: PM, TC

### Timebox Review Record
* Evolutionary
* Capture feedback from each timebox review.
    * What is acheived + feedback
    * If regulated env - formal auditable record of review compoents from expert BAs.
        * Becomes governance product in this case
* *BY*: Team Leader
* *FOR*: Governance authority, PM
* *APPROVED BY*: BV, TC (Acknowledge solution continues to be fit for purpose)

### Project Review Report
* Milestone.
* Updated at end of *each increment*.
* Purpose:
    * Capture review of solution feedback.
    * Confirm whats delivered and what is not.
    * Capture learning points from retros.
    * Describe business benefits that should now accrue.
* At end of project review report informs the project closure retrospective.
* *BY*: PM
* *FOR*: All project participants/stakeholders.
* *APPROVED BY*: BV, TC, TL

### Benefits Assessment
* Milestone
* Describes how benefits actually accrued following *period of live use*.
* *BY*: BV, BA
* *FOR*: Governance authority
* *APPROVED BY*: BS

## Workshops

## MoSCoW Prioritisation
<pre style="border: 0;">
Must have = MUST = Minimum Usable SubseT...
                   ^       ^      ^    ^
    Without no point in project - customer will reject project.
    PM or BA may challenge less obvious must haves
        - Can a requirement be broken down further
        to have a smaller must have with one or more
        should/could have.

Should have...
    Important byt not vital
    Painful to leave out - needs workarounds
Could have...
    Wanted or desirable bu less important
    Less impact if not done compared to should have.
Wont have this time...
    Will not be delivered in this timeframe.

Prioritisation
    BV and BAmb have the final say
    Start with all requirements ans wont have and then justify any
        priority increment
Business sponsor
    - Expects ALL must haves
    - Typically expects most/all should haves
    - DSDM recommends 20% contingency for could haves
        but 10% can be "more normal" sometimes.

Team needs to ask questions to relevant stakeholders to determine the priority.
</pre>

## Iterative Development

## Modelling

## Timeboxing
<pre style="border: 0">
DEMOs and end of each TIMEBOX - thats why mix MH, CH, SH in one single timebox.
Investigation -  phase is couple of hours - do we understand requirements and acceptable criteria
Refinement - iterative development and testing - dailies and burn down charts etc.
Consolidation - Try to tie up loose ends and UATs and prep for demos.

Generic def of done for timebox:
    All requirements implemented
    Code compiles cleanly
    All requirements tested
    Regression tests pass
    Code reviewed and comments addressed
    Code merged into development line

For Epic:
    All stores are complete (they meet their definition of done).
    All epic-level acceptance criteria are met, and these are listed in the epic record as complete.
    All epic-level acceptance criteria have associated tests (new or existing), which all pass.
    In source control, the epic branch has been merged with an appropriate development branch.
    Any user guides / manuals / procedures impacted by the epic have been updated
    Any maintained design documentation impacted by the epic has been updated


Generic def of ready for epics:
    Epic has been created in management solution and linked to its parent Portfolio Project
    Epic page exists in Confluence in the correct location (e.g. in the UPM 2.0 Backlog section)
    Goals of the Epic are clear
    The originators (Product Owner, Product Manager, Chief Architect) have captured all their requirements and constraints related to the epic. As a minimum, if you care about it, write it down.
    All relevant customer inputs have been captured
    Any open questions are captured, "known unknowns"
    Epic Acceptance Criteria are described... these will be used to determine if the goals of the epic have been achieved
    If the Epic involves a major architectural initiative or change this has been described in sufficient detail to allow work to progress appropriately
    The epic has been split into estimated stories 
    The Epic has been reviewed by the Product Owner and Chief Architect and any issues arising have been addressed.
    All parties are satisfied that the Epic is "Ready"

Standups
    RAID
    Risks
    Assumptions
    Issues
    Dependencies
</pre>


## People, Teams and Interactions

## Requirements and User Stories
<pre style="border: 0">
EPICS - placeholders for user stories and then technical breakdown - at feas and found levels.
	Functional
		What the solition does. What not how.
	Non functional.
		How well solition performs against defined behaviour.
		Warantee testing - security, work load etc testing

EPICS - high level acceptance criteria, which is more detailed as go into foundations.

EPICS ----> USER STORIES ----> TICKETS
Each has an acceptance criteria against which testers can perform tests.
Epic colelction of user stories linked with the business req that we received from vis phase.
Break them down into 100s of user stories in workshops which are then further broken into
tech tasks in timebox kickoffs.

USER STORIES
	Requirements to drive the project expressed from ((perspective of an end-user goal**.
	All have the same format
	3 C's
		Card, Conversation, Confirmation
		^
		Size of a sticky note with 2 or 3 lines of info based on good convo with user
		with some acceptance criteria.

		FRONT of card:
		+------------------------------------------------------+
		| (1) STK001     Customer Order (2)                    |
		+------------------------------------------------------+
		| (3) AS A: Customer                                   |
		| (4) I WANT TO: place an order                        |
		| (5) SO THAT: I can have goods deliveries to my house |
		+------------------------------------------------------+

		(1) Unique ID
		(2) Story title - clear and explicit
		(3) Role - may also be another system or component
		(4) Requirement, problem or opportunity (not the solution!)
		(5) Business value derive

		BACK of card (testing):
		+------------------------------------------------------+
		| STK001     Acceptance Criteria                       |
		+------------------------------------------------------+
		|Functional:                                           |
		|    Can I save my order and com back to it later?     |
		|    Can I change my order before I pay for it?        |
		|    Etc                                               |
		|Nonfunctional Requirements (NFRs) - Availability      |
		|   ...                                                |
		|Nonfunctional Requirements (NFRs) - Security          |
		|   ...                                                |
		| ...                                                  |
		+------------------------------------------------------+


	Follow INVEST model - BA or PM if not BA
		I Independent
		N Negotiable    - Its not a contract. It's a placeholder for stories to be negoitated.
		V Valuable      - Business visonary can help with this - Get clear direction.
		E Estimable     - Small | Medium | Large | XL - relative very course grained estimate.
		                - "T-shirt sizing" method. Top down, relative/comparative estimation.
		                - "Bucketting" method.
		                - Fibonacci numbers.
		S Small Enough  -
		T Testable      -
</pre>

## Project Planning & Control

## Tailoring the DSDM Approach

