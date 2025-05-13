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

- [ ] 🏷️ Model tag added to `app/core/lib/slash_commands/linked_model.CommandLinkedModel.get_model()` function

    - [ ] 📘 Tag updated in the [docs](https://nofusscomputing.com/projects/centurion_erp/user/core/markdown/#model-reference)
    - [ ] tag added to `app/core/lib/slash_commands/linked_model.CommandLinkedModel.get_model()`
    - [ ] ⚒️ Migration _Ticket Linked Item item_type choices update_

>[!note]
> Ensure that when creating the tag the following is adhered to:
> - Two words are not to contain a space char, `\s`. It is to be replaced with an underscore `_`
> - As much as practical, keep the tag as close to the model name as possible

- [ ] 📝 New [History model](https://nofusscomputing.com/projects/centurion_erp/development/core/model_history/) created

    - Sub-Models **_ONLY_**

        - [ ] Model class variable [`history_app_label`](https://nofusscomputing.com/projects/centurion_erp/development/models/#history) set to correct application label

        - [ ] Model class variable [`history_model_name`](https://nofusscomputing.com/projects/centurion_erp/development/models/#history) set to correct model label

- [ ] 📓 New [Notes model](https://nofusscomputing.com/projects/centurion_erp/development/core/model_notes/) created 
    - [ ] 🆕 Model Created
    - [ ] 🛠️ Migrations added
    - [ ] Add `app_label` to KB Models `app/assistance/models/model_knowledge_base_article.all_models().model_apps`
    - [ ] _(Notes not used/required) -_ Add `model_name` to KB Models `app/assistance/models/model_knowledge_base_article.all_models().excluded_models`
    - [ ] 🧪 [Unit tested](https://nofusscomputing.com/projects/centurion_erp/development/core/model_notes/#testing)
    - [ ] 🧪 [Functional tested](https://nofusscomputing.com/projects/centurion_erp/development/core/model_notes/#testing)

- [ ] Admin Documentation added/updated _if applicable_
- [ ] Developer Documentation added/updated _if applicable_
- [ ] User Documentation added/updated

---

<!-- Add additional tasks here and as a check box list -->



### 🧪 Tests

- Unit Tests
    - [ ] API Render (fields)
    - [ ] [Model](https://nofusscomputing.com/projects/centurion_erp/development/models/#tests)
    - [ ] ViewSet
- Function Test
    - [ ] History API Render (fields)
    - [ ] History Entries
    - [ ] API Metadata
    - [ ] API Permissions
    - [ ] Model
    - [ ] Serializer
    - [ ] ViewSet


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


- Non-Functional Requirements


---

<!-- Add additional requirement here and as a check box list -->
