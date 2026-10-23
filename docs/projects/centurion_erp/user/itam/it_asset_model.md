---
title: Asset Model
description: IT Asset Models Documentation for Centurion ERP by No Fuss Computing
date: 2026-10-23
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

An IT Asset model is for recording the manufacturer and model for an IT Asset. Additionally it also acts like a template. In that you can add to the model, sub asset connections. Then when you create an asset that uses the model, the asset will have the connections ready to add the actual sub assets.


## Features

The following fields/tabs are available to track items:

- [Connections](#connections)

- [Change History](../index.md#history)


### Details

The fields that show on this tab are the details of the asset Model. Available fields are:

- `Name`, _Required_ - The model name

- [Manufacturer](../access/company.md)

- [Asset Type](./asset_type.md)



Additionally you can set the fields that should be marked as mandatory. These fields are collectively an identifier, they are:

- International Mobile Equipment Identity (IMEI)

    For assets that have a sim card slot.

- Mac Address

    For assets that connect to a 802.3/802.11 network.

- Personal Unlocking Key (PUK)

    For assets that are a sim card.

- PUK Pin

    For assets that are a sim card.

- Serial Number

    For assets that were manufactured with a serial number.

Marking any of the above identifiers as mandatory, will force the assets that use this model to require the field of the same name to be filled-out.


### Connections

This tab shows the child connections for this model. Its intent is that you create each child asset and then when an asset is created using the model, those child connections will be created on the asset.

When creating a connection the following fields are available:

- `Name`, _Required_  The name you would like to give the connection.

- `Type`, _Optional_ - The asset Type to limit the child to.

- `Child Asset Model`, _Optional_ - The model to limit the child connection to.

As with a lot of assets, you may have multiple child assets to connect that are essentially the same with the exception of the name. As such, to cater for this. you can template the `Name` field with a range, i.e. `LAN1-5`. The range part is the suffix `1-5`. This tells Centurion ERP that when an asset is created using this model create five child connections with names `LAN1`, `LAN2`, `LAN3`, `LAN4`, and `LAN5`.
