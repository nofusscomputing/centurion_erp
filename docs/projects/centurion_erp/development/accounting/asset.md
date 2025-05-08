---
title: Asset
description: Asset Base Model Development Documentation for Centurion ERP by No Fuss Computing
date: 2025-05-05
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Asset is a base model of Centurion ERP and contains all of the core features. This allows for easier extensibility.


## Tests

- Unit

    - API Fields Rendering `accounting.tests.unit.asset_base.test_unit_asset_base_api_fields.AssetBaseAPIInheritedCases`

    - Model `accounting.tests.unit.asset_base.test_unit_asset_base_model.AssetBaseModelInheritedCases`

    - ViewSet `accounting.tests.unit.asset_base.test_unit_asset_base_viewset.AssetBaseViewsetInheritedCases`

- Functional:

    - History `accounting.tests.functional.asset_base.test_functional_asset_base_history.History`

    - Metadata `accounting.tests.functional.asset_base.test_functional_asset_base_metadata.AssetBaseMetadataInheritedCases`

    - Permission `accounting.tests.functional.asset_base.test_functional_asset_base_permission.AssetBasePermissionsAPIInheritedCases`

    - Serializer `accounting.tests.functional.asset_base.test_functional_asset_base_serializer.AssetBaseSerializerInheritedCases`

    - ViewSet `accounting.tests.functional.asset_base.test_functional_asset_base_viewset.AssetBaseViewSetInheritedCases`
