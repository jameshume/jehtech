<style>
    .same {
        background-color: #ccffcc
    }
    pre > code {
        border: 0;
        background-color: transparent;
        font-size: 85%;
    }
</style>

![Phab object relationships](##IMG_DIR##/phabricator_projects_tasks_structure.png)

## Setup Python API With Token
To avoid storing the token in source control, keep it in a file that is part of `.gitignore` so that
it does not get committed.

```
conduit_api_data = json.load(open('conduit_token.json', 'r', encoding='ascii'))
conduit_api_token = conduit_api_data['token']
phab = Phabricator(host='https://HOST_ADDR/api/', token=conduit_api_token)
phab.update_interfaces()
```

## Tasks (The Maniphest API)
### Task Info
To search for a task there is `phab_api.maniphest.query(ids=[...])` and `phab_api.maniphest.search(constraints={'ids': [...]})`. Both return an overlapping set of information but with some annoying differences, for example, `search()` will give information about the story points for the task, whilst `query()` will not. The reason is that **`query()` is deprecated**.

<pre>
Auxillary fields removed from below:

+------------------------------------------------+-------------------------------------------------------------+
| <b>maniphest.search()</b>                             | <b>maniphest.query()</ b>[DEPRECATED]</b>                               |
+------------------------------------------------+-------------------------------------------------------------+
| List[Dict]                                     | Dict: PHID-TASK -> Dict                                     |
| [{                                             | {                                                           |
|     'attachments': {},                         |                                                             |
|     'fields': {                                |     'PHID-TASK-sff44g4bfykui2mwakwt': {                     |
<span class="same">|         'authorPHID': 'PHID-USER-...',         |         'authorPHID': 'PHID-USER-...',                      |</span>
|         'closerPHID': 'PHID-USER-...',         |                                                             |
|         'dateClosed': unix-epoch-timestamp,    |                                                             |
<span class="same">|         'dateCreated': unix-epoch-timestamp,   |         'dateCreated': 'unix-epoch-timestamp',              |</span>
<span class="same">|         'dateModified': unix-epoch-timestamp,  |         'dateModified': 'unix-epoch-timestamp',             |</span>
<span class="same">|         'description': {'raw': '...'},         |         'description': '...',                               |</span>
<span class="same">|         'name': '...',                         |         'title': '...',                                     |</span>
<span class="same">|         'ownerPHID': 'PHID-USER-...',          |         'ownerPHID': 'PHID-USER-lvc3c4gnmdu6biq5bac4'       |</span>
|         'points': '...',                       |                                                             |
|         'policy': {'edit': 'users',            |         'objectName': 'T1234',                              |
|                    'interact': 'users',        |                                                             |
|                    'view': 'users'},           |                                                             |
<span class="same">|         'priority': {'color': 'orange',        |         'priority': 'Normal',                               |</span>
<span class="same">|                      'name': 'Normal',         |         'priorityColor': 'orange',                          |</span>
|                      'value': 50},             |                                                             |
|         'spacePHID': None,                     |                                                             |
|         'status': {'color': None,              |                                                             |
<span class="same">|                    'name': 'Resolved',         |         'statusName': 'Resolved',                           |</span>
<span class="same">|                    'value': 'resolved'},       |         'status': 'resolved',                               |</span>
|         'subtype': 'default'                   |                                                             |
|     },                                         |                                                             |
<span class="same">|     'id': 11600,                               |         'id': '11600',                                      |</span>
<span class="same">|     'phid': 'PHID-TASK-...',                   |         'phid': 'PHID-TASK-...',                            |</span>
|     'type': 'TASK'                             |                                                             |
|                                                |         'projectPHIDs': ['PHID-PROJ-...'],                  |
|                                                |         'uri': 'https://url-here.com/T1234',                |
|                                                |         'dependsOnTaskPHIDs': ['PHID-TASK-...', ...],       |
|                                                |         'ccPHIDs': ['PHID-USER-.', ...],                    |
|                                                |         'isClosed': True,                                   |
| },                                             |     },                                                      |
| ...                                            |     ...                                                     |
| ]                                              | }                                                           |
+------------------------------------------------+-------------------------------------------------------------+
</pre>

To get a complete view of a task 2 API calls need to be made :(

Urg. not sure if I've missed something, but I can't figure out how to get all the tasks associated with a sub-project form `search()`. Been using `query()` for this! For some reason `search()` wants to just give be everything from a project, which I suppose isn't so bad, just a shame I can't get it for a specific board (sub project). Don't know why they bothered because sub-project name's are globally unique, it would seem.

So, using new API can get tasks for project but not sub-project. So either use `query()` and then suppliment with `search([task ids from query])` or search on parent project. But then can't associate the tasks to a sub-project, thre's nothing in the returned data to do this. Which seems like a P in the A until... `search()` has a constraint called `columnPHIDs`, so the work around is to get the workboard columns for a project and use them as the filter criteria... phew!

Ah, there are extra **attachments** that can be requested! So, can get all the tasks for the main project and then filter for tasks that belong to a sub-project by adding `attachments={'parents': True}` into the API call.

WOW! Tested the `search` API further and it returned, in my test, a ticket that was not actually associated with JEHTest1 in the present (didn't appear on the workboards and also the API returned an empty list in the attachments list). It had previously been associated with JEHTest1 but it had been removed from that project. So, does this search for tickets that have been associated with a project at any time!

So... if I am looking at points currently on a board I need to filter this list to ensure the ticket attachments list the PHID of the project in the constraints!

But if I want to delve into the history of the project I need to know *when* the ticket was associated with the project.

So, I suppose it makes sense this API returns tickets that were associated with the project at *any* time in its history.


### Getting Transactions For A Task
Use [`maniphest.gettasktransactions()`](https://secure.phabricator.com/conduit/method/maniphest.gettasktransactions/)

I wanted to get transactions for each task. To do this in Python:

```
result = phab.maniphest.gettasktransactions(ids=[...])
```

Where `ids` is a list of task IDs as *integers*.

This returns the following structure in `result.response`:

```
{
    '<task ID>': [
        {
            'authorPHID': <PHID-USER-...>,
            'comments': <str or None>,
            'dateCreated': 'unix-time-since-epoch',
            'newValue': <phid or None or []>,
            'oldValue': <phid or None or []>,
            'taskID': '<task ID>',
            'transactionID': '<number>',
            'transactionPHID': '<PHID-XACT-TASK-...>',
            'transactionType': '(core:create|core:comment|core:columns
                                |core:edge|core:edit-policy|core:subscribers
                                |core:view-policy|description|points|priority
                                |reassign|title
                                )'
        }
    ],
    ...
}
```

The fields `newValue` and `oldValue` depend on the `transactionType`.

#### transactionType == 'core:create'

```
{
    'authorPHID': 'PHID-USER-...',
    'comments': None,
    'dateCreated': '1648665913',
    'newValue': None,
    'oldValue': None,
    'taskID': '13163',
    'transactionID': '300668',
    'transactionPHID': 'PHID-XACT-TASK-...',
    'transactionType': 'core:create'
}
```

#### transactionType == 'core:columns'

```
{
    'authorPHID': 'PHID-USER-...',
    ...
    'newValue': [{
        'afterPHIDs': [],
        'beforePHIDs': ['PHID-TASK-...', ...],
        'boardPHID': 'PHID-PROJ-...',                                  #< The board it is current on
        'columnPHID': 'PHID-PCOL-....',                                #< Column it's moved to
        'fromColumnPHIDs': ([] | {'PHID-PCOL-...': 'PHID-PCOL-...'})   #< Column it's moved from
    }],
    'oldValue': None,
    ...
}
```

When `fromColumnPHIDs` is the empty  list (`[]`) it means that the task was created and has just been
assigned a column in a workboard. When it is a dictionary, I have, so far, only seen it have one key.

The `beforePHIDs` field appears, to give the order of tickets in the workboard column after the ticket
was moved, relative to this ticket. The PHID at index 0 is the one below this ticket, and so on.

The `afterPHIDs` fields is similar, except it gives tickets *above* this ticket. Index 0 is the ticket
immediately above, index 1, the one above that and so on.

Both `beforePHIDs` and `afterPHIDs` can be an empty or not. The combination gives the snapshot of the
workboard column at the time of the move.

One might wonder why there is only `boardPHID` and to a "to" and "from" board PHID if a ticket moves
board. The reason is is that this is a different event. This would generate a `core:edge` transaction,
where the ticket, from whatever column it is in the source board, moves to the backlog of the other
board.

**Warnign about which board the column PHID is on**:
You have to watch out for board changes. The `columnPHID` and `fromColumnPHIDs` can be on another board.
The `boardPHID` field can refer to a *different project* when this is the case and to get the column
name the other board's columns must be looked up. I don't quite understand why this is. It would seem
the ticket might have been moved to this board but the references remain to the old board - the column
names appear to be the same in these cases.


**Example ticket just created**
Here the transaction `core:columns` occurs just after a `core:create`:
```
'newValue': [{'afterPHIDs': [],
                'beforePHIDs': [],
                'boardPHID': 'PHID-PROJ-...',
                'columnPHID': 'PHID-PCOL-...',
                'fromColumnPHIDs': []}],
```

#### transactionType == 'points'
```
'newValue': <int or None>,
'oldValue': <int or None>,
```

#### transactionType == 'core:edges'
As in edges in a graph data structure: these are the links between tasks and projects, other taks and diffusion commits.

For example, when a ticket is created, after the `core:create` and then the `core:columns` is a `core:edge` to associate
the task with the project it was created in...

```
{
    'authorPHID': 'PHID-USER-...',
    'comments': None,
    'dateCreated': '1648665913',
    'newValue': ['PHID-PROJ-...'],
    'oldValue': [],
    'taskID': '...',
    'transactionID': '...',
    'transactionPHID': 'PHID-XACT-TASK-...',
    'transactionType': 'core:edge'
}
```

Then, lets say a tag is added.

```
{
    'authorPHID': 'PHID-USER-...',
    'comments': None,
    'dateCreated': '1648667160',
    'newValue': ['PHID-PROJ-...'],
    'oldValue': [],
    'taskID': '...',
    'transactionID': '...',
    'transactionPHID': 'PHID-XACT-TASK-...',
    'transactionType': 'core:edge'
}
```

Note, how `oldValue` doesn't contain anything. That is because nothing was *removed*, only added. *And*, `newValue` does not accumulate the tags on the ticket, it only shows what was added by this transaction. So, when the same tag is removed...

```
{   
    'authorPHID': 'PHID-USER-...',
    'comments': None,
    'dateCreated': '1648667354',
    'newValue': [],
    'oldValue': ['PHID-PROJ-...'],
    'taskID': '...',
    'transactionID': '...',
    'transactionPHID': 'PHID-XACT-TASK-...',
    'transactionType': 'core:edge'
}
```

Now, if we moved a task from one board to another:

```
{
    'authorPHID': 'PHID-USER-..',
    'comments': None,
    'dateCreated': '1648667477',
    'newValue': ['PHID-PROJ-...'],
    'oldValue': ['PHID-PROJ-...'],
    'taskID': '...',
    'transactionID': '..',
    'transactionPHID': 'PHID-XACT-TASK-...',
    'transactionType': 'core:edge'
}
```

**Add/Remove Project To/From Task**
Example of adding a Project tag to a task - an edge between the project and task is created:
```
{
    'authorPHID': 'PHID-USER-...', 
            'comments': None,
            'dateCreated': '...',
            'newValue': ['PHID-PROJ-', ...],
            'oldValue': [],
            'taskID': '...',
            'transactionID': '...',
            'transactionPHID': 'PHID-XACT-TASK-...',
            'transactionType': 'core:edge'
}
```

`newValue` has the project PHID that was newly associated with the task. If multiple projects were associated then the list has more than one member.

`oldValue` would be populated if a project as disassociated from a task

**Add/Remove Metnion Of Another Task To/From A Task**
When another task is mentioned in the current task, an association, or edge, to the mentioned task must be created. The edge direction is from the mentioner to the mentionee Eg:

```
{
    'authorPHID': 'PHID-USER-'
    'comments': None,
    'dateCreated': '1617143557',
    'newValue': ['PHID-TASK-...'],
    'oldValue': [],
    'taskID': '...',
    'transactionID': '...',
    'transactionPHID': 'PHID-XACT-TASK-...',
    'transactionType': 'core:edge'
},
```

**Add/Remove Mention Of Task To/From Diffusion Comment**
This is when a Diffusion comment mentions a task. The edge directon is from the mentioner (the diffusion comment) to the mentionee (the task):
```
{
    'authorPHID': 'PHID-USER-...',
    'comments': None,
    'dateCreated': '...',
    'newValue': ['PHID-CMIT-...'],
    'oldValue': [],
    'taskID': '...',
    'transactionID': '...',
    'transactionPHID': 'PHID-XACT-TASK-...',
    'transactionType': 'core:edge'
}
```

## Listing Projects
From the Phab docs:

> Phabricator projects are flexible, general-purpose groups of objects that you can use to organize
> information.
> ...
> Subprojects are projects that are contained inside the main project. You can use them to break
> large or complex groups, tags, lists, or > undertakings apart into smaller pieces.
>
> Milestones are a special kind of subproject for organizing tasks into blocks of work.
> You can use them to implement sprints, iterations, milestones, versions, etc.

Use [`projects.query()`](https://secure.phabricator.com/conduit/method/project.query/) and/or
Use [`projects.search()`](https://secure.phabricator.com/conduit/method/project.search/)

### Query
**`query()` is deprecated**.

```
all_projects = phab.project.query()
all.projects.response
```

The response looks like this:

```
{
    'cursor': {'after': '283', 'before': None, 'limit': 100},
    'data': {
        'PHID-PROJ-23nn4aloh2s4wqwwigtr': {
            'color': 'disabled',
            'dateCreated': '1562702056',
            'dateModified': '1570469329',
            'icon': 'tag',
            'id': '206',
            'members': ['PHID-USER-...', ...],
            'name': 'My Project Name',
            'phid': 'PHID-PROJ-...',
            'profileImagePHID': <None or phid>,
            'slugs': [... list of strings...]
        }, 
        ...
    }
```

To query a specific project or projects by name use:

```
my_projects = phab.project.query(names=['My Project', 'My Other Project', ...])
```
In this case the response is the same shape as shown above except that the `data` dictionary will only have one key.

If the project cannot be found then `data` will be an empty *list*.

![How Project dicts returned by project.search link up](##IMG_DIR##/phab_project_search_api.jpg)

### Search
Just as for tasks, query and search give slightly different sets of data. For example, search lets you find out about parents! The reason is that **`query()` is deprecated**.

```
{'attachments': {'ancestors': {'ancestors': [{'id': ...,                 # The parent projects can be 
                                               'name': '...',            # obtained using the attachments={"ancestors":True}
                                               'phid': 'PHID-PROJ-...'   # API parameter.
                                              },                         # Looks like list is ordered by depth, 0 first.
                                              ...
                                            ]
                              },
                  'members': ...,
                  ...
                },
  'fields': {'color': {'key': 'blue', 'name': 'Blue'},
             'dateCreated': 1614861258,
             'dateModified': 1634812114,
             'depth': 1,
             'description': '* Development of the configuration for the DS '
                            'server cluster\n'
                            '* Initial deployment of intrusion detection '
                            '(Snort & SELinux)',
             'icon': {'icon': 'fa-map-marker',
                      'key': 'milestone',
                      'name': 'Milestone'},
             'milestone': 5,
             'name': 'DS 1: Platform & Intrusion Det. 1',
             'parent': {'id': 359,
                        'name': 'Seagull',
                        'phid': 'PHID-PROJ-anuxwlemwcqozn7zwlxs'},
             'policy': {'edit': 'users', 'join': 'users', 'view': 'users'},
             'slug': None,
             'spacePHID': None,
             'subtype': 'default'},
  'id': 385,
  'phid': 'PHID-PROJ-2ogwbkehmovihj36qump',
  'type': 'PROJ'
}
```

* `depth` is the level in the parent/child tree where the parent has depth `0`.
* If searching for a project by name, that is not at depth 0, then if subprojects can have identical names then
  will need to also specificy the parent project.

#### Project Work Board: Getting Columns

```
search_result = phab.project.column.search(
    constraints={'projects': [<project-phid>, ...]}
)
```

The `search_result.response` has this shape:

```
{
    'cursor': {
        'after': ...,
        'before': ...,
        'limit': ...,
        'order': ...
    },
    'data': [
        {
            'attachments': {},
            'fields': {
                'dateCreated': <unix-seconds-since-epoch>,
                'dateModified': <unix-seconds-since-epoch>,
                'name': 'WB Column Name',
                'policy': {'edit': 'users', 'view': 'users'},
                'project': {
                    'id': 410,
                    'name': 'My Project Name',
                    'phid': 'PHID-PROJ-...'
                },
                'proxyPHID': None
            },
           'id': <int>,
           'phid': 'PHID-PCOL-...',
           'type': 'PCOL'
        },
        ...
    ],
    'maps': {},
    'query': {'queryKey': None}
}
```


