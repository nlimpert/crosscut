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


********************************************************************************
Stylistic Hints
********************************************************************************


Elements of the Robot Operating System
================================================================================

Different elements of :term:`ROS` are highlighted all over the offered material.
If you do not remember what a specific colour means or in case you have problems
distinguishing the used colours you can hover the element and a hint is shown.
For some official :term:`ROS` elements like messages you can directly navigate
to the official documentation by clicking on the highlighted element. Elements
that are created by ourselves within a tutorial are marked by a small "*i*".

-  Packages: :ros:package:`package` (dead link) or :ros:package-i:`package`
   mean that you are reading something about a :term:`ROS` package.

   .. hint:: For official packages like :ros:package:`sensor_msgs` there is a
      link generated which leads you directly to the wiki.

   .. internal:: Use :rst:`:ros:package:` or :rst:`:ros:package-i:`. The latter
      does not create a link to the wiki page of the package, due to the fact
      that it is suggested for unofficial packages.

      .. rst:role:: ros:package

         Used to highlight an official :term:`ROS` package and create a link to
         the online documentation.

         .. code-block:: rst

            :ros:package:`<package>`

      .. rst:role:: ros:package-i

         Used to highlight a non-official :term:`ROS` package, e.g. the ones
         created by ourselves.

         .. code-block:: rst

            :ros:package-i:`<package>`

-  Nodes: :ros:node:`node package` or :ros:node-i:`node package` mean that this
   is the program name of a :term:`ROS` node.

   .. internal:: Use :rst:`:ros:node:` or :rst:`:ros:node-i:`. For a shorter
      version add the keyword :rst:`short` before the package name.

      .. rst:role:: ros:node

         Used to highlight a node of an official :term:`ROS` package.

         .. code-block:: rst

            :ros:node:`<node> (short) <package>`

      .. rst:role:: ros:node-i

         Used to highlight a node of a non-official :term:`ROS` package.

         .. code-block:: rst

            :ros:node-i:`<package> (short) <node>`

-  Messages: :ros:message:`message package` (dead link) or
   :ros:message-i:`message package` are marked with a small "*m*", which allows
   you to distinguish between the different communication formats.

   .. hint:: For official messages like :ros:message:`Image sensor_msgs` there
      is a link generated which leads you directly to the message definition.

   .. internal:: Use :rst:`:ros:message:` or :rst:`:ros:message-i:`. For a
      shorter version add the keyword :rst:`short` before the package name.

      .. rst:role:: ros:message

         Used to highlight an official :term:`ROS` message and create a link to
         the online documentation.

         .. code-block:: rst

            :ros:message:`<message> (short) <package>`

      .. rst:role:: ros:message-i

         Used to highlight a non-official :term:`ROS` message, e.g. the ones
         created by ourselves.

         .. code-block:: rst

            :ros:message-i:`<message> (short) <package>`

-  Services: :ros:service:`service package` or :ros:service-i:`service package`
   are marked with a small "*s*", which allows you to distinguish between the
   different communication formats.

   .. hint:: For official services like :ros:service:`GetPlan nav_msgs` there
      is a link generated which leads you directly to the service definition.

   .. internal:: Use :rst:`:ros:service:` or :rst:`:ros:service-i:`. For a
      shorter version add the keyword :rst:`short` before the package name.

      .. rst:role:: ros:service

         Used to highlight an official :term:`ROS` service and create a link to
         the online documentation.

         .. code-block:: rst

            :ros:service:`<service> (short) <package>`

      .. rst:role:: ros:service-i

         Used to highlight a non-official :term:`ROS` service, e.g. the ones
         created by ourselves.

         .. code-block:: rst

            :ros:service-i:`<service> (short) <package>`

-  Actions: :ros:action:`action package` or :ros:action-i:`action package` are
   marked with a small "*a*", which allows you to distinguish between the
   different communication formats.

   .. hint:: For official actions like :ros:action:`MoveBase move_base_msgs`
      there is a link generated which leads you directly to action definition.

   .. internal:: Use :rst:`:ros:action:` or :rst:`:ros:action-i:`. For a shorter
      version add the keyword :rst:`short` before the package name.

      .. rst:role:: ros:action

         Used to highlight an official :term:`ROS` action and create a link to
         the online documentation.

         .. code-block:: rst

            :ros:action:`<action> (short) <package>`

      .. rst:role:: ros:action-i

         Used to highlight a non-official :term:`ROS` action, e.g. the ones
         created by ourselves.

         .. code-block:: rst

            :ros:action-i:`<action> (short) <package>`

-  Parameters: :ros:parameter:`parameter`, :ros:parameter-i:`parameter`,
   :ros:parameter-np:`parameter node package`, and :ros:parameter-inp:`parameter
   node package` represent different scenarios of how parameters are used. There
   are some that are used in a global manner and others that are only used to
   configure nodes.

   .. internal:: Use :rst:`:ros:parameter:`, :rst:`:ros:parameter-i:`,
      :rst:`:ros:parameter-np:` or :rst:`:ros:parameter-inp:`. For a shorter
      version add the keyword :rst:`short` before the node name or the package
      name.

      .. rst:role:: ros:parameter

         Used to highlight parameter that is used in an official setup.

         .. code-block:: rst

            :ros:parameter:`<parameter>`

      .. rst:role:: ros:parameter-i

         Used to highlight parameter that is used in a non-official setup, e.g.
         the ones we define by ourselves.

         .. code-block:: rst

            :ros:parameter-i:`<parameter>`

      .. rst:role:: ros:parameter-np

         Used to highlight parameter that is used by a node of an official
         :term:`ROS` packages.

         .. code-block:: rst

            :ros:parameter-np:`<parameter> (short) <node> (short) <package>`

      .. rst:role:: ros:parameter-inp

         Used to highlight parameter that is used by a node of a non-official
         :term:`ROS` packages, e.g. the ones we define by ourselves.

         .. code-block:: rst

            :ros:parameter-inp:`<parameter> (short) <node> (short) <package>`

-  Topics: :ros:topic:`topic`, :ros:topic-i:`topic`, :ros:topic-np:`topic node
   package`, and :ros:topic-inp:`topic node package` represent different
   scenarios of how topics are used. There are some that are used in a global
   manner and others that are only used by certain nodes.

   .. internal:: Use :rst:`:ros:topic:`, :rst:`:ros:topic-i:`,
      :rst:`:ros:topic-np:` or :rst:`:ros:topic-inp:`. For a shorter version add
      the keyword :rst:`short` before the node name or the package name.

      .. rst:role:: ros:topic

         Used to highlight topic that is used in an official setup.

         .. code-block:: rst

            :ros:topic:`<topic>`

      .. rst:role:: ros:topic-i

         Used to highlight topic that is used in a non-official setup, e.g.
         the ones we define by ourselves.

         .. code-block:: rst

            :ros:topic-i:`<topic>`

      .. rst:role:: ros:topic-np

         Used to highlight topic that is used by a node of an official
         :term:`ROS` packages.

         .. code-block:: rst

            :ros:topic-np:`<topic> (short) <node> (short) <package>`

      .. rst:role:: ros:topic-inp

         Used to highlight parameter that is used by a node of a non-official
         :term:`ROS` packages, e.g. the ones we define by ourselves.

         .. code-block:: rst

            :ros:topic-inp:`<topic> (short) <node> (short) <package>`


Other Elements
================================================================================

-  Files: Files and paths look like :file:`path/file_name` or
   :file:`/home/{user}/catkin_ws` if there is a user-specific part.

   .. internal:: Use the :rst:`:file:` role for files to provide a uniform look.

      .. code-block:: rst

         :file:`path/file_name`
         :file:`/home/{user}/catkin_ws`

-  Multimedia: Mostly directly embedded and available for download.

   :Embedded:
      .. raw:: html

          <video width="480" controls>
            <source src="_downloads/big_buck_bunny_trailer.ogg" type="video/mp4">
            Your browser does not support the video tag.
          </video>

   :Downloadable:
      :download:`Big Buck Bunny (Trailer)
      <_resource/video/big_buck_bunny_trailer.ogg>`


   .. internal:: Embed videos with raw HTML 5.

      .. code-block:: rst

            .. raw:: html

                <video width="480" controls>
                  <source src="_downloads/big_buck_bunny_trailer.ogg"
                          type="video/mp4">
                  Your browser does not support the video tag.
                </video>

      Provide downloads with the :rst:`:download:` role, do not use normal
      links for this purpose.

      .. code-block:: rst

         :download:`Big Buck Bunny (Trailer) <_resource/video/big_buck_bunny_trailer.ogg>`

-  Keyboard-Shortcuts: :kbd:`Ctrl-C Ctrl-V Alt-Del` whereby the minus sign links
   key combinations and the space separates individual steps of a key stroke.

   .. only:: internal

      Use the :rst:`:kbd:` role to introduce a key stroke or sequence. Always
      use the text that is imprinted on a "standard" UK QWERTY keyboard:
      :code:`Ctrl`, :code:`Alt`, :code:`Tab`, :code:`Shift`, :code:`Del`, and so
      on. Do never use lowercase and uppercase to substitute a :code:`Shift`,
      like :kbd:`Shift-a` :math:`\not\rightarrow` :kbd:`A`. Always use
      capitalized letters as they are imprinted on a keyboard. This is not to be
      applied for symbols like :kbd:`$` :math:`\not\rightarrow` :kbd:`Shift-4`
      because this may not work with other layouts. Combined strokes have to be
      connected with a minus sign "-" and sequences have to be delimited by
      spaces " ".

      .. code-block:: rst

         :kbd:`Ctrl-C Ctrl-V Alt-Del`
         :kbd:`Ctrl-a Del`

-  GUI Elements: Different elements have different appearances.

   :Button:
      .. Never do this in any other document, NEVER!

      :raw-html:`<span onclick="window.alert('Hahaha, what did you think would happen?')"><span>`
      :gui:button:`Please, click me`
      :raw-html:`</span></span>`

   :Text/Label:
      :gui:text:`This is a label`

   :Radio:
      :gui:radio:`Normal radio button`

      :gui:radio-selected:`Selected radio button`

   :Checkbox:
      :gui:checkbox:`Normal check box`

      :gui:checkbox-selected:`Selected check box`

      :gui:checkbox-indeterminate:`Indeterminate check box`

   :Textbox:
      :gui:textbox:`Text box`

   :Dropdown:
      :gui:dropdown:`Drop-down menu`


   :Menu Selection:
      :menuselection:`&File --> E&xit`.

   .. internal:: Use the different roles of the :rst:`:gui:` domain for any
      kinds of GUI elements and the :rst:`:menuselection:` role for menu paths.

      .. code-block:: rst

         :menuselection:`&File --> E&xit`

      .. rst:role:: gui:text

         Create a label or text which can be used to reference an actual GUI
         element.

         .. code-block:: rst

            :gui:text:`This is a label`

      .. rst:role:: gui:button

         Create a button which can be used to reference an actual GUI element.

         .. code-block:: rst

            :gui:button:`Please, click me`

      .. rst:role:: gui:radio

         Create a radio button which can be used to reference an actual GUI
         element.

         .. code-block:: rst

            :gui:radio:`Normal radio button`

      .. rst:role:: gui:radio-selected

         Create a selected radio button which can be used to reference an actual
         GUI element.

         .. code-block:: rst

            :gui:radio-selected:`Selected radio button`

      .. rst:role:: gui:checkbox

         Create a check box which can be used to reference an actual GUI
         element.

         .. code-block:: rst

            :gui:checkbox:`Normal check box`

      .. rst:role:: gui:checkbox-selected

         Create a selected check box which can be used to reference an actual
         GUI element.

         .. code-block:: rst

            :gui:checkbox-selected:`Selected check box`

      .. rst:role:: gui:checkbox-indeterminate

         Create a indeterminate check box which can be used to reference an
         actual GUI element.

         .. code-block:: rst

            :gui:checkbox-indeterminate:`Indeterminate check box`

      .. rst:role:: gui:textbox

         Create a text box which can be used to reference an actual GUI element.

         .. code-block:: rst

            :gui:textbox:`Text box`

      .. rst:role:: gui:dropdown

         Create a drop-down menu which can be used to reference an actual GUI
         element.

         .. code-block:: rst

            :gui:dropdown:`Drop-down menu`


.. _guideline-admonitions:

Admonitions
================================================================================

:Hint:
   A "hint" gives some useful information that can be used to e.g. fulfill a
   task or to understand the previous text.

   .. hint:: This is a hint.

   .. internal:: Use the :rst:`hint` directive to produce this admonition.

      .. code-block:: rst

         .. hint:: This is a hint.

:Note:
   A "note" gives additional information that is not necessary in the current
   context but may be useful later or in general.

   .. note:: This is a note.

   .. internal:: Use the :rst:`note` directive to produce this admonition.

      .. code-block:: rst

         .. note:: This is a note.

:Warning:
   A "warning" requires extraordinary attention. At this point a problem or an
   error occurs frequently, which can be avoided by following the warning's text
   exactly.

   .. warning:: This is a warning.

   .. internal:: Use the :rst:`warning` directive to produce this admonition.

      .. code-block:: rst

         .. warning:: This is a warning.

:Danger:
   A "danger" admonition explicitly advises that irreversible damage to the
   software, in particular to the hardware, can occur at this point. The
   instructions must be strictly followed.

   .. danger:: This is a danger.

   .. internal:: Use the :rst:`danger` directive to produce this admonition.

      .. code-block:: rst

         .. danger:: This is a danger.

:Task:
   A "task" tells you what to do in order to get closer to the goal of the
   course.

   .. task:: This is a task.

   .. internal:: Use the :rst:`task` directive to produce this admonition. This
      is not a standard directive of reStructuredText, so it requires the
      :code:`rosin.didactic` extension.

      .. code-block:: rst

         .. task:: This is a task.

.. only:: internal

   :Internal Note:
      An "internal note" is not visible to the reader, it is intended to be read
      by authors and trainers only.

      .. internal:: Use the :rst:`internal` directive to... well it is getting
         too meta in here. This is not a standard directive of reStructuredText,
         so it requires the :code:`rosin.didactic` extension.

         .. code-block:: rst

            .. internal:: This is an internal.

            .. only:: internal

               This will also be visible only to internals, but without
               this beautiful box. This is e.g. necessary if you want to
               hide captions.

   All other available admonitions are not allowed in this project.


Lists and Enumerations
================================================================================

- Enumerations always indicate either a fixed or usual order of operations, like

   :Example:

      #. Start the :bash:`roscore`.
      #. Run the node.

   or a set of rules

   :Example:

      #. You do not talk about Fight Club.
      #. You *do not* talk about Fight Club.
      #. If someone says "stop" or goes limp, taps out the fight is over.
      #. Only two guys to a fight.
      #. One fight at a time.
      #. No shirts, no shoes.
      #. Fights will go on as long as they have to.
      #. If this is your first night at Fight Club, you *have* to fight.

-  For all other cases an unordered list is used, e.g. for a number of task that
   can be done in any order

   :Example:
      -  Start the subscriber.
      -  Start the publisher.

   or a shopping list

   :Example:
      -  Tricycle
      -  :strike:`Key to room 237` Large Axe
      -  Some crazy eyes


.. _guideline_references:

References
================================================================================

:Figures:
   .. _rosin_logo:
   .. figure:: /_resource/image/logo/rosin.svg
      :width: 50%
      :align: center

      The Best Robotics Project in the Whole Wide World

   A figure will be referenced as :numref:`rosin_logo`.

   .. internal:: If a figure is nowhere referenced in the text it might be
      expandable. Every figure should therefor have a name and should be
      referenced using the :rst:`:numref:` role.

      .. code-block:: rst

         .. _rosin_logo:
         .. figure:: /_resource/image/logo/rosin.svg
            :align: center
            :width: 50%

            The Best Robotics Project in the Whole Wide World

         :numref:`rosin_logo`

:Tables:
   .. _rosin_table:
   .. table:: Some Table About ROSIN.

      +---------------------+------+
      | Pros                | Cons |
      +=====================+======+
      | ROS                 | ---  |
      | and everything else |      |
      +---------------------+------+

   A table will be referenced as :numref:`rosin_table`,

   .. internal:: If a table is nowhere referenced in the text is might be
      expandable. Every table should therefor have a name and should be
      referenced using the :rst:`:numref:` role.

      .. code-block:: rst

         .. _rosin_table:
         .. table:: Some Table About ROSIN.

            +---------------------+------+
            | Pros                | Cons |
            +=====================+======+
            | ROS                 | ---  |
            | and everything else |      |
            +---------------------+------+

         :numref:`rosin_table`

:Sections:
   A section will be referenced as :numref:`guideline_references`.

   .. internal:: Labeled sections can be referenced just as figures and tables
      using the :rst:`:numref:` role.

      .. code-block:: rst

         .. _guideline_references:

         References
         ================================================================================

         :numref:`guideline_references`

:Terms:
   Terms will be linked to the glossary, like :term:`ROSIN`.


   .. internal:: Terms in a glossary can be referenced with the :rst:`:term:`
      role.

      .. code-block:: rst

         .. glossary::

            ROSIN
               ROS Industrial, not to be confused with
               the german chef Frank Rosin.

         :term:`ROSIN`


Text Formatting
================================================================================

[TBD]

.. only:: internal

   Never combine bold and italics. Use both sparse.

Italics are used

#. to emphasize words, is not synonymous for nothing

   .. only:: internal

      .. hint:: Use italics in this case only when [TBD]

#. or to encourage the reader to critically question the meaning.

   .. only:: internal

      .. hint:: Use italics in this case only when [TBD]

#. or to make reasoning easier, e.g. "...we now want to use the algorithm
   *which we've implemented yesterday* to...".

   .. only:: internal

      .. hint:: Use italics in this case only when [TBD]

Use bold text only for things that are very often and very easily done wrong
respectively are forgotten. An admonition might be the better option.
[TBD] (the above does not apply)


Documentation of Programs
================================================================================

Options of programs are documented as follows and can also be linked as
:option:`test -t`.

:Example:
   .. program:: test

   This is a list of options available for the :program:`test` program.

   .. option:: -c

      That helps you cheat... or does it consult a coach? I don't know anymore.

   .. option:: -t

      This will test your knowledge about ROS.

.. internal:: Programs and options can be defined with the :rst:`program` and
   :rst:`option` directives, and referenced with the roles of the same name.

   .. code-block:: rst

      .. program:: test

      This is a list of options available for the :program:`test` program.

      .. option:: -c

         That helps you cheat... or does it consult a coach? I don't know anymore.

      .. option:: -t

         This will test your knowledge about ROS.

      :program:`test`
      :option:`test -t`


********************************************************************************
Teaching Approach
********************************************************************************

[TBD]

.. the following is taken from meeting minutes
.. we need to define the target groups
.. we need to define the intended learning outcomes
.. we need to motivate students (and later industry) for ROS
.. - teach how to do (accomplish) something in ROS that is currently being done with traditional automation.
.. - then move to the next level, do the next step, do something intelligent with ROS (some task that requires the machine intelligence and flexibility that comes with ROS)

.. How to Implement Constructive Alignment
.. What is important
.. - Student Learning Focus (activation)
.. - Student Motivation (intrinsic -vs- extrinsic)
.. - Constructivism (transmission is dead, knowledge is actively constructed)
.. - SOLO Taxonomy (hierarchy of competences, deep learning)
.. - Alignment (make explicit ILOs (Intended Learning Outcomes, exam = ILO = assessment))
.. How do people get good at something?
.. Not because somebody told them but because they practiced it!
.. --> Knowledge is actively constructed.
.. Main idea of alignment: Exams are supposed to assess "explain, relate, prove, apply"

.. the most important thing to start with is defining the learning outcomes
.. It is important to fix the teacher's intention
.. → From content to competence
.. Competence as goals: from nouns to verbs
.. competence := knowledge + capacity to /act/ upon it
.. understanding is of course pre-requisitional! inherently operational


Levels
================================================================================

The teaching material is grouped into different levels, which are marked
accordingly.

.. level:: beginner advanced

   This section should show up only for the levels "beginner", "advanced",
   and "all".

   The border on the right indicates were this region ends.

.. level:: intermediate

   This section should show up only for intermediates and "all".

.. level:: advanced

   This section should show up only for advanced and "all".


Scenarios
================================================================================

Beyond the levels, the material is also grouped into different scenarios.
Sections that focus to a specific scenario are marked accordingly.

.. scenario:: linux

   This section should show up only for the scenarios "linux" and "all".

.. scenario:: turtle_bot_3

   This section should show up only for turtle_bot_3 and "all".

.. scenario:: turtle_sim

   This section should show up only for turtle_sim and "all".

.. level:: advanced

   .. scenario:: linux

      This is visible for "advanced" level with the "linux" scenario.
