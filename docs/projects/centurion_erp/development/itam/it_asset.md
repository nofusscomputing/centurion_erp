---
title: IT Asset
description: IT Asset Base Model Development Documentation for Centurion ERP by No Fuss Computing
date: 2025-05-08
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

IT Asset is a base model of Centurion ERP and contains all of the core features. This model is also a sub-model, and that of an [asset](../accounting/asset.md).


## Tests

- Unit

    - API Fields Rendering `itam.tests.unit.itamasset_base.test_unit_asset_base_api_fields.ITAMAssetBaseAPIInheritedCases`

    - Model `itam.tests.unit.itamasset_base.test_unit_asset_base_model.ITAMAssetBaseModelInheritedCases`

    - ViewSet `itam.tests.unit.itamasset_base.test_unit_asset_base_viewset.ITAMAssetBaseViewsetInheritedCases`

- Functional:

    - History `itam.tests.functional.itamasset_base.test_functional_asset_base_history.History`

    - Metadata `itam.tests.functional.itamasset_base.test_functional_asset_base_metadata.ITAMAssetBaseMetadataInheritedCases`

    - Permission `itam.tests.functional.itamasset_base.test_functional_asset_base_permission.ITAMAssetBasePermissionsAPIInheritedCases`

    - Serializer `itam.tests.functional.itamasset_base.test_functional_asset_base_serializer.ITAMAssetBaseSerializerInheritedCases`

    - ViewSet `itam.tests.functional.itamasset_base.test_functional_asset_base_viewset.ITAMAssetBaseViewSetInheritedCases`
