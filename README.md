littlehelp
==========

Littlehelp was conceived to help reduce daily button bashing.  As I often find myself developing on my mac, but executing code on a server somewhere, Ill frequently find myself running the same rsync and restart commands.

Littlehelp aims to lend a hand by automating this process for you.  To do this littlehelp registers a file system watch on the project directory it is launched from, and when it detects a file modification it executes an 'action'.  An 'action' is simply a function within the launching bash script, called with the path and file name of the file modified.

To get started simply checkout little help, you probably dont want all the history, so try something like this ...

```
git clone –depth 1 https://github.com/rasathus/littlehelp.git
```

Once checked out, take a look at the file 'littlhelp' in your root folder and customise your 'action' function. 

```
function action {
    file_path=$1
    file_name=$2

    # Add your actions here ...
}
```

you can now launch littlehelp with the command ./littlehelp, at which point it will daemonise itself and get on with the task at hand.  Littlehelp uses OsX's built in notifications to alert you of any changes to the project.
