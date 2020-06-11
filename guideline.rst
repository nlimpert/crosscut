.. meta::
   :topic: guideline
   :author: Marcus Meeßen
   :keywords lang=en: guideline, stylistic hints, teaching approach, version
      control
   :description lang=en: A guideline that helps readers and authors to
      communicate in the same way.

.. role:: raw-html(raw)
   :format: html

.. role:: rst(code)
   :language: rst

.. role:: html(code)
   :language: html

.. role:: bash(code)
   :language: bash

.. sidebar::
   Guideline

   .. sectionauthor::
      :term:`Meeßen`

   .. codeauthor::
      :term:`Meeßen`

   .. versionadded:: r.1

   .. seealso::
      `Style guide for Sphinx-based documentations
      <https://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html>`_


.. _guideline:

################################################################################
Guideline
################################################################################

The aim of this guideline is to achieve a shared understanding of the stylistic
techniques and teaching concepts used. These are intended to support the flow of
reading, make the author's argumentation comprehensible, and enable the reader
to quickly achieve an overview and find important information. The reader is
prepared for working with the offered material.

.. glossary::

   Guideline
      The guideline helps readers and authors to communicate in the same way.

.. internal:: It is particularly important to offer a uniform teaching format
   that does never confuse the reader or the course participant. The process of
   creating high-quality teaching material begins with the "right" usage of a
   version-control system, which we want to start with. It is important that
   *every change to the material is documented, reviewed and tested several
   times*.

   A second factor for high-quality material is *stylistic consistency*. A small
   deviation may confuse the reader and disturbs the reading flow. It may also
   be difficult for the reader to keep track of too many rules. The principle
   should always be "as little as possible, as much as necessary".

   The third and maybe most important factor is *content consistency*. A guided
   thread in every course is desirable, but it isn't the only crucial concern.
   Each time someone reads one page, they also build up an expectation attitude
   that is transferred to the other teaching materials. We should always try to
   satisfy these expectations.

   Other factors are the existence of a conclusion of each topic and to avoid
   frequently switching between topics. One last factor is the *retrievability*
   of materials. A course participant will forget things, one more, the other
   less. Instead of repeating things over and over again, a *high level of
   referencing* is what we aim for. This should make it possible to read quickly
   because we will not constantly mention what the reader could already know.
   Experienced users will no longer be bored with familiar topics and in
   addition the teaching materials will remain maintainable and exchangeable.


.. only:: internal

   *****************************************************************************
   Version-Control System ("Git")
   *****************************************************************************

   .. internal:: Git is used to maintain different versions of our course
      material and is fully integrated into the prescribed quality control
      process. We use Git in conjunction with GitLab, a tool that supports issue
      tracking as well as other processes such as merge requests and continuous
      integration.

      https://git.fh-aachen.de/h2020rosin/academy


   Bring Yourself Up to Date
   =============================================================================

   .. internal:: The very first step to take to work with a repository is to
      clone it, using the :bash:`git clone` command.

      .. code-block:: bash

         git clone git@git.fh-aachen.de:h2020rosin/academy.git

      In everyday work, this command is no longer used. Instead, the commands
      :bash:`git fetch` and :bash:`git merge` are used. The "fetch" retrieves
      the current state from the server or the "origin", which usually includes
      changes made by other users. The "merge" combine the current state with
      your own state. Both commands are executed in the prescribed order by
      using :bash:`git pull`.


   Branching
   =============================================================================

   .. internal:: The whole project is divided into several feature-branches
      while it's developed. Branches are one of the main techniques that we use
      to ensure high quality of materials. This is achieved by a tiered system,
      which is explained in the next sections.

      In the following we will introduce some command, that you should know when
      working with branches. All available branches on your local version can be
      listed with :bash:`git branch -av`. To switch to another branch, you start
      in the :code:`master` per default, you can use :bash:`git checkout
      <branch>`. If you need to create a new branch either :bash:`git branch
      <new branch name>` or :bash:`git checkout <branch>` can be used. The
      latter will directly switch to the newly create branch.


   Structure
   -----------------------------------------------------------------------------

   .. internal:: The branches represent a hierarchical tree structure. The trunk
      is the :code:`master` branch. This branch only contains the most complete
      and audited material that can be used in this form without any hesitation
      during a training. Milestone branches build on the :code:`master`. These
      branches comprise a series of changes, that are attributed to a certain
      topic or to a certain target state. Milestones are the thickest branches,
      which hold directly at the trunk.

      From the milestones there originate feature branches. These are the
      thematically atomic units, which are described by an issue in GitLab in
      general. They are the small branches in the crown. As the last tier the
      user or work branches follow. They are the leaves, which make sure that
      the tree grows.

      Like in the real life: A tree is only as stable as its trunk, and if a
      branch breaks or a leaf falls this is not fatal. Unlike in nature, with
      Git branches may become part of the trunk at some point. Bad branches
      should be cut off or corrected before the trunk gets sick.

      :math:`\circ` :gui:text:`master`
         :math:`\rightarrow` :gui:text:`milestone`
            :math:`\rightarrow` :gui:text:`feature`
               :math:`\rightarrow` :gui:text:`user`

      In order to maintain the quality and at the same time to quickly take new
      material to a higher level, there are "stage" branches. These exist
      between the previously described stages. In them new material is collected
      for a while and tested in combination with other changes. If everything
      looks good the "stage" becomes "stable". So the branching is as follows.

      :math:`\circ` :gui:text:`master`
         :math:`\rightarrow` :gui:text:`master-stage`
            :math:`\rightarrow` :gui:text:`milestone-stable`
               :math:`\rightarrow` :gui:text:`milestone-stage`
                  :math:`\rightarrow` :gui:text:`feature`
                     :math:`\rightarrow`:gui:text:`user`

      Branches can bei created by various method. One opportunity is to use
      GitLab for this. From the command line you can create a branch with
      :bash:`git branch` which will create a new branch that is based on the
      current branch or commit. You can switch to the newly created branch with
      :bash:`git checkout`. A faster way to do both steps is to use the
      :bash:`-b` option of :bash:`git checkout`.


   Naming a Milestone Branch
   -----------------------------------------------------------------------------

   .. internal:: Milestone branches are named according to their identification
      number and a strongly simplified name of the milestone. Milestone branches
      are created and merged exclusively by the maintainers of the project. The
      following is a brief example.

      Milestone #2 is named "Writing a Guideline for Authors, Instructors, and
      Course Participants". This name is simplified to "guidelines" so that the
      branches are named :code:`2-guidelines-stable` for the stable one and
      :code:`2-guidelines-stage` to test a bunch of new features. The "stage"
      is based on the "stable" branch, and both are created by a project
      maintainer. Spaces in the shortened name are represented by underscores.
      This scheme is enforced by GitLab.


   Naming a Feature Branch
   -----------------------------------------------------------------------------

   .. internal:: Just like a milestone branch, a feature branch is named after
      the assigned milestone's number, its own identification number and a
      shorter version of the associated issue. Feature branches are also created
      and merged exclusively by the maintainers of the project. The following is
      a brief example.

      The issue number #4 has the name "Sphinx Extension to Process Elements of
      ROS". It belongs to milestone #1. So the created branch has to be named
      :code:`1/4-sphinx_ros_extension` can only be created by a maintainer.
      Spaces in the shortened name are represented by underscores. This scheme
      is enforced by GitLab.


   Naming a Work Branch
   -----------------------------------------------------------------------------

   .. internal:: A work or user branch starts with the name of the assignee who
      is processing a task. Yes, you've read correctly: A task should always be
      processed by one person. The user's initials are followed by the given
      identification numbers of the milestone and the issue to which this task
      belongs. Finally, there is a very brief description of the task that will
      be accomplished. In some cases, an issue can also be resolved by a task,
      but a work branch still has to be created for that.

      A work branch is created by the user who creates the task. This user is
      also responsible for initiating the merge request so that the work can be
      added to the feature branch. There are two basic ways to do this: Either
      you create the branch locally, solve the task and finally create the merge
      request in GitLab or you directly create a merge request in GitLab, which
      is marked as :code:`[WIP]` (Work in Progress), where the branch is
      automatically created. With the latter, the actual merge process starts
      with the removal of the :code:`[WIP]` tag, which is recommended.

      Again a short example for the naming. Issue #4 requires a customized
      configuration of the environment. The issue belongs to milestone #1. The
      task is to be done by John Doe. If the above scheme is applied, the branch
      name is :code:`jdoe/1/4/configuration_for_ros`, for example. Spaces in the
      shortened name are represented by underscores. This scheme is enforced by
      GitLab.


   Merge
   -----------------------------------------------------------------------------

   .. internal:: As already mentioned in the very first section, there is the
      command :bash:`git merge` with which you can merge your state with the
      origin's state. But the command can do more, at least in the context of
      pure git semantics. With the command two different branches can also be
      merged. When using GitLab, however, the use of merge request is always
      recommended, because at this point quality controls can be performed. This
      includes peer-review, of course, but also continuous integration, time
      tracking, labeling, and so on.

      A merge request should always transfer one branch to another branch that
      is directly above it in the hierarchy. E.g. a work branch is merged into a
      feature branch, which in turn is merged to its related milestone branch
      and so on.

      Due to merge commits are forbidden by our convention, a branch must be
      capable of being merged in fast-forward. This means it has to be rebased
      on the last commit of the origin's branches state.


   Rebase
   -----------------------------------------------------------------------------

   .. internal:: The :bash:`git rebase` lets you rewrite the history in many
      ways. Commits may be reworded, rearranged, "squashed" (unite multiple
      commits) or removed. We use the rebase mainly in two cases.

      The first case, as mentioned above, is to make a branch capable of being
      fast-forward merged. This arranges the history as if everything that
      exists in the target branch had already been there.

      The second case is the squashing of work branches. This reduces the number
      of commits needed to accomplish a task to only one. This merges an
      unnecessary high number of possibly incorrect or badly described commits
      into one that represents a fully functional and hopefully well described
      commit. Since a work branch must only be used by one user at a time, the
      author of a change is preserved and can be determined with tools like
      :bash:`git blame`.

      If an automatic rebase is not possibly due to conflicts, you have to
      resolve them and then use :bash:`git add <resolved file>` or :bash:`git rm
      <resolved file>` before you can use :bash:`git rebase --continue`. If you
      accidentally messed up, a rebase can be fully reverted by :bash:`git
      rebase --continue`. In general you should search for assistance, if you
      are not familiar with rebasing.


   Local Changes
   =============================================================================

   .. internal:: To track your local changes Git offers plenty of ways, here are
      some commonly used commands to do so. :bash:`git status`, among some other
      information, lists all files that have been modified, deleted, added, and
      so on. It distinguishes between "staged", "unstaged" and "untracked"
      files, which will be explained later. With :bash:`git diff` you will get
      all changes that were made between the actual files or "working tree", and
      the latest commit or :code:`HEAD`. An interesting command that helps to
      write a meaningful commit message is :bash:`git diff --staged`, which
      shows only the changes between the staged files and the :code:`HEAD`.


   Commit
   =============================================================================

   .. internal:: A commit represents a versioned state. It is created by the
      :bash:`git commit` command, saving the changes to all files that are
      staged. A commit consists of all changes that have been staged at the time
      it was created and a meaningful message. If you want to add something to
      the last commit, like an actually meaningful message or some more staged
      changes, you can use :bash:`git commit --amend`. Advanced fixing of broken
      or incomplete commits at any time in the history can also be done with
      rebasing.

      A common principle is to commit early and often. Do not exaggerate this,
      and if you experiment a lot and want to back up often, don't upload this
      history to the origin; in this case you can better squash your commits.
      Any commit that ends up on the origin should at least be error-free
      compilable.


   Staging Files
   -----------------------------------------------------------------------------

   .. internal:: To stage files, that might be taken into a commit later, you
      can use :bash:`git add -p <changed file>`. We strictly discourage from
      just using :bash:`git add` and don't you ever dare do a :bash:`git add *`.
      Know about every change you want to add to a commit.


   Writing a Message
   -----------------------------------------------------------------------------

   .. internal:: Just semantically summarize all the changes you've made, don't
      be too technical. You should identify what the task was. For a "normal"
      commit, 40 to 160 characters is a rough guide. :bash:`git commit -m
      <commit message>` is a shorthand to to avoid opening an editor.


   Publish
   =============================================================================

   .. internal:: At some point you might want to make your work available to the
      other contributors of the project. In order to do so, you have to "push"
      or synchronise your local branch with the origin. If you do this the first
      time with a newly created branch, use :bash:`git push --set-upstream
      origin <branch name>`. Later a simple :bash:`git push` will be sufficient.
      If you forget the first step, don't worry, Git will complain about it and
      provide you the required command.


   Tagging Versions
   =============================================================================

   .. internal:: After closing and merging a single milestone or a bunch of
      milestones into the master, the latest commit in the master branch should
      represent a new release. The :bash:`git tag` command or GitLab can be used
      to add a tag, which enables a user to find those commits. Since a full
      grown version numbering like SemVer.org is overkill for an mainly
      non-software product, we use a simple increment plus a patch number. A
      version is labeled by :code:`r.1` for the release #1, :code:`r.1-a`` for
      the first patch of release #1, :code:`r.2` for release #2 and so on.
      Patches are only designated to fix a critical problem, that may introduce
      legal problems or causes the product to be no longer compilable on some
      systems. The system is also explained in the :file:`CHANGELOG.md`. To push
      locally created tags you have to state this explicit with :bash:`git push
      --tags`.


   Miscellaneous
   =============================================================================


   Reusing Code and Configs
   -----------------------------------------------------------------------------

   .. internal:: Sometimes it makes sense to use code already developed
      elsewhere in the current repository, although this is not always so easy.
      One thing is for sure: copy and paste is the worst way, because it not
      only does takes away the original author's kudos, but it is also slower
      and more error-prone. Also rebasing from one feature or work branch to
      another is not always desirable. Instead, we have the following two
      methods at our disposal.


   Cherry-Picking
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. internal:: The preferred way of using codes from other branches is the use
      of :bash:`git cherry-pick`, but this may cause problems if a later commit
      in the other branch reverts the contained changes. Be sure that the
      cherry-picked commit contains exactly what you want to be changed, and be
      sure that these changes are not temporarily. If you have concerns about
      the latter, ask the author of this commit.


   Checkout From Other Branch
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. internal:: An more copy-paste-like alternative to cherry-picking is to
      checkout a file version from another branch. This may be useful if the
      changes you need are fragmented over multiple commits or the commit
      introduces other changes that are not required in any way for completing
      your task. For the latter you may remind the author about this guideline.


   Recover and Revoke
   -----------------------------------------------------------------------------

   .. internal:: At some point anyone messes up something, but if you regularly
      use Git for what it has been made, you should be able to recover. For
      example, to undo all changes in working tree use :bash:`git reset --hard
      HEAD`. If you are not sure that you messed up in the working tree, you can
      also use :bash:`git stash` to put all changes on a stack. With :bash:`git
      stash --pop` you can apply these changes again. If a "misdevelopment" has
      been made multiple commits earlier, you can go back with :bash:`git reset
      --hard <commit>`. To do this for single files, use :bash:`git checkout
      HEAD <file>` instead.

      To undo commits in a less destructive way, you can use :bash:git revert
      <commit>` which keeps old commits and adds an additional "revert" commit
      to the history. You can go back in history without resetting you working
      tree with :bash:`git reset <commit>`. This resets the committed and staged
      changes and leaves them in the working tree. :bash:`git reset --keep
      <commit>` will prevent the reset from overriding files in your working
      tree.
