---
name: New Database Model
about: Use when creating a new database model.
title: "New Model - <model table name>"
type: Task
labels: task::feature, triage, type::task
---

<!-- Add an intro -->


<!-- describe a use case if not covered in intro -->


## 📝 Details
<!-- 

Describe in detail the following:

- New model field
    - if foreign key field, what it's name will be or if it's not to be linked ensure specified and coded with `related_name = '+' to disable the link`. 
- How the UI will work, be layed out, new ui features etc
- custom permissions if required

-->


## 🚧 Tasks

<!-- Don't remove tasks strike them out. use `~~` before and after the item. i.e. `- ~~[ ] Model Created~~` note: don't include the list dash-->

- [ ] 🆕 [Model Created](https://nofusscomputing.com/projects/centurion_erp/development/models/)

- [ ] 🛠️ Migrations added

- [ ] ♻️ Serializer Created

- [ ] 🔄 [ViewSet Created](https://nofusscomputing.com/projects/centurion_erp/development/views/)

- [ ] 🔗 URL Route Added

- [ ] 🏷️ Model tag

    - [ ] 📘 Tag updated in the [docs](https://nofusscomputing.com/projects/centurion_erp/user/core/markdown/#model-reference)

    - [ ] tag added to class

- [ ] Admin Documentation added/updated _if applicable_

- [ ] Developer Documentation added/updated _if applicable_

- [ ] User Documentation added/updated

---

<!-- Add additional tasks here and as a check box list -->



### 🧪 Tests

- Unit Tests
    - [ ] [Model](https://nofusscomputing.com/projects/centurion_erp/development/models/#tests)
    - [ ] [ViewSet](https://nofusscomputing.com/projects/centurion_erp/development/views/#requirements)
    - [ ] Serializer
- Function Test
    - [ ] API Render (fields)
    - [ ] Model
    - [ ] [ViewSet](https://nofusscomputing.com/projects/centurion_erp/development/views/#requirements)


## ✅ Requirements

A Requirement is a must have. In addition will also be tested.

- [ ] Must have a [model_tag](https://nofusscomputing.com/projects/centurion_erp/user/core/markdown/#model-reference)

<!--

When detailing requirements the following must be taken into account:

- what the user should be able to do

- what the user should not be able to do

- what should occur when a user performs an action

-->

- Functional Requirements

    - Data integrity maintained

        - [ ] Create. _Data used to add to db equals the value supplied._

        - [ ] Update.  _Data used to add to db equals the value supplied._


- Non-Functional Requirements


---

<!-- Add additional requirement here and as a check box list -->
