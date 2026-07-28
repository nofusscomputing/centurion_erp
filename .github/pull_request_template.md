### :books: Summary
<!-- your summary here emojis ref: https://github.com/yodamad/gitlab-emoji -->

<!--

You may as required add another L3 header here if you need to provide more detail than a summary.

-->




### :link: Links / References
<!-- 

    using a list as any links to other references or links as required. if relevant, describe the link/reference

    Include any issues or related merge requests. Note: dependent MR's also to be added to "Merge request dependencies"

-->



### :construction_worker: Tasks

<!--

Add any tasks you wish to this section. Its intent is for you to be able to keep track of items that need to be done.
Additionally the code reviewer can see and confirm if they are done so as to assist.

-->

 - [ ] Add your tasks here if required (delete)


<!--

DO NOT EDIT / CHANGE ANYTHING BELOW THIS LINE.

Exception: There has been a policy change and said change should be included below. If this occurs please 
raise an issue to address. Or `/cc` a maintainer to confirm that it's OK to update this template as part
of you pull request.

-->


#### :mag: Code Reviewer Tasks
<!--

The Following tasks are for the code reviewer.

    - Do NOT remove ANY tasks below strike through including the checkbox by enclosing in double tidle '~~'
    
-->

 - [ ] **Feature Release ONLY** :red_square: [Squash migration files](https://docs.djangoproject.com/en/5.2/topics/migrations/#squashing-migrations) :red_square: 
    _Multiple migration files created as part of this release are to be sqauashed into a few files as possible so as to limit the number of migrations_ 

- [ ] :firecracker: Contains breaking-change Any Breaking change(s)?

    _Breaking Change must also be notated in the commit that introduces it and in [Conventional Commit Format](https://www.conventionalcommits.org/en/v1.0.0/)._

    - [ ] :notebook: Release notes updated

- [ ] :blue_book: Documentation written

    _All features to be documented within the correct section(s). Administration, Development and/or User_

- [ ] :checkered_flag: Milestone assigned

- [ ] :gear: :test_tube: [Functional Test(s) Written](https://nofusscomputing.com/projects/centurion_erp/development/testing/)

- [ ] :test_tube: [Unit Test(s) Written](https://nofusscomputing.com/projects/centurion_erp/development/testing/)

    _ensure test coverage delta is not less than zero_

- [ ] :page_facing_up: Roadmap updated
