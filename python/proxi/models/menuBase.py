# -*- coding: utf-8 -*-
'''Base models for Unreal menu integration'''

from __future__ import annotations

import unreal


class UnrealMenuObjectBase(object):
    '''Unreal Menu Object Base Class'''

    def __init__(self, id: str=None, unrealObject: unreal.ToolMenu|unreal.ToolMenuEntry=None, label: str=None, devModeOnly: bool=False) -> None:
        '''Unreal Menu Object Base Class

        Args:
            id (str, optional): initializes and id else defaults to None.
            unrealObject (unreal.ToolMenu, optional): initializes and unrealObject else defaults to None.
            label (str, optional):initializes a label else defaults to None.
            devModeOnly (bool, optional): Defaults to False.
        '''
        self.id = id
        self.unrealObject = unrealObject
        self.devModeOnly = devModeOnly
        self.label = label


class MenuSection(UnrealMenuObjectBase):
    '''Menu Section Class'''

    def __init__(self, sectionId: str, sectionLabel: str, menuItems: list[UnrealMenuObjectBase], devModeOnly: bool=False) -> None:
        '''Menu Section Class

        Args:
            sectionId (str): Gets the sectionId
            sectionLabel (str): Gets the sectionLabel
            menuItems (list[UnrealMenuObjectBase]): Gets a list of UnrealMenuObjectBase
            devModeOnly (bool, optional): Defaults to False.
        '''
        super().__init__(
            id=sectionId,
            label=sectionLabel,
            devModeOnly=devModeOnly
        )
        self.items = menuItems


class SubMenu(UnrealMenuObjectBase):
    '''Sub Menu Class'''

    def __init__(self, menuId: str, menuLabel: str, menuItems: list[UnrealMenuObjectBase], menuTooltip: str='', devModeOnly: bool=False) -> None:
        '''Sub Menu Class

        Args:
            menuId (str): Gets the menuId
            menuLabel (str): Gets the menulabel
            menuItems (list[UnrealMenuObjectBase]): Gets a list of UnrealMenuObjectBase
            menuTooltip (str, optional): Gets the Menu Tool Tip else defaults to an empty string.
            devModeOnly (bool, optional): Defaults to False.
        '''
        super().__init__(
            id=menuId,
            label=menuLabel,
            devModeOnly=devModeOnly
        )
        self.tooltip = menuTooltip
        self.items = menuItems


class MenuItem(UnrealMenuObjectBase):
    '''Menu Item Class'''
    
    def __init__(self, itemLabel: str, itemCommand: str, itemToolTip='', devModeOnly: bool=False) -> None:
        '''Menu Item Class

        Args:
            itemLabel (str): Gets the itemLabel
            itemCommand (str): Gets the itemCommand
            itemToolTip (str, optional): Gets the Item Tool Tip else defaults to and empty string.
            devModeOnly (bool, optional): Defaults to False.
        '''
        super().__init__(
            label=itemLabel,
            devModeOnly=devModeOnly
        )
        self.command = itemCommand
        self.tooltip = itemToolTip

    # Creates an unreal object for the itemToolTip
    def create(self) -> unreal.ToolMenuEntry:
        if self.unrealObject:
            return self.unrealObject

        self.unrealObject = unreal.ToolMenuEntry(
            name='',
            type=unreal.MultiBlockType.MENU_ENTRY
        )
        self.unrealObject.set_label(self.label)
        self.unrealObject.set_string_command(
            type=unreal.ToolMenuStringCommandType.PYTHON,
            custom_type='',
            string=self.command
        )

        if self.tooltip:
            self.unrealObject.set_tool_tip(self.tooltip)

        return self.unrealObject


class MenuSeparator(UnrealMenuObjectBase):
    '''Menu Separator Class'''

    def __init__(self, devModeOnly: bool=False) -> None:
        '''Menu Separator Class

        Args:
            devModeOnly (bool, optional): Defaults to False.
        '''
        super().__init__(
            label='#separator', # debug only
            devModeOnly=devModeOnly
        )

    # Creates an unreal object for the menu separator
    def create(self) -> unreal.ToolMenuEntry:
        if self.unrealObject:
            return self.unrealObject

        self.unrealObject = unreal.ToolMenuEntry(
            name='',
            type=unreal.MultiBlockType.SEPARATOR
        )
        return self.unrealObject

    
class TopLevelMenu:
    '''Top Level Menu'''

    def __init__(self, id:str, name:str, tooltip:str, items:list[MenuSection], devOnly:bool=False) -> None:
        '''Top Level Menu

        Args:
            id (str): id(called name in unreal) of menu
            name (str): name(called label in unreal) of menu
            tooltip (str): tooltip for menu
            items (list[MenuSection]): list of items in menu
            devOnly (bool, optional): checks to see if its a developer or not. Defaults to False.
        '''

        self.id = id
        self.name = name
        self.tooltip = tooltip
        self.items = items
        self.devOnly = devOnly