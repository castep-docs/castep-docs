## Command not found ##

When you type `castep`, Linux doesn't know where that command is, so it looks in the places where programs are usually put (often /bin, /sbin, /usr/bin, /usr/sbin, /usr/local/bin and /usr/local/sbin ; "bin" here is short for "binary"). Unless CASTEP is there, it will tell you that it can't find it. Notice in particular that the directory you're in when you type the command is *not* in Linux's list of usual places to look, which is especially confusing when you first encounter it!

### Telling Linux where to find CASTEP ###

There are several ways to fix this. If you're on a shared machine, it is usually best to make a subdirectory in your home directory, perhaps called "bin":

```
mkdir ~/bin
```
and put CASTEP in there (along with any other programs you compile yourself), e.g.
```
cp ~/CASTEP-22.1/obj/linux_x86_64_gfortran--serial/castep.serial ~/bin
```
This still won't mean that Linux will find CASTEP, because this is also not a place it will look for programs. The places Linux looks in are stored in a special Linux environment variable called the "path", and the final step is to add the new directory to this "path". Exactly how you do this depends on what kind of command-line interpreter (called a "shell") you're using in Linux, but there are only really two main kinds: bash and csh. Type
```
export PATH=${PATH}:~/bin
```
if you're using bash, or
```
setenv PATH ${PATH}:~/bin
```
if you're using csh.

These commands tell Linux to look in all the places it's looking in already, and also "~/bin". If you don't know which shell you're using, try typing:
```
echo $SHELL
```
and see what it says. If it says something like "/bin/bash" then you're using bash, if it's "/bin/csh" or "/bin/tcsh" then it's csh (or close enough). If it gives something else, just try the line starting "export" and if it gives an error, try the "setenv" one instead.

Now try typing "castep.serial" and you should see this:
```
Usage:
castep <seedname> : Run files <seedname>.cell [and <seedname>.param]
" [-d|--dryrun] <seedname> : Perform a dryrun calculation on files <seedname>.cell
" [-s|--search] <text> : print list of keywords with <text> match in description
" [-v|--version] : print version information
" [-h|--help] <keyword> : describe specific keyword in <>.cell or <>.param
" " all : print list of all keywords
" " basic : print list of basic-level keywords
" " inter : print list of intermediate-level keywords
" " expert : print list of expert-level keywords
" " dummy : print list of dummy keywords
```

### Automatically adding to your PATH ###

The changes so far will be lost when you exit the command-line. We need to make sure that your directory is added to the PATH variable every time you log in or open a new terminal. If you're using bash, edit the file `~/.bashrc` with a text editor (e.g. gedit), go to the end, and add the line to set the PATH:
```
export PATH=${PATH}:~/bin
```
Note that the file is in your home directory ("~/"), and the name starts with a dot ("." a full stop). Save and exit, and it should all be set up for you.

If you're using csh, edit the file "~/.cshrc" instead, and add the appropriate line to set the PATH:
```
setenv PATH ${PATH}:~/bin
```
Save and exit, and it should all be set up for you.
