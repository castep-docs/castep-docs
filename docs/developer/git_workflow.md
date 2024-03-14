Draft bitbucket/git workflow for CASTEP developers: NB: Not a git tutorial!

1.  Bitbucket web - create fork (“myfork” for this example)

2.  Make fork visible to CDG (bitbucket group, very least to dominik.jochym@stfc.ac.uk so that the CI works)

3.  Clone to local machine ``git clone git@bitbucket.org:mybitbucket/castep-myfork.git castep-myfork``

4.  Setup local githook (see readme in .githooks)

5.  Configure remote “myfork” and “upstream”:

    ```
    git remote add upstream git@bitbucket.org:castep/castep.git
    git remote add myfork git@bitbucket.org:mybitbucket/castep-myfork.git
    ```
    Can verify remotes with git remote -v (useful to have more remote aliases if you want to check out a branch on someone else’s fork)

6.  Name branch ``git branch foo``

7.  Switch to branch ``git switch foo``

8.  (Stage and) Commit changes ``git commit -m “Cool stuff”``

9.  If planned destination branch (usually default) has changed:

    1.      Fetch from official ``git fetch upstream default:default`` [NB: reference to “upstream” might be different if   your remote aliases are configured differently]. This not only performs the fetch but also updates the local "default" branch to sync with the upstream.

    2. Rebase using destination (default) branch ``git rebase default``. This makes it so that your changes are sitting on top of the latest “official” default. If your branch contains many PRs it may be better to "squash", using the bitbucket merge option "squash merge", or
    ```
    git rebase -i default
    ```
    and then in your editor, leave the first line as 'pick ....' and then change all subsequent lines from 'pick ...' to 'squash ...'. Save the file and then you will get a squashed history for this PR.

    3. Fix conflicts if needed ``git mergetool tool=kdiff3`` [kdiff3 is just my personal preference] and then:
                        ``git rebase --continue`` (and commit)

10.      Push branch to fork (``git push myfork foo``) This is a very good habit to get used to: always specify the remote and branch so you know exactly what you’re trying to push and where!
                Synchronise your fork’s default branch with upstream:
       ```
      git push myfork default
       ```

11.      Create pull request (bitbucket web, from fork)
                "Delete this branch after merge" should be checked in most cases. The exception is with long-term development branches and release branches.

12.      If another PR is merged first, you have two choices:


    1. &nbsp;

          1. *Do NOT* click “Sync now” on the PR page as this does a merge and commit, which breaks our --ffonly policy

          2. At your local clone, go back to step 9

          3. Similar to step 10, except this is a “force” push as the rebase has changed the commit history:
          ```
          git push --force myfork foo
          git push myfork default
          ```

    2. On the website interface, click "merge". Then change the merge strategy to "Squash". You will then get an opportunity to edit the commit message.

13. Switch back to the default branch ``git switch default.`` Do not do any further work on your foo branch and attempt any merging, or you risk creating a "spaghetti" of loops in the commit graph. You may re-use the name of your branch if you delete the old one with ``git branch -D``.
