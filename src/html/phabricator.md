## Conduit API

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

## Tasks
### Task Info
To search for a task there is `phab_api.maniphest.query(ids=[...])` and `phab_api.maniphest.search(constraints={'ids': [...]})`. Both return an overlapping set of information but with some annoying differences, for example, `search()` will give information about the story points for the task, whilst `query()` will not.

``` { .prettyprint .linenums}
+------------------------------------------------+-------------------------------------------------------------+
| Search()                                       | Query()                                                     |
+------------------------------------------------+-------------------------------------------------------------+
| List[Dict]                                     | Dict: PHID-TASK -> Dict                                     |
| [{                                             | {                                                           |
|     'attachments': {},                         |                                                             |
|     'fields': {                                |     'PHID-TASK-sff44g4bfykui2mwakwt': {                     |
|         'authorPHID': 'PHID-USER-...',         |         'authorPHID': 'PHID-USER-...',                      |
|         'closerPHID': 'PHID-USER-...',         |         'auxiliary': {...},                                 |
|         'dateClosed': unix-epoch-timestamp,    |         'ccPHIDs': ['PHID-USER-.', ...],                    |
|         'dateCreated': unix-epoch-timestamp,   |         'dateCreated': '1617202435',                        |
|         'dateModified': unix-epoch-timestamp,  |         'dateModified': '1646080087',                       |
|         'description': {'raw': '...'},         |         'description': '...',                               |
|         'name': '...',                         |         'title': '...',                                     |
|         'ownerPHID': 'PHID-USER-...',          |                                                             |
|         'points': '...',                       |         'isClosed': True,                                   |
|         'policy': {'edit': 'users',            |         'objectName': 'T1234',                              |
|                    'interact': 'users',        |         'ownerPHID': 'PHID-USER-lvc3c4gnmdu6biq5bac4'       |
|                    'view': 'users'},           |                                                             |
|         'priority': {'color': 'orange',        |         'priority': 'Normal',                               |
|                      'name': 'Normal',         |         'priorityColor': 'orange',                          |
|                      'value': 50},             |         'projectPHIDs': ['PHID-PROJ-...'],                  |
|         'spacePHID': None,                     |         'uri': 'https://url-here.com/T1234',                |
|         'status': {'color': None,              |         'status': 'resolved',                               |
|                    'name': 'Resolved',         |         'statusName': 'Resolved',                           |
|                    'value': 'resolved'},       |                                                             |
|         'subtype': 'default'                   |         'dependsOnTaskPHIDs': ['PHID-TASK-...', ...],       |
|     },                                         |                                                             |
|     'id': 11600,                               |         'id': '11600',                                      |
|     'phid': 'PHID-TASK-...',                   |         'phid': 'PHID-TASK-...',                            |
|     'type': 'TASK'                             |                                                             |
| },                                             |     },                                                      |
| ...                                            |     ...                                                     |
| ]                                              | }                                                           |
+------------------------------------------------+-------------------------------------------------------------+
```

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

When `fromColumnPHIDs` is the empty  list (`[]`) it means that the task (if you were querying tasks!)
was created and has just been assigned a column in a workboard.

You have to watch out for board changes. The `columnPHID` and `fromColumnPHIDs` can be on another board.

#### transactionType == 'points'
```
'newValue': <int or None>,
'oldValue': <int or None>,
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

Use [`projects.query()`](https://secure.phabricator.com/conduit/method/project.query/).

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


