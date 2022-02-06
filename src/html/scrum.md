## SCRUM

* Follows the Agile Manifesto:
    * 4 Values
    * 12 Principles
* Agile is a *framework*, scrum is an agile *METHODOLOGY*.
* Value-driven life cycle: prioritise work by business value - do most valuable work first.
    * Provides best return on investment (ROI) possible to stakeholders.
    * Incremental build and deployment lets stakeholders evolve requirements and check right thing built.
    * However, could be more risk focused.
* Empowerment and business buy in are fundamental success factors.
* Critisisms of pure scrum:
    * Budget risk - dont have good visibility of everything that needs to be done from the onset.
    * Scope creep - change from time to time, risk of scope creep - difficult for people to focus.
    * Not for every project.
    * Does not scale well.
        * The output does not have any give - its all or nothing.
        * Or if big design up front needed like construction projects or data center migration project - difficult fit maybe.
    * Risk - will business accept it.
* https://www.atlassian.com/continuous-delivery/software-testing/types-of-software-testing
* Pillars = TIA:
	1. Trasparency
	2. Inspection
	3. Adaptation
* Ceremonies (Events):
    * Sprint Planning
    * Daily Scrum
    * Sprint Review
    * Sprint Retrospective
   
### Good References
* [The Agile Manifesto](https://agilemanifesto.org/)
* [The Scrum Guide](https://scrumguides.org/scrum-guide.html)

[An amazing SO thread on sprints and "failures"](https://pm.stackexchange.com/a/18228), quoted
below:

> TL;DR
> They have decided that if there are any User Stories not fully completed (as per the DoD) 
> at the end of the Sprint, the Sprint has failed.
> 
> This is not only incorrect, it's an abuse of the Scrum framework and a thorough
> misunderstanding of how work is selected for inclusion into a Sprint.
> 
> The purpose of a Sprint is not to complete user stories. That's simply a means to an end. 
> Rather, the purpose of a Sprint is to provide a time-box to work on Product Backlog items 
> that collectively deliver the value defined by an overarching Sprint Goal.
> 
> Sprint Failure Conditions
> While not addressed specifically within The Scrum Guide, a Sprint really has only three failure conditions:
> 
> The Sprint Goal has not been met.
> The delivered Increment is not in usable condition.
> The Increment does not meet the "Definition of Done."
> That's it. Individual stories can be done or not-done, forecasts (estimates) can be missed, and 
> the team may have successfully delivered the wrong MacGuffin. Such Sprints are still technically 
> "successful" in that they delivered a potentially-releasable Increment and leveraged the framework
> to provide the business with process transparency and appropriate opportunities to inspect-and-adapt.
>
> Sprint Goals and Increments
> The following elements of the Scrum framework are explicitly defined in The Scrum Guide. The Sprint
> Goal is developed during Sprint Planning, and provides guidance throughout the Sprint. The Increment
> is the work completed according to the Definition of Done, and is essentially the de facto
> deliverable for the Sprint.
>
> Sprint Goal
> The selected Product Backlog items deliver one coherent function, which can be the Sprint Goal.
> The Sprint Goal can be any other coherence that causes the Development Team to work together
> rather than on separate initiatives.
>
> Increment
> At the end of a Sprint, the new Increment must be "Done", which means it must be in useable
> condition and meet the Scrum Team’s definition of “Done.” It must be in useable condition regardless
> of whether the Product Owner decides to actually release it.
> 
> Educational Opportunities
> In general, your management team's approach is exhibiting a number of smells that indicate a faulty
> Scrum implementation. It is the Scrum Master's job to educate the entire organization, including
> the Scrum Team and senior management, about the way Scrum actually works.
>
> Specifically, you should use this as an opportunity to address the following project smells
> implied by your original post:
> 
> A Sprint should have a coherent goal.
> 
> As defined by the Scrum Guide, each Sprint should have a defined goal which causes the team to
> work together rather than on separate initiatives. If you don't have a coherent Sprint Goal, a
> coherent Increment, or a collection of Sprint Backlog Items that are interrelated, then the
> framework is being implemented incorrectly.
> 
> Work is selected by the Scrum Team, not assigned from the outside.
> 
> The Product Owner prioritizes work on the Product Backlog, and the team negotiates with the
> Product Owner during Sprint Planning to select stories for the Sprint Backlog that will:
> 
> Fit within the time box.
> Support the Sprint Goal.
> Collectively deliver a vertical slice of value.
> Assigning stories to the team, selecting unrelated stories, or failing to leverage the "team"
> aspect of the Development Team >when performing Sprint Planning are all huge red flags.
> 
> Forecasts are not money-back guarantees.
> 
> Sprint Planning is a short-term planning exercise that estimates both level-of-effort and team capacity
> to arrive at a reasonable forecast of the work that can be completed within a given time box (the Sprint)
> with the resources and knowledge currently available. Forecasts can be missed for a wide variety of
> reasons; it is not inherently a failure of either the framework or the team's work during the iteration.
> Instead, a missed forecast is an opportunity to:
> 
> - Learn more about the problem domain.
> - Inspect-and-adapt the framework or development process.
> - Improve estimating techniques.
> It is more effective to iterate rather than to affix blame.
> 
> If your organization is trying to "hold people accountable" for forecasts, they have misunderstood
> the difference between an estimate and a guarantee. Educate them about how iterative development and
> iterative process improvement actually work, and explain how the Scrum framework provides them with
> the tools they need to effectively manage emergent designs and processes.


## Roles
### Product Owner (PO)
* Product owner == business owner, who's responsibility is Optimizing the business value of the work
    * Prioritised the backlog.
    * Captures requirements.
    * Don't need to understand all technical details.


* One person.
* Represents the business & customer in the scrum team.
* Provides vision & day-to-day steers - directs development team.
* Responsible for accomplishment of deliverables at each project stage/increment.
    * S/he defines the following:
        * Product features
        * Release date
    * And is responsible for:
		* Prioritising features
		* Developing and maintaining product backlog
    		* Changes must be approved by PO
		* Making decisions on behalf of customer/business
		* Accepting/Rejecting work
* Must attend sprint planning and review at a minimum

### Scrum Master (SM)
* Promotes scrum values and coaches team. Ensures all following scrum practices.
* Serves PO and SDT
* Facilitate events/ceremonies
* **It is the Scrum Master's top priority to remove impediments.**
* Process Expert
	* Verify test cases - benificial? Needs to be reviewed by someone, e.g. someone close to requirements.
  
#### How as a scrum master can we ensure the values?

Commitment:	Are people attending daily standups and other ceremonies, taking part in discussions/collaboration, etc.

* Focus:	
    * Daily standup. Collaboration between entire SDT.
    * Limit the number of tasks placed on each team member to ensure they are setup to proceed.
    * Are goals SMART? INVEST?
    * Ensure everyone knows what their roles and responsibilities are.
* Courage:
    * Demoing regularly, asking for help, taking part in discussions/collaboration.
	* Foster envionment where courage is applauded not shot down - e.g. its ok to ask for help.
	* Promote honest feedback - attack the idea/problem not the person.
	* Be empowered to push back if "too much to eat".
* Openness:
    * The scrub board is viewable by all.
	* Turn feedback into change.
	* Foster envionment where courage is applauded not shot down - e.g. its ok to ask for help.
	* Promote honest feedback - attack the idea/problem not the person.
* Respect:
    * A problem is the TEAM's problem not an individual's. Team empowered to self organise.

Feedback:

* How to ask for feedback:
    * Don't ask for honesty
    * Ask them what they need (focus on them)
    * Don't talk about yourself (dont make their review about you)
* How to respond to feedback:
    * Don't explain, argue, or rationalize - don't try to get them to see your side –
      this tells them their feedback is not welcome or valuable.
    * Believe them
    * Get details
    * Thank them
* How to act on feedback:
	* If one person said it, assume that others agree
	* Turn feedback into change
	* Be patient


## Sprints
A sprint is a *timeboxed* duration that can*not* be extended. It defines an increment of a product, in that
it has a clear *goal*, which ensures that at the end of the sprint some feature is delivered that adds to existing
functionality.

![Sprint structure and timings](##IMG_DIR##/scrum_sprint_cememony_timings.jpeg.jpg)

A sprint has the following ceremonies:

1. Planning
2. Daily scrums
3. Review
4. Retrospective

Is the output of each sprint deployable?

### Planning
* Attended by PO, SM, SDT
* 3 things to consider:
    1. Capacity - Finding the availablility of the team.
    2. Scope - Set the goal: *Why is this Sprint valuable?
    3. Estimation - Task breakdown and assignment etc.
       1. The requirements for the sprint and each task must be fully understood by the SDT.
       2. Tasks must be INVEST/SMART
       3. What can be Done this Sprint and how will it get done?
          1. Definition of *Done* decided and applied.

The "Definition of *Ready*" applies: is the team ready to start the sprint? Are all requirements fully understood? Does every task
have an estimate against it?

### Daily Scrum
* During the daily Scrum, The Product Owner's participation is defined by the team.
* Timebox to 15 minutes - approx. 2 minutes per team member.
* Format:
    * What did I do yesterday to help meet the Sprint Goal
    * What do I plan to do today to help meet the Sprint Goal
    * What individual or Team impediments might prevent us from meeting the Sprint Goal
* Progress visible to all on the *work board*.

### Scrum Artifacts
1. Product backlog
	* ** This is MANAGED BY THE PRODUCT OWNER **
	* Its the PRL, maintained by the product owner based on:
		* Risk
		* Business value
		* Dependencies
		* Timescales
	* Features added normally in user story format
	* WHAT will be built
	* ** Open and editable by anyone but PRODUCT OWNER is responsible for ordering it. **
	* Rough estimates of business values and development effort, e.g. using story points.
	* ** Product refinement/"grooming" <= 5 - 10% of teams capacity **
	* When Resource planning:
		1. Work Breakdown Structure: Divide task into sub tasks
		2. Basing requirments on past projects or industry standards
		3. Using the scope statement of the project to estimate resource needs
		4. Creating a resource plan to specify the resources needded in different categories.
2. Sprint backlog
	* ** This is MANAGED BY THE TEAM **
	* Not mandatory commitment.
		* Is a prediction of work that will be completed
		* Distinction exists to create a less stressful work environment - take only what you
		  can eat.
	* Work is not assigned - any team member can pick up a ticket - team should be self motivated to
		pick their tasks.
	* Backlog can be updated when important information comes to light but in general the sprint
		should be FIXED. Any one can change the sprint but the SCRUM MASTER MUST APPROVE and
		depending on bredth of scope the PRODUCT OWNER may also have to.
	* Servant leaderhip is a philosophy and a practice. Servant leader looks to the needs of people
	around them attempts to fix or solves their problems, promoting personal development.
		* Should have these qualities:
			* Forsight
			* Vision
			* Transformation
			* Awareness
		    * Empathy
		    * Persuasion
		    * Listening
		    * Team Growth
			* Stewarship
			* Building continuity
	* A good leader needs to understand themselves.
	* All Sprint Backlog Items are "owned" by the entire Development Team, even though each one
	may be done by an individual team member. 
3. Increment



### Report Out Session
- Product owner, scrum master, business analysis, SDT for ONLY 20 minutes max
- SDT take < 5 minutes each and demo their work.
- Gives a sense of responsibility so micro managemement is not required on a daily basis.
- How is this different from the review meeting?
- Review meeting is scrum master and product owner and just the most senior developer.
- Review meeting is when the Scrum Team and stakeholders inspect the outcome of the
    Sprint and figure out what to do in the upcoming Sprint

## Estimation

* Finding out how much time we think it will take to complete a task: Comparisons against a "norm"
* High level estimates are TOP DOWN.
* Sprints and tasks are often BOTTOM UP.
* Estimate by consensus - e.g. planning poker, t-shirt sizing, fibonacci
* Estimate only to the level of detail necessary.

### User stories
<pre style="border: 0;">
Theme						- Features are grouped into logical groups.
    Feature					- Describe a high level portion of final product.
        Epic				- High level requirements to be decomposed into user stories.
            User story		- Requirements that describe a single action.
                Task		- Detailed decomposition of user story into steps.
</pre>

User stories should use *INVEST* model:

* **I***ndependent*
	* Should be self-contained - no dependencies on other stories, as far as is possible
* **N***egotiable*
	* Until they are part of an iteration can always be changed and re-written
* ***V**aluable*
	* Must deliver value to end user in aligment with business goals
* **E***stimatible*
* **S***ized appropriately*
	* Should not be so big as to become impossible to plan/task/prioritise with a certain level of
	certainty
* **T***estable*
	* The story and description must procide enough detqail to make test development possible.

Should also be *SMART*:

* **S**pecific (simple, sensible, significant).
    * *What* do I want to accomplish?
    * *Why* is this goal important?
    * *Who* is involved?
    * *Where* is it located?
    * *Which* resources or limits are involved?
* **M**easurable (meaningful, motivating).
    * How much?
    * How many?
    * How will I know when it is accomplished?
* **A**chievable (agreed, attainable).
* **R**elevant (reasonable, realistic and resourced, results-based).
* **T**ime bound (time-based, time limited, time/cost limited, timely, time-sensitive).


## Burn-down/Burn-up charts/Risk-burn-down charts:
* Burn-down:
	* Core project management tool in Scrum
	* A graphical representation of work to do against time left, often showing idea time too.
  	* Helps predict liklihood of completing on time.
  	* Number of story points completed per sprint is the teams *velocity*.
  	* Can be at the sprint *and* epic level (kind of a burndown of burndowns).
  	* Actual-work line above ideal-work line => behind schedule
  	* Actual-work line below ideal-work line => doing better than expected
	


## Kanban v.s. scrum

## Minimal Product Definitions
### MVP - Minimum Viable Product
The "must haves" == the MVP

### MLP - Minimum Loveable Product
The "must haves" and the "should haves" perhaps.

### MMP - Minimum Marketable Product
The version of the completed project that provides enough value to consumers to order to be commercially sucessful at market.
This is normally "must haves" and "should haves"
	Can have several MVP iterations as interative prototypes for reaching the MMP threshold.
	

## Definition of Done (DoD)
According to [Scrum.org](https://scrum.org):

> a definition of done (DoD) is a shared understanding of expectations that the current sprint 
> (or increment) must meet in order to be released to users.

* Benefits / Purpose [[Ref]](https://plan.io/blog/definition-of-done/):
    * Building a common understanding within the team about quality and completeness.
    * Providing a checklist of criteria to check user stories against. 
    * Ensuring that the increment shipped at the end of the sprint meets the quality level that your 
    	team and the project owner agreed upon. 
    * Makes shared understanding of "complete" visible to all - pool of shared knowledge/understanding.
    * Strong base to deliver increments.
    * Build in quality at each step.

* All acceptance criterias are met,
    * A checklist that defines what's needed for an increment to be releasable at the end of a sprint. 
    * Note: DoD is global but acceptance specific to task
    * DoD is different depending on whats being designed.
    * Should be clear, testable, concise and realistic.

* Different definitions will affect the estimates and then work in the sprint plan,
* Scrum team should come together to define this,
 
* Example DoD list:
    * Code peer reviewed
    * Unit test passed
    * Functional tests passed
    * Non-functional tests pass / requirements met
    * Acceptance criteria for each issue met
    * Continuous Integration build passing
    * Documentation updated
    * Product owner accepts the User Story

* DoD v.s. acceptance criteria:
    * DoD is *global*, acceptance unique to the user story.

## Definition of ready (DoR)
* Defines what a piece of work needs to have in place before work can start on producing it,
* Should be collaboratively created and agreed by the SDT,
* Living document - can evolve with team,
* Do the tasks follow the INVEST model?
* Other common questions:
	* Are the acceptance criteria agreed and understood?
	* Are estimates agreed?
	* Is the testing strategy agreed?
	* Are the items [[Ref]](https://agility.im/frequent-agile-question/what-is-a-definition-of-ready):
    	* *Actionable* – Is the item immediately actionable (doable) by the team? Do the team know what they need to do, and can they do it now? Is the item free from external dependencies?
        * *Refined* – Has the item been through a process of refinement before sprint planning? Is there a common understanding amongst the team on what the item is and how it will be implemented?
        * *Valuable* – What is the business value of the item? What is the value to the end user? Is the value clear to everyone on the team?
        * *Estimated* – Has the item been estimated by the team? And, is the item agreed to be of a size that the team are comfortable can be completed within a sprint?
        * *Testable* - Acceptance criteria – Has the item got clear acceptance criteria?
        * *Demoable* – Do the team understand how they might demo the item or discuss it in the sprint review once complete?

## Durations
* Scrum duration 15 minutes
* Max sprint duration is 1 month
	* Review 4 hrs
	* Retro 3hrs
	* Plan 1 day (in a 4 week sprint)
    * For 2 week sprint just half everything.
* For every week of sprint to a max of 2 hours of planning
* For every week of sprint do 1 hour review
* For every week of sprint fo 45 minutes of retro.
* Review - 1 hour for each week in pstring
* Retro - max 1.5 hours for 2 week sprint
