## SCRUM

* Follows the Agile Manifesto:
    * 4 Values
    * 12 Principles
* Agile is a framework, scrum is an agile METHODOLOGY
* Product owner == business owner, who's responsibility is Optimizing the business value of the work
* SDT - Built and test the product
* Scrum master: Process Expert
	* Verify test cases - benificial? Needs to be reviewed by someone, e.g. someone close to requirements.
* Empowerment and business buy in
* Budget risk - dont have good visibility of everything that needs to be done from the onset.
* Scope creep - change from time to time, risk of scope creep - difficult for people to focus.
* Risk - will business accept it.
* Is is suitable for every project?
* Is the output of each sprint deployable?
* Does not scale well.
    * The output does not have any give - its all or nothing.
    * Or if big design up front needed like construction projects or data center migration project - difficult fit maybe.
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


## How as a scrum master can we ensure the values?

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

**It is the Scrum Master's top priority to remove impediments.**

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
* Increment - Some feature that you add to the existing functionaility.
* Sprint cancellation - If product becomes obsolete, for example. Or the business case is no longer valid.
    * Product owner must approve this!
* Sprint Goal - The object of the sprint - what is meant to be achieved at the end of the sprint.
* Sprint planning - 3 things to consider:
    1. Capacity - Finding the availablility of the team
    2. Scope - setting the sprint goal
    3. Estimation -task breakdown and assignment etc.
* During the daily Scrum, The Product Owner's participation is defined by the team.
* Scrum Artifacts
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
        * <pre style="border: 0">
+---------------------------------------------------------+
| vv The product backlog vv                               |
+---------------------------------------------------------+
|Sprint backlog  Requirement  }                           |
|                Requirement  } Ready for sprint          |
|                ...          }                           |
|                Requirement  }                           |
|---------------------------------------------------------+
|Groomed         Requirement  }                           |
|                ...          } User stories              |
|                Requirement  }                           |
|---------------------------------------------------------+
|Future          Requirement  } EPIC stories              |
|                ...          } to be broken down later   |
+---------------------------------------------------------+</pre>
		* When Resource planning:
			1. Work Breakdown Structure: Divide task into sub tashs
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


Key techniques:

* Estimating
* User Stories
* Kanban Board
* Definition of *Done*
* Definition of *Ready*
* MoSCoW
* Retrospectives
* Estimating
* Burn Charts
* Team Board\Information Radiators

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


## Burn-down/Burn-up charts/Risk-burn-down charts:
Burn-down:
	Core project management tool in Scrum
	A graphical representation of work to do against time left
	


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
* All acceptance criterias are met,
* Different definitions will affect the estimates and then work in the sprint plan,
* Scrum team should come together to define this,
* According to [Scrum.org](https://scrum.org), a definition of done (DoD) is a shared understanding of expectations that the current sprint (or increment) must meet in order to be released to users.
* Purpose [[Ref]](https://plan.io/blog/definition-of-done/):
    * Building a common understanding within the team about quality and completeness.
    * Providing a checklist of criteria to check user stories against. 
    * Ensuring that the increment shipped at the end of the sprint meets the quality level that your team and the project owner agreed upon. 
* Example DoD list:
    * Unit test passed
    * Code reviewed
    * Acceptance criteria for each issue met
    * Functional tests passed
    * Non-functional requirements met
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
