## This is a brief guide to ZenHub

If you want to learn more, I recommend you check out the PDF file on project management
included in this directory.

All guidelines below are adapted from this [link](https://help.zenhub.com/support/home).

This guide includes:
1. Kanban board
2. Milestones
3. Issues
4. Labels
5. Filtering

------------

### ZenHub's Kanban Board

It consists of 7 pipelines (individual panels):

1. __New Issues__ - Wait for scrum master to prioritize and categorize

2. __In Progress This Week__ - issues that need to be done by the milestone for the
    current week. Prioritize by the position. The top is the most important.
    The bottom is not as important as the top.

3. __Upcoming Low Priority__ - Future issues that are low priority should be placed
    here. Issues here should be prioritized top-to-bottom in the pipeline.

4. __Upcoming High Priority__ - Future issues that are high priority should be placed
    here. Issues here should be prioritized top-to-bottom in the pipeline.

5. __Review Q/A__ - Issues or code that are ready to be tested and reviewed by
    other team members should be placed here.

6. __Done__ - Issues or code that are tested and done. This is to keep track of what
    has been done in the past. Issues should be ordered chronologically.

7. __Closed__ - This tab records closed pull requests. (We can decide if we want to
    get rid of this pipeline).

Proposed basic workflow is:

* all new issues go to new issues (unless exception applies)
* tasks that __must be done this week__ goes to 2. 2 should only have issues to be focused on this week.
* tasks that are not due the current week's deadline should go in 3 or 4
* issues that are done should be moved to 5 or 6. That means issues that are in progress
this week, once done, should be migrated to 5 or 6
* issues that were not done by the deadline of the week (leftovers) should stay in 2 and should be moved
to the top

------------
### Milestones

Scrum's sprints are GitHub/ZenHub's milestones. This corresponds to our weekly
goal. Some of us might question: what are epics then? Epics are a "theme" of work.
They are broader than milestones. One epic can have many milestones.
For this project, we only have one Epic. Milestones are used to keep track of the
progress of the project. Think of it as deadlines. Read more [here](https://help.zenhub.com/support/solutions/articles/43000500256-getting-started-with-milestones)

__To create new milestones:__

1. Go to ZenHub board

2. There's is "+" plus sign next to New issue. Click.

3. Select "new milestone"

4. Add title, select start date and end date (which should corresponds with Monday
  and Friday of the week or our weekly deadline/meeting date) and a brief description.

__To view all milestones or delete milestones:__

1. Go to GitHub's Issues tab

2. On the top right, left of the search is the Milestones tab. Click.

3. You can view all existing milestones here and select the one you want to delete.

__Add issues to milestones:__

1. Go to ZenHub's Board

2. Hover your mouse on one of the issues until you see a box with three vertical dots.
Click and click select issues. Now you can click other cards too.

3. A tab with "Set Milestone" will appear on the top right. Click and select the right
milestone.

4. Click "Apply changes."

To clear milestones from issues. Just select the issues. Click "Set Milestone."
Click "Clear milestones from issues"

------------
### Issues

__To create new issues:__

1. Go to ZenHub Board

2. Click "New Issue" on the top right corner. Always add the following

  * Issue title - This must be telling and short like "Get data - research BigQuery"
    or "Get data - download from torrent"

  * comments - not required if it's not necessary. Here's the best place to detail
    granular steps you want to take to achieve this issue.

  * Pipelines - not required. Can leave it as it and wait for scrum master to prioritize. If you know
    how to prioritize it (which pipeline it should go in), feel free to select
    the right one as well.

  * Labels - Must select! Very important for filtering issues. Always include (1) one label
    indicating priority (2) one label indicating how hard it is. (3) one label indicating
    which step of the project the issue belongs to (such as "data retrieval", "analysis").
    Use your judgement. You can also use other labels to indicate related issues like bugs, help wanted etc.
    See below.

  * Assignees - Must select! Very important for filtering issues. Can add as many people
    as you want.

  * Milestone - not required. Can leave it as it and wait for scrum master to do. If you know
    which milestone it should go in, feel free to select the right one as well.

3. Click submit new issue.

__To close issues:__

1. Go to ZenHub Board

2. Hover your mouse on one of the issues until you see a box with three vertical dots.
Click and click close issue.

------------
### Labels

Our issues will be driven by labels. Here's a proposed system:

Labels are grouped into 4 categories:

1. Priority - 3 priorities:
  * High Priority - These are issues that must be done in sequence or must meet the deadline soon.
    For instance, data cleaning is high priority because other work can't be done until this issue is solved.
  * Medium Priority
  * Low Priority - These could be issues that can be done independently or it doesn't need to be done very early.

2. Complexity - How hard is the task? 3 levels: Difficult, Medium, Easy.

3. Major tasks in the project - Here're what to start with (we can add more as we go):
  * data retrieval
  * analysis - we might break this down in the future
  * visualization
  * writeup
  * presentation

4. Issue specific and others - This is where issue specific labels like bug,
enhancement, duplicate, help wanted, invalid, and question belong.

__To create new labels:__

1. Go to GitHub's Issues tab

2. On the top right, left of the search is the labels tab. Click.

3. Click new labels

read more [here](https://help.zenhub.com/support/solutions/articles/43000480398-creating-github-issue-labels)

------------
### Filtering

It is quite straightforward. Can be done on the ZenHub board.

See [here](https://help.zenhub.com/support/solutions/articles/43000498508--filtering-the-board-to-see-what-matters-most-to-you)

------------
v.1 updated by Nikki (Apr. 27)
