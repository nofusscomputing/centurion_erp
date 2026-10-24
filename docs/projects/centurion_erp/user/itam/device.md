---
title: Assets
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

This list is not exhaustive and you are only limited by your imagination. Basically, you create an asset, if it can have a child connected to or part of it, you create the connection and the child asset.




## Features

For each device within your inventory, the following fields/tabs are available to track items:

- Name

- Model / Manufacturer

- Operating System

- Software

- Configuration

- Inventory

- [Change History](../index.md#history)

- Virtual Status


### Status at a glance

On the devices list page you can quickly gauge the status of a device. It's a simple colour system: green=OK, red=bad, Orange=Warning and Grey=Unknown. This status icon denotes the age of the last inventory report, being: within 24-hours, within 72-hours, more than 72-hours and unknown. The latter generally indicates that no inventory has been performed.


### Details

The fields that show on this tab are the details of the asset. Additionally if the asset was created with an asset model, then depending upon what fields in the model were marked as mandatory, will determine what else will be displayed. Some other fields that may be shown:

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

Creating an asset without providing an asset model, will have all of the previous listed fields displayed on the asset.

This tab display the details of the device.

To add a new model navigate to `settings -> ITAM -> Device Models`

Operating System is also visible on this tab with the version `name` as intended to be full [semver](https://semver.org/).

!!! note
    If you change the devices organization the config groups the device is a part of will be removed.


### Software

- Configuration key `software`

- Format `list of dict`

- Ansible Module `ansible.builtin.apt`

This tab displays both software actions and installed software. Software install details are added/updated by uploading an [inventory report](../api.md#inventory-reports).

You can specify a software action for any piece of software within the ITAM database. You can do this by pressing the `Add Software Action` button or if the software is installed clicking on the `+ Add` button on the row of the software to add the action to. An action can be set to either `Install` or `Remove` and you can also select a software version from the database if you choose to do so. Software actions are added to config management and can be pulled from the API for use within an Ansible playbook.

Display of both installed software and software actions is within a single row, if it's for the same software. Any software that you add an action to, will be displayed at the top of the list of software tab.

!!! info
    If you add a software action for software that is already installed using the `Add Software Action` button, an additional row will not be added as the applications logic is smart enough to check if the software is already installed.


### Configuration

This tab displays in `JSON` format configuration that is ready for use. Config from the [Config Management](../config_management/index.md) module is also included and rendered as part of this config. The intended audience is Ansible users with the fields provided matching established Ansible modules, if they exist.

This configuration can also be obtained from API endpoint `/api/config/<machine-slug>` where `<machine-slug>` would match the Ansible `inventory_hostname`.

The device can also have configuration defined. this configuration is intended to replicate Ansible `hostvars`. After all of the configuration has been rendered from the other modules that contain config, the devices configuration is applied last. In essence the devices configuration will always override any duplicated configuration.


### Inventory

!!! tip
    Within your "user settings" you must have a default organization set. Without this the inventory will not be added as this is how the inventory logic determines which organization for the device to be created in.

It's possible for a machine to be inventoried and have the report passed to the [inventory endpoint](../api.md#inventory-reports). This report will update the device within the interface and provides the option to use scheduled inventory gathering to keep the device up to date.

Inventory processing is conducted by a background worker. As soon as the inventory is uploaded, the inventory processing is added to the background worker queue. Further information about the background worker can be found within its [documentation](../core/index.md#background-worker). All inventory objects history entries will be added by a user called `System User` regardless of the user that was used to authenticated to upload the inventory. 

!!! tip
    Inventory not uploading? review the task logs by navigating to `Settings -> Application -> Task Logs`

The report can contain the following information:

- device:

    - `name` Device name

    - `serial number` Device serial number

    - `GUID/UUID` Device GUID/UUID

- operating System

    - `name` Operating system name

    - `version major` Operating system Major version number

    - `installed version` Full [semver](https://semver.org/) of the installed operating system

- software

    - `name` Software Name

    - `category` Software Category

    - `version` Software version

        !!! info
            When the software is added to the inventory, a regex search is done to return the [semver](https://semver.org/) of the software. if no semver is found, the version number provided is used.

Example Report

``` json

{
    "details": {
        "name": "string",
        "serial_number": "string",
        "uuid": "string"
    },
    "os": {
        "name": "name of os",
        "version_major": "major version number",
        "version": "as reported"
    },
    "software": [
        {
            "name": "string",
            "category": "string",
            "version": "string"
        }
    ]
}

```


#### Permissions

The user that uploads an inventory will require the correct permissions. The required permissions are as follows:

- `itam.add_device` For adding a new device via inventory

- `itam.change_device` For updating an existing device via inventory
