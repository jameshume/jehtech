<style>
    pre > code {
        border: 0;
        background-color: inherit;
        font-size: 90%;
    }
</style>

## Basics
* https://github.com/ansible/workshops
    * Self paced exercises: https://www.redhat.com/en/engage/redhat-ansible-automation-202108061218
* Agentless - no software installed on what we're automating - e.g. talking to a device where we can't install python on that device and install from that device.
* Ansible core is written in Python
* **Playbooks**
    * Playbooks are files which describe the desired configurations or steps to implement on managed hosts. Playbooks can change lengthy, complex administrative tasks into easily repeatable routines with predictable and successful outcomes.
    * A playbook is interpretted and run against one or more hosts - task by task. The order of the tasks defines the execution and in each task the module does the actual work.
    * They are made of **plays**
        * A playbook can have multiple plays. They are the building blocks of playbooks.
        * A play starts with the `---`, called the "play stanza".
        * A play has a set of **task**s. A task has a 1-1 correlation with a module
        * A play is a top level specification for a group of tasks. Can tell a play which host it is executing on (`hosts: web`) and control behviour such as fact gathering or priviledge level (`become: yes` allows it to become `sudo`).
        * By default, Ansible executes each task in order, one at a time, against all machines matched by the host pattern. Each task executes a module with specific arguments. When a task has executed on all target machines, Ansible moves on to the next task.

        ```{.prettyprint .linenums}
        ---
        - name install and start apache
        hosts: web   ##< If "all" is used the play runs on all hosts - "all" is a reserved word
        become: yes  ##< privilege escalation in Playbooks

        tasks:
            - name: http package is present
            yum:  ##< This is the module that this task will use
                name: httpd
                state: latest
            ...
        ```

    * Good Playbooks are idempotent, so if a Playbook is run once to put the hosts in the correct state, it should be safe to run it a second time and it should make no further changes to the hosts.
    * There is a [best practice on the preferred directory structures for playbooks](https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html#directory-layout).
        * For example, the `copy` module knows where to find files based on this directory structure: from the root, it looks in the `files` directory.
        * For vars, Ansible will look automatically, relative to the root dir, in `group_vars` and `host_vars`.
            * Host variables will override, or take precedence, over group variables. The host variable YAML files basename is the name of the host to which the contained variables will be applied.
        * From the online labs example we had:
            ```
            |--- ansible-files                 ## Root level folder containing all the ansible files
                 |
                 |--- files                    ## This is where the copy module searched for files it was given
                 |    |--- dev_web.html        ## if the paths were relative they were relative to this directory
                 |    |--- prod_web.html
                 |    |--- web.html
                 |    ...
                 |
                 |--- groups_vars              ## "web" is a group in the hosts file. these variables are automatically
                 |    |--- web.yml             ## made available in playbooks where the "web" group of hosts is used.
                 |
                 |--- host_vars                ## Like the group_vars, except they apply to specific hosts and will override
                 |    |--- node1.yml           ## any group_vars.
                 |
                 |--- hosts                    ## The INI file that places sets of hosts into specific groups
                 |
                 |--- playbook_example1.yml    ## Different playbooks
                 |--- playbook_example2.yml
                 |--- ...
            ```

* **Modules**
    * Technically modules are plugins
* **Plugins**
    * Are pieces of code that augment Anisble's core functionality. Ansible uses a plugin architecture to enable a rich, flexible and expandable feature set.
    * Filter plugins allow to change the output of a task to a new format. E.g. `{{ some_variable | to_nice_yaml }}`.
* **Inventory** - the systems that a playbook runs against
    * List of multiple systems in your infrastructure that automation is executed against. 
        * Ansible works against multiple managed nodes or "hosts" in your infrastructure at the same time, using a list or group of lists known as inventory.
        * The inventory tells what nodes are out there to be used by Ansible, what credentials need to be used to connect to them, how the nodes are grouped, and other necessary variables.
    * Inventory usually file based but can be a DB or Git repo,
    * Can have multiple groups,
    * Can have variables for each group or even host.
    * E.g.
        ```{.prettyprint .linenums}
        [web]
        # These will use DNS
        server1.example.com
        server2.example.com

        [web:vars]
        # Example of group variables
        apache_listen_port=8080
        apache_root_path=/var/www/mywebdocs

        [all:vars]
        # This is an implicit group
        ansible_user=blah
        ansible_ssh_private_key_file=/home/blah/.ssh/id_rsa

        [db]
        dbserver.example.com

        [app1srv]
        # Here, rather than use DNS, the IP address is pinned to a host name
        appserver01 ansible_host=10.42.10.1

        [big:children]
        #    ^^^^^^^^
        #    Keyword saying any groups should be collapsed into this group
        #
        # So here, web, will be replaced (collasped) with its members
        web
        # And we can spec other resources directly here too... doesnt just have to be groups
        my.new.server.com
        ```

* **Roles** - reusable playbooks (automation actions).
    * They group your tasks and variables of your automation in a re-usable structure:

        ```{.prettyprint .linenums}
        ---
        - name install and start apache
        hosts: web
        become: yes 
        roles: 
            - common
            - webservers
        ```

* **Collections** - simplified and consistent content delivery (basically a TAR with a specific folder structure)
    * A data structure containing automation content:
        * Modules, playbooks, roles, plugins, docs, tests
* **Automation Execution Environments**
    * Solve the problem of having many collections with dependencies on different Python versions, OS libs etc etc.
    * So Automation Execution Environments wrap all of this up: the collections, libraries and ansible core running on top of a universal base image (leverages container technology).
* **Config file**
    * `ansible.cfg`, usually `/etc/ansible/ansible.cfg`.
    * Basic config file for Ansible.

* **Commands**
    * Navigator:
        * `ansible-navigator` is a CLI tool that gives you a text based user interface (TUI)
        *  Use `ansible-navigator run my_plyabook.yaml --mode stdout`. or use `--mode check` for a dry run.
    * Playbook:
        * Ansible Playbooks are executed using the ansible-playbook command on the control node
        * `ansible-playbook` - launch a playbook. 
            * Check syntax: `ansible-playbook --syntax-check apache.yml`


## Variables
* Vars not normally in a playbook itself
* Host vars supercede group vars. 
```{.prettyprint .linenums}
---
- name: variable playbook test
  hosts: localhost

  vars:
    var_one: awsome
    var_two: ansible is
    var_three: "{{ var_two }} {{ var_one }}" #< Jinja syntax for variable unpacking

  tasks:
    -name print out var_three
     debug:
       msg: "{{ var_three }}"
```

* **Ansible Facts**
    * Just variables, but come from the host (whatever we're talking to) itself.
    * Check them out with the setup module (built in module (for Linux), have modules for other systems): e.g., `ansible -m setup localhost`.
        * Includes things like IP addresses on the box, the distribution, DNS info, and on and on...

## Constructs
* Conditions, handlers, loops.
* [The docs!](https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html#playbooks-conditionals)

### Conditions
```{.prettyprint .linenums}
---
- name: Conditional test
  hosts: localhost

  vars:
        my_mood: happy

  tasks:
    - name: task, basd on my_mood var
      debug:
          msg: "Yay! I am {{ my_mood }}!"
      when: my_mood == "happy"
    - name: task, basd on my_mood var
      debug:
          msg: "Uh oh... I'm {{ my_mood }}!"
      when: my_mood == "grumpy"
```

Or, more realistically,

```{.prettyprint .linenums}
tasks:
    - name: Install Apache
        apt:
            name: apache2
            state: latest
        when: ansible_distribution == 'Debian' or
              ansible_distribution == 'Ubuntu'
    
    - name: Install httpd
        yum:
            name: httpd
            state: latest
        when: ansible_distribution == 'RedHat'
```

Other interesting things could be `when: inventory_hostname in groups["web"]` to conditionally run a task based on which group a particular invetory items is in and so on...

### Handler

* Not a handler (but leads up to them)
    * `register` - a task parameter - register the results of the task
    * You can create variables from the output of an Ansible task with the task keyword register. You can use registered variables in any later tasks in your play.
        ```{.prettyprint .linenums}
        tasks:
            - name: Install httpd
                yum:
                    name: httpd
                    state: latest
                register: httpd_results
            
            - name: Restart httpd
            service:
                    name: httpd
                    state: restart
            when: httpd_results.changed
        ```
    * Can do lots of things like `when: http_results.stdout.find('something') != -1`, for example.
    * If a play fails, the registered variable can be queried to `is skipped` as in `when: http_results is skipped`.

* Handlers
    * Run a task only when a change is made on a machine - use handlers (`notify`) rather than a `when`.
    * Replace `register` with `notify` - specifies a list of handlers to notify when the task returns a `changed=True` status.
    * By default, handlers run after all the tasks in a particular play have been completed: handler only runs once, regardless of how many tasks notify it.
    * [The Docs!](https://docs.ansible.com/ansible/latest/user_guide/playbooks_handlers.html)
        ```{.prettyprint .linenums}
        tasks:
            - name: Install httpd
                yum:
                    name: httpd
                    state: latest
                notify: restart_httpd
            
            - name: restart_httpd
                service:
                        name: httpd
                        state: restart
        ```

### Loops

```{.prettyprint .linenums}
---
- name
hosts: node1
become: yes

tasks:
    - name: Ensure user is present
        user:
        name: "{{item}}:
        state: present
        loop:
        - dev_user
        - qa_user
        - prod_user
```

* Note however, that if a module accepts lists, for example `yum` accepts lists of packages to install, using the module's built-in abilities will be faster and cleaner than using Ansible scipted loops.
    * Performance hit.
    * Makes playbook more complicated. Try not to do programming instead of Ansible.


## Templating
* Uses Jinja2 templating
* Template module
    * Source is on the control node (i.e. where automation is being run from). The source gets run through the Jinja2 templating engine.
        * The template can contain variables from the Ansible script, e.g. a template line could read `Listen {{ http_port }}`.
    * Dest is a file on the host being setup that results from running the templating engine above.
* A *very* simple example:
    * The Ansible file could read

    ```{.prettyprint .linenums}
    - name: Ensure apache is configured
    hosts: web
    become:  yes

    vars:
        http_port: 80
        http_docroot: /var/ww/mysite.com

    tasks:
        - name: Verify correct config file present
        template:
            src: tmplates/httpd.conf.j2
            dest: /etc/httpd/conf/httpd.conf
    ```

    * And the template could read (a snipped):

    ```{.prettyprint .linenums}
    # Listen on specific IP addresses
    Listen {{ http_port }}  ##< Variable is taken from Ansible playbook above

    # DocumentRoot: The dir out of which you will service your docs
    DocumentRoot {{ http_docroot }}
    ```

## Roles
* [The docs!](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)
* Roles let you automatically load related vars, files, tasks, handlers, and other Ansible artifacts based on a known file structure.
* TODO



