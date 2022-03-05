<style>
    .same {
        background-color: #ccffcc
    }
</style>


![Phab object relationships](##IMG_DIR##/phabricator_projects_tasks_structure.png)

## Setup Python API With Token
To avoid storing the token in source control, keep it in a file that is part of `.gitignore` so that
it does not get committed.

``` { .prettyprint .linenums}
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
| <b>maniphest.search()</b>                             | <b>maniphest.query()</b>                                           |
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

### Getting Transactions For A Task
Use [`maniphest.gettasktransactions()`](https://secure.phabricator.com/conduit/method/maniphest.gettasktransactions/)

I wanted to get transactions for each task. To do this in Python:

``` { .prettyprint .linenums}
result = phab.maniphest.gettasktransactions(ids=[...])
```

Where `ids` is a list of task IDs as *integers*.

This returns the following structure in `result.response`:

``` { .prettyprint .linenums}
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

#### transactionType == 'core:columns'

```{ .prettyprint .linenums}
'newValue': [{
    'afterPHIDs': [],
    'beforePHIDs': ['PHID-TASK-...', ...],
    'boardPHID': 'PHID-PROJ-...',
    'columnPHID': 'PHID-PCOL-....',
    'fromColumnPHIDs': ([] | {'PHID-PCOL-...': 'PHID-PCOL-...'})
}],
'oldValue': None,
```

When `fromColumnPHIDs` is the empty  list (`[]`) it means that the task was created and has just been
assigned a column in a workboard.

You have to watch out for board changes. The `columnPHID` and `fromColumnPHIDs` can be on another board.

#### transactionType == 'points'
```
'newValue': <int or None>,
'oldValue': <int or None>,
```

#### transactionType == 'core:edges'
As in edges in a graph data structure: these are the links between tasks and projects, other taks and diffusion commits.

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

``` { .prettyprint .linenums}
all_projects = phab.project.query()
all.projects.response
```

The response looks like this:

``` { .prettyprint .linenums}
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

``` { .prettyprint .linenums}
my_projects = phab.project.query(names=['My Project', 'My Other Project', ...])
```
In this case the response is the same shape as shown above except that the `data` dictionary will only have one key.

If the project cannot be found then `data` will be an empty *list*.

### Search
Just as for tasks, query and search give slightly different sets of data. For example, search lets you find out about parents! The reason is that **`query()` is deprecated**.

```
{'attachments': {},
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

``` { .prettyprint .linenums}
search_result = phab.project.column.search(
    constraints={'projects': [<project-phid>, ...]}
)
```

The `search_result.response` has this shape:

``` { .prettyprint .linenums}
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


