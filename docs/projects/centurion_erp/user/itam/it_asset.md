---
title: IT Assets
description: IT Assets Documentation for Centurion ERP by No Fuss Computing
date: 2024-05-15
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

This component within ITAM is intended to display information about an asset, be it a computer, router or switch etc. We have designed the IT Assets not as hard coded pre-defined assets, but as a thing you create and assemble as an asset. This is far superior than pre-defined assets like computer, mouse, printer and HDD etc. As assembling the assets yourself allows you to create a template for a common make of computer and another for a single one off custom computer you physically built yourself. Even better, if you have an asset with some random thing that can be connected to it, you can do that with our IT Assets.

IT Assets is not intended to cover **all** assets within an IT environment as there is a need that some assets be hard coded into the ITAM module. In this case the hard coded assets require some part of their lifecycle be managed by the ITAM module. Examples of some of these assets are:

- Certificates

- Operating Systems

- Softwares

The design of the IT Assets has been done to support creating and if required assembling the following assets:

- Hardware

    - Custom computer case

    - Case fan

    - Water cooling block

    - switch/router expansion port hardware

    - your custom piece of hardware

- Components

    - some electronic component. i.e. CPU, RAM, HDD etc

- Peripherals

    - Mouse

    - Keyboard

    - External HDD

- Devices (pre-build)

    - Computer

    - Mobile Phone

    - Model

    - Phone

    - Printer

    - Switch

    - WiFi Router

This list is not exhaustive and you are only limited by your imagination. Basically, you create an asset, if it can have a child connected to or part of it, you create the connection and the child asset can be connected.


## Features

The following Additional features are available for IT Asset Models:

- Links into [configuration management](../config_management/index.md)

- Records collected inventories

- Tracks:

    - Installed software details

    - Installed operating System

    - Deployed Services


### Status at a glance

On the devices list page you can quickly gauge the status of a device. It's a simple colour system: green=OK, red=bad, Orange=Warning and Grey=Unknown. This status icon denotes the age of the last inventory report, being: within 24-hours, within 72-hours, more than 72-hours and unknown. The latter generally indicates that no inventory has been performed.


### Details

The fields that show on this tab are the details of the asset. Available fields are:

- Details Section

    - [Model](./it_asset_model.md)

    - Name _Required_ - Name of this asset.

    - [Asset Type](./asset_type.md) _Read-Only_ - This field is obtained from the model.

    - UUID _Optional_ - UUID of this asset.

    - Last Inventory Date _Read-Only_ - Date the last inventory was collected.

    - Virtual Status _Optional, default: False_ Is this asset a virtual asset.

- Operating System Section

    - Shows the [operating system(s)](./operating_system.md) installed on this asset

- Deployed Services Section

    - Shows the [services](../itim/service.md) that are deployed upon this asset.

- Host Configuration Section

    - Shows the configuration for this asset.


Additionally if the asset was created with an [asset model](./it_asset_model.md), then depending upon what fields in the model were marked as mandatory, will determine what else will be displayed. Some other fields that may be shown:

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

Creating an asset without providing an [asset model](./it_asset_model.md), will have all of the previous listed fields displayed on the asset.


## Connections

This tab displays the available connections that this asset can have. Alongside that, will also display any child items connected to the asset.


## Software

This tab displays the [software](./software.md) installed upon the asset. Additionally it also provides the config management options for installing/uninstalling any software within ITAM.


## Config Management

This tab displays the fully rendered configuration for this asset. The fully rendered config is obtained from the [configuration groups](../config_management/index.md) the asset is part of, merged with the hosts configuration.
