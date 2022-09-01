# -*- coding: utf-8 -*-
'''Unreal menu entry'''

from __future__ import annotations

import unreal
import proxi.dev as dev
import proxi.config as config
import proxi.common as common
import proxi.console as console
from proxi.models.menuBase import MenuItem, MenuSection, MenuSeparator, UnrealMenuObjectBase, SubMenu, TopLevelMenu

# level editor main menu ID
MAINMENU_ID = 'LevelEditor.MainMenu'

# Top level menus
TOPLEVELMENUS = [
    TopLevelMenu(
        id='DevMenu',
        name='Developer',
        tooltip='PROXi developer',
        devOnly=True,
        items= [
            MenuSection('Developer', 'Developer', [
                MenuItem('Toggle developer mode', 'import proxi.debug as x; x.toggleDevMode()', 'Toggles developer mode on/off'),
                MenuSeparator(),
                MenuItem('Material UI demo window', 'import proxi.ui.demoMainWindow as x; {} x.showWindow()'.format(dev.insertReloadForDev('x')), 'Launch a demo window showcasing the Qt Material integration'),
                MenuItem('Debug System Time', 'import proxi.ui.debugSystemTime as x; {} x.showWindow()'.format(dev.insertReloadForDev('x')), 'Launch a demo window showcasing the Qt Material integration')
            ])
        ]
    )    
]



# Recursion example below:
# MENUITEMS = (
#     menuSection('Tools', 'Tools', (
#         menuItem('Tool item 1', 'unreal.log("tool-one")'),
#         menuItem('Tool item 2', 'unreal.log("tool-two")'),
#         menuItem('Tool item 3', 'unreal.log("tool-three")'),
#         subMenu('ToolsSubMenu', 'Tools sub menu', (
#             menuSection('SubMenuSection', 'Sub Menu Section', (
#                 menuItem('Sub item 1', 'unreal.log("sub-one")'),
#                 menuItem('Sub item 2', 'unreal.log("sub-two")'),
#                 menuItem('Sub item 3', 'unreal.log("sub-three")'),
#                 subMenu('ToolsSubSubMenu', 'Tools sub sub menu', (
#                     menuItem('Sub sub item 1', 'unreal.log("sub-sub-one")'),
#                     menuItem('Sub sub item 2', 'unreal.log("sub-sub-two")'),
#                     menuItem('Sub sub item 3', 'unreal.log("sub-sub-three")')
#                 ))
#             )),
#             menuItem('Sub item 4', 'unreal.log("sub-four")'),
#             menuItem('Sub item 5', 'unreal.log("sub-five")'),
#         ))
#     )),
#     menuSection('Export', 'Export', (
#         menuItem('Export item 1', 'unreal.log("export-one")'),
#         menuItem('Export item 2', 'unreal.log("export-two")'),
#         menuItem('Export item 3', 'unreal.log("export-three")')
#     )),
#     # menuSeparator(),
#     menuSection('Debug', 'Debug', (
#         menuItem('Debug item 1', 'unreal.log("debug-one")'),
#         # menuSeparator(),
#         menuItem('About', 'unreal.log("debug-about")')
#     ))
# )



def getMainMenu() -> unreal.ToolMenu:
    '''Get main menu entry'''

    menus: unreal.ToolMenus = unreal.ToolMenus.get() # type: ignore
    return menus.find_menu(MAINMENU_ID) # type: ignore


def refresh():
    '''Refresh all menu widgets'''

    menus: unreal.ToolMenus = unreal.ToolMenus.get() # type: ignore
    menus.refresh_all_widgets()


def createMenu():
    '''Main logic to kick off menu creation'''

    # Clean up old if required
    deleteMenu()

    # Find main menu and insert PROXi
    console.log("Creating menus")
    mainMenu: unreal.ToolMenu = getMainMenu()

    #loops through the top level menus and creates the menus
    for topLevelMenu in TOPLEVELMENUS:

        if topLevelMenu.devOnly and not dev.DEV_MODE:
            console.log(f'Skipping top-level menu {topLevelMenu.name} -> This is only available in DEV MODE')
            continue

        console.log(f"Creating menu {topLevelMenu.name}")
        menu: unreal.ToolMenu = mainMenu.add_sub_menu(mainMenu.get_name(), '', topLevelMenu.id, topLevelMenu.name, topLevelMenu.tooltip) # type: ignore
        for topLevelItem in topLevelMenu.items:
            recurseMenuItems(topLevelItem, UnrealMenuObjectBase(unrealObject=menu))

    refresh()


def recurseMenuItems(item: UnrealMenuObjectBase, parent: UnrealMenuObjectBase, section: str=''):
    '''Recurse through all menu items and create and nest them as required'''

    # This is a collection of items
    if isinstance(item, (tuple, list)):
        for actual in item:
            recurseMenuItems(actual, parent, section)

        return

    # Skip some items for non-devs?
    if item.devModeOnly and not dev.DEV_MODE:
        console.log(f'Skipping menu item {item.label} (type {type(item)}) -> This is only available in DEV MODE')
        return

    # Sub menu
    if isinstance(item, SubMenu):
        item.unrealObject = parent.unrealObject.add_sub_menu(parent.unrealObject.get_name(), '', item.id, item.label, item.tooltip) # type: ignore
        section = ''
        recurseMenuItems(item.items, item, section) # type: ignore

    # Menu section
    elif isinstance(item, MenuSection):
        parent.unrealObject.add_section(item.id, label=item.label) # type: ignore
        item.unrealObject = parent.unrealObject
        recurseMenuItems(item.items, item, item.id) # type: ignore

    # Straight up menu item
    else:
        parent.unrealObject.add_menu_entry(section, item.create()) # type: ignore


def deleteMenu():
    '''Delete PROXi menu if it already exists. This will only really happen during development'''

    console.log('Deleting old menu contents, if required')
    menus: unreal.ToolMenus = unreal.ToolMenus.get() # type: ignore

    #loops through the top level menus and deletes the menus
    for topLevelMenu in TOPLEVELMENUS:
        console.log(f"Deleteing menu {topLevelMenu.name}")
        fullMenuPath = f'{MAINMENU_ID}.{topLevelMenu.id}'
        menus.unregister_owner_by_name(fullMenuPath)
        menus.remove_menu(fullMenuPath)