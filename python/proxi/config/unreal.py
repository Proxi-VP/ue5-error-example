# -*- coding: utf-8 -*-
'''Unreal config'''

from __future__ import annotations

import re
import unreal
import proxi.common.strings as strings

from typing import Any
from .abbreviations import Abbreviations
from proxi.models import (
    Version,
    UnrealObjectType,
    SequenceGeneratorRootFolder,
    SequenceGeneratorFolder,
    SequenceGeneratorFile,
    _SequenceGeneratorObjectBase,
    SequenceMaster,
    TechVizType
)


class Unreal:
    '''Unreal configuration'''

    firstCameraNumber = 1
    cameraSeriesNumber1 = 1000
    cameraSeriesNumber2 = 2000
    cameraSeriesNumber3 = 3000
    cameraSeriesNumber4 = 4000
    cameraSeriesNumber5 = 5000
    cameraSeriesNumber6 = 6000
    cameraSeriesNumber7 = 7000
    cameraSeriesNumber8 = 8000
    cameraSeriesNumber9 = 9000
    camKitsPath = 'blueprints/cam-kits' # Implicit /Game/<GameName>/
    measureToolPath = '/Game/proxiDex/proxiCore/blueprints/techViz/measureTool'
    measureToolEndPath = '/Game/proxiDex/proxiCore/blueprints/techViz/measureTool/BP_measureToolEnd.BP_measureToolEnd'
    measureToolOriginPath = '/Game/proxiDex/proxiCore/blueprints/techViz/measureTool/BP_measureToolOrigin.BP_measureToolOrigin'
    sceneCapturePath = '/Game/proxiDex/proxiCore/blueprints/techViz/cameraTechViz/BP_TV-PiP_sceneCapture.BP_TV-PiP_sceneCapture'
    staticMeshPath = '/Game/proxiDex/proxiCore/blueprints/techViz/cameraTechViz/SM_CineCamTechViz.StaticMeshActor'
    techVizCamPath = '/Game/proxiDex/proxiCore/lensing/proxiCam/cam-kits/techViz/BP_proxiTechViz.BP_proxiTechViz'
    techVizBodyPath = '/Game/proxiDex/proxiCore/lensing/proxiCam/cam-kits/techViz'
    placeholderAssetName = '_placeholder'
    currentGamePattern = re.compile(r'^(\/[Gg]ame\/.+?\/).*')
    sequencePattern = re.compile(r'^([a-zA-Z]{3})')
    masterWorldPattern = re.compile(r'_Master$')
    masterSequencePattern = re.compile(r'\-[A-Z]$')
    masterSequenceDetailedPattern = re.compile(r'^([a-zA-Z]{3})(\d{2})[-_]([a-zA-Z]{2})[-_]([a-zA-Z])$')
    masterSequenceDetailedShortPattern = re.compile(r'^([a-zA-Z]{3})(\d{2})$')
    shotCodePattern = re.compile(r'(\w+?\d{2})[-_]([a-zA-Z]{2})[-_]([a-zA-Z])(\d)(\d{3})([a-zA-Z]?)')
    engineVersionPattern = re.compile(r'^(\d)\.(\d{1,2})\.(\d{1,2})')
    animClipPattern = re.compile(r'^(.+?(?:[tT][xX]|[vV][zZ])[-_].*?(?:\w[-_])?)(([aA][bB])(\d{3}))?(.+?[-_])([vV])?((\d{3,4})|(TEMPLATE))$')
    animBasePattern = re.compile(r'^([a-zA-Z]{3})(\d{2})([-_])([a-zA-Z]{2})([-_])([a-zA-Z])(.*$)')
    defaultFrameRate = 24.0
    defaultSequenceLengthSeconds = 200.0
    defaultSequenceLengthFrames = int(defaultSequenceLengthSeconds * defaultFrameRate)
    defaultAnimClipLengthSeconds = 30.0
    defaultAnimClipLengthFrames = int(defaultAnimClipLengthSeconds * defaultFrameRate)
    defaultRenderPaddingSeconds = 5.0
    defaultRenderPaddingFrames = int(defaultRenderPaddingSeconds * defaultFrameRate)
    defaultActionClipLengthSeconds = 10.0
    defaultActionClipLengthFrames = int(defaultActionClipLengthSeconds * defaultFrameRate)

    class EngineVersion:
        '''A collection of static engine versions useful for various feature-comparisons'''

        _4_26_0 = Version(4, 26, 0)
        _4_26_1 = Version(4, 26, 1)
        _4_26_2 = Version(4, 26, 2)
        _4_27_0 = Version(4, 27, 0)
        _4_27_1 = Version(4, 27, 1)
        _4_27_2 = Version(4, 27, 2)
        _5_0_0 = Version(5, 0, 0)

    class FieldName:
        '''Field/variable names. Usually used via `[get|set]_editor_property()`'''

        cameraBody = 'SetCameraType'
        focalLength = 'current_focal_length'
        guid = 'actor_guid'

    class Folder:
        shared = 'shared'
        subSequences = 'subSequences'
        subLevels = 'subLevels'
        cameras = 'cameras'
        animation = 'animation'
        sequences = 'sequences'
        clips = 'clips'
        test = 'test'
        cameraTechViz = 'cameraTechViz'
        measureTool = 'measureTool'

    class ActorNameStorage:
        actorName = 'BP_actorNameStorage'
        actorPath = '/Game/proxiDex/proxiCore/blueprints/techViz/actorTechViz/BP_actorNameStorage'

        class Fields:
            actorNamesEncoded = 'ActorNamesEncoded'

    class TechViz:
        suffixCamCommon = '_TVCAM-'
        suffixCam1 = f'{suffixCamCommon}01'
        suffixCam2 = f'{suffixCamCommon}02'
        suffixCam3 = f'{suffixCamCommon}03'
        suffixCam4 = f'{suffixCamCommon}04'

        suffixRenderCommon = '_TV-'

        #TV DIST 01 section
        suffixDistCamOrigin = 'TV-dist01_origin'

        suffixDistCamEndCommon = 'TV-dist01_end'
        suffixDistCam1 = f'{suffixDistCamEndCommon}01'
        suffixDistCam2 = f'{suffixDistCamEndCommon}02'
        suffixDistCam3 = f'{suffixDistCamEndCommon}03'
        suffixDistCam4 = f'{suffixDistCamEndCommon}04'
        suffixDistCam5 = f'{suffixDistCamEndCommon}05'

        #TVDIST 02 section
        suffixDist2CamOrigin = 'TV-dist02_origin'

        suffixDist2CamEndCommon = 'TV-dist02_end'
        suffixDist2Cam1 = f'{suffixDist2CamEndCommon}01'
        suffixDist2Cam2 = f'{suffixDist2CamEndCommon}02'
        suffixDist2Cam3 = f'{suffixDist2CamEndCommon}03'
        suffixDist2Cam4 = f'{suffixDist2CamEndCommon}04'
        suffixDist2Cam5 = f'{suffixDist2CamEndCommon}05'

        proxi = TechVizType(
            suffix=f'{suffixRenderCommon}proxi',
            description='PROXi Preset',
            enabled=True
        )
        prod = TechVizType(
            suffix=f'{suffixRenderCommon}prod',
            description='Production Preset',
            enabled=True
        )

        dist = TechVizType(
            suffix=f'{suffixRenderCommon}dist',
            description='Camera Distance',
            enabled=True
        )

        # TODO: Enable this once implemented in `tools.techviz`
        camOH = TechVizType(
            suffix=f'{suffixRenderCommon}cam_oh',
            description='Camera Overhead View',
            enabled=True
        )
        # TODO: Enable this once implemented in `tools.techviz`
        camSplit = TechVizType(
            suffix=f'{suffixRenderCommon}cam_split',
            description='Camera Multi View',
            enabled=True
        )

        craneOH = TechVizType(
            suffix=f'{suffixRenderCommon}crane_oh',
            description='Crane Overhead View',
            enabled=False
        )
        craneSplit = TechVizType(
            suffix=f'{suffixRenderCommon}crane_split',
            description='Crane Multi View',
            enabled=False
        )
        # prodFull = TechVizType(
        #     suffix=f'{suffixCommon}prod_full',
        #     description='Production Preset Full',
        #     enabled=False
        # )
        # secondUnit = TechVizType(
        #     suffix=f'{suffixCommon}2U',
        #     description='Second Unit Preset',
        #     enabled=False
        # )

        _displayOrder = [
            proxi,
            prod,
            # prodFull,
            # secondUnit,
            dist,
            camOH,
            camSplit,
            craneOH,
            craneSplit
        ]

        @classmethod
        def getAllTypes(cls) -> list[TechVizType]:
            return cls._displayOrder

    class Sequencer:
        '''Unreal sequencer specific options'''

        camsTrackLabel = '_CAMS'
        animTrackLabel = '_ANIM'

    class CameraCodeSequenceType:
        '''Unreal camera sequence code abbreviations'''

        toyBox = Abbreviations.toyBox
        proxiViz = Abbreviations.proxiViz

    class CameraTypeMapping:
        '''Lookup/mapping between custom Unreal Enumeration `ECameraType` and Shotgun field Shot.sg_camera_type_1

        Public static access method via one-way method `getShotgunValue`
        '''

        # Unreal ECameraType idx -> Shotgun value (null allowed)
        _lookup = {
            0: None,
            1: 'Red Monstro',
            2: 'Arri Alexa LF',
            3: 'TechViz'
        }

        # Specific reference to TechViz. Storing here for easy update if the above list changes
        _techVizLabel = _lookup[3]

        @classmethod
        def getShotgunValue(cls, idxOrEnum: Any) -> str:
            '''Retrieve the corresponding Shotgun string-value for index or enum entry in PROXi specific enumeration `ECameraType`

            Args:
                idxOrEnum (unreal.EnumBase|int): Index or enum entry to look up

            Raises:
                KeyError: `idxOrEnum` is not found in lookup table
                TypeError: `idxOrEnum` is not of a recognised type and cannot be used for lookup

            Returns:
                str: Shotgun compatible string-value for field `Shot.sg_camera_type_1`
            '''

            if isinstance(idxOrEnum, unreal.EnumBase):
                return cls._lookup[idxOrEnum.value] # type: ignore
            elif isinstance(idxOrEnum, int): # type: ignore
                return cls._lookup[idxOrEnum]
            else:
                raise TypeError('Object or index `{}` is not a valid lookup key'.format(idxOrEnum))

        @classmethod
        def isTechVizCamera(cls, idxOrEnum: Any=None, label: str|None=None) -> bool:
            '''Check if a given camera (by index, enum or label) is considered a TechViz camera

            Args:
                idxOrEnum (int|unreal.EnumBase, optional): Index or enum entry to fetch label for. Defaults to None.
                label (str, optional): Pre-fetched label. Defaults to None.

            Raises:
                ValueError: No valid argument supplied

            Returns:
                bool: True if camera is considered a TechViz camera
            '''

            if idxOrEnum is None and label is None:
                raise ValueError('Neither index, enum, or label was provided for lookup')

            label = cls.getShotgunValue(idxOrEnum) if idxOrEnum is not None else label
            return bool(label == cls._techVizLabel)


    class SequenceTypeMapping:
        '''Lookup/mapping between Unreal camera name abbreviation and Shotgun field `Shot.sg_shot_type`

        Public static access method via one-way method `getShotgunValue`
        '''

        _lookup = {
            Abbreviations.toyBox: 'ToyBox',
            Abbreviations.proxiViz: 'ProxiViz'
        }

        @classmethod
        def getShotgunValue(cls, sequenceTypeCode: str|None):
            '''Retrieve the corresponding Shotgun string-value for key `sequenceTypeCode`

            Args:
                sequenceTypeCode (str): Abbreviated shot type code (tx, vz, etc)

            Returns:
                str|None: Full code if found, None otherwise
            '''

            if not sequenceTypeCode:
                return None

            return cls._lookup.get(sequenceTypeCode.lower())

    class SequenceFolderStructure:
        '''Retrieve and create sequence folder structure for a given `SequenceMaster`'''

        class AssetNames:
            masterMap = '_Master'
            actorsMap = '_ACTORS'
            actorsBlockoutMap = '_ACTORS-blockout'
            envBlockoutMap = '_ENV-blockout'
            envBuildingsMap = '_ENV-buildings'
            envLandscapeMap = '_ENV-landscape'
            fxEnvMap = '_FX-env'
            lxEnvMap = '_LX-env'
            ppSharedMap = '_PP-shared'

            fxCharMap = '_FX-char'
            lxCineMap = '_LX-cine'
            tvDistMap = '_TV-dist'
            tvCamsMap = '_TV-cams'

            animSequence = '_ANIM'
            camsMap = '_CAMS'
            camsSequence = camsMap



        _buffer: list[_SequenceGeneratorObjectBase] = []

        @classmethod
        def getStructure(cls, projectName: str, master: SequenceMaster) -> list[_SequenceGeneratorObjectBase]:
            '''Generate a default PROXi sequence structure based on the given `ProjectName` and `SequenceMaster`'''

            
            if not projectName or not master:
                unreal.log_error('SequenceFolderStructure.getStructure(): Either project name or sequence master is missing')
                unreal.log_error(f'Project name: {projectName}')
                unreal.log_error(f'Master: {master}')
                return []

            projectNameUpper = projectName.upper() # NECTAR
            sequenceCodeUpper:str|None = master.sequence['code'].upper() # BFA
            sequenceCodeLower = master.sequence['code'].lower() # bfa
            sequenceNameCamel = strings.camelCase(master.sequence["name"]) # bulletFarmAmbush
            subSequenceCodeUpper = master.subSequence['code'].upper() # BFA01
            subSequenceCodeLower = master.subSequence['code'].lower() # bfa01
            shotTypeCodeUpper = master.type.upper() # TX
            shotTypeCodeLower = master.type.lower() # tx
            shotTypeNameCamel = strings.camelCase(Unreal.SequenceTypeMapping.getShotgunValue(shotTypeCodeLower)) # toyBox
            sequenceMasterLetterUpper = master.masterLetter.upper()

            _hierarchy = SequenceGeneratorRootFolder(f'/Game/{projectNameUpper}', [
                        SequenceGeneratorFolder(Unreal.Folder.sequences, [
                            SequenceGeneratorFolder(f'{sequenceCodeUpper}_{sequenceNameCamel}', [
                                SequenceGeneratorFile(f'{sequenceCodeUpper}.uasset', UnrealObjectType.levelSequence),
                                SequenceGeneratorFile(f'{sequenceCodeUpper}{cls.AssetNames.masterMap}.umap', UnrealObjectType.world),
                                SequenceGeneratorFolder(Unreal.Folder.shared, [
                                    SequenceGeneratorFolder(Unreal.Folder.subLevels, [
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.actorsMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.actorsBlockoutMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.envBlockoutMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.envBuildingsMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.envLandscapeMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.fxEnvMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.lxEnvMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.ppSharedMap}.umap', UnrealObjectType.level)
                                    ])
                                ]),
                                SequenceGeneratorFolder(f'{shotTypeCodeUpper}_{shotTypeNameCamel}', [
                                    SequenceGeneratorFolder(f'{subSequenceCodeUpper}_{shotTypeCodeUpper}', [
                                        SequenceGeneratorFolder(Unreal.Folder.shared, [
                                            SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.fxCharMap}.umap', UnrealObjectType.level),
                                            SequenceGeneratorFile(f'{subSequenceCodeLower}{cls.AssetNames.fxEnvMap}.umap', UnrealObjectType.level),
                                            SequenceGeneratorFile(f'{subSequenceCodeLower}{cls.AssetNames.lxCineMap}.umap', UnrealObjectType.level),
                                            SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.tvDistMap}.umap', UnrealObjectType.level),
                                            SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.tvCamsMap}.umap', UnrealObjectType.level)
                                        ]),
                                        SequenceGeneratorFolder(f'{shotTypeCodeLower}-{sequenceMasterLetterUpper}', [
                                            SequenceGeneratorFile(f'{subSequenceCodeUpper}_{shotTypeCodeUpper}-{sequenceMasterLetterUpper}.uasset', UnrealObjectType.masterSequence),
                                            SequenceGeneratorFolder(Unreal.Folder.cameras),
                                            SequenceGeneratorFolder(Unreal.Folder.animation),
                                            SequenceGeneratorFolder(Unreal.Folder.subLevels, [
                                                SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}-{sequenceMasterLetterUpper}{cls.AssetNames.camsMap}.umap', UnrealObjectType.level)
                                            ]),
                                            SequenceGeneratorFolder(Unreal.Folder.subSequences, [
                                                SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}-{sequenceMasterLetterUpper}{cls.AssetNames.animSequence}.uasset', UnrealObjectType.levelSequenceAnim),
                                                SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}-{sequenceMasterLetterUpper}{cls.AssetNames.camsSequence}.uasset', UnrealObjectType.levelSequenceCams)
                                            ])
                                        ])
                                    ])
                                ])
                            ])
                        ])
                    ])

            cls._buffer = [_SequenceGeneratorObjectBase(_hierarchy.path, _hierarchy.type)]
            for child in _hierarchy.children:
                cls._getStructureRecursiveHelper(child, _hierarchy.path)

            return cls._buffer

        @classmethod
        def getStructureAlt(cls, projectName: str, master: SequenceMaster) -> list[_SequenceGeneratorObjectBase]:
            '''Generate a default PROXi sequence structure based on the given `ProjectName` and `SequenceMaster`'''

            if not projectName or not master:
                unreal.log_error('SequenceFolderStructure.getStructure(): Either project name or sequence master is missing')
                unreal.log_error(f'Project name: {projectName}')
                unreal.log_error(f'Master: {master}')
                return []

            projectNameUpper = projectName.upper() # NECTAR
            sequenceCodeUpper = master.sequence['code'].upper() # BFA
            sequenceCodeLower = master.sequence['code'].lower() # bfa
            sequenceNameCamel = strings.camelCase(master.sequence["name"]) # bulletFarmAmbush
            subSequenceCodeUpper = master.subSequence['code'].upper() # BFA01
            subSequenceCodeLower = master.subSequence['code'].lower() # bfa01
            shotTypeCodeUpper = master.type.upper() # TX
            shotTypeCodeLower = master.type.lower() # tx
            shotTypeNameCamel = strings.camelCase(Unreal.SequenceTypeMapping.getShotgunValue(shotTypeCodeLower)) # toyBox
            sequenceMasterLetterUpper = master.masterLetter.upper()

            _hierarchy = SequenceGeneratorRootFolder(f'/Game/{projectNameUpper}', [
                        SequenceGeneratorFolder(Unreal.Folder.sequences, [
                            SequenceGeneratorFolder(f'{sequenceCodeUpper}_{sequenceNameCamel}', [
                                SequenceGeneratorFile(f'{sequenceCodeUpper}.uasset', UnrealObjectType.levelSequence),
                                SequenceGeneratorFile(f'{sequenceCodeUpper}{cls.AssetNames.masterMap}.umap', UnrealObjectType.world),
                                SequenceGeneratorFolder(Unreal.Folder.shared, [
                                    SequenceGeneratorFolder(Unreal.Folder.subLevels, [
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.actorsMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.actorsBlockoutMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.envBlockoutMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.envBuildingsMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.envLandscapeMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.fxEnvMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.lxEnvMap}.umap', UnrealObjectType.level),
                                        SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.ppSharedMap}.umap', UnrealObjectType.level)
                                    ])
                                ]),
                                SequenceGeneratorFolder(f'{shotTypeCodeUpper}_{shotTypeNameCamel}', [
                                    SequenceGeneratorFolder(f'{subSequenceCodeUpper}_{shotTypeCodeUpper}', [
                                        SequenceGeneratorFolder(Unreal.Folder.shared, [
                                            SequenceGeneratorFile(f'{sequenceCodeLower}_{shotTypeCodeLower}{cls.AssetNames.fxCharMap}.umap', UnrealObjectType.level),
                                            SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}{cls.AssetNames.fxEnvMap}.umap', UnrealObjectType.level),
                                            SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}{cls.AssetNames.lxCineMap}.umap', UnrealObjectType.level),
                                            SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.tvDistMap}.umap', UnrealObjectType.level),
                                            SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.tvCamsMap}.umap', UnrealObjectType.level)
                                        ]),
                                        SequenceGeneratorFolder(f'{shotTypeCodeLower}-{sequenceMasterLetterUpper}', [
                                            SequenceGeneratorFile(f'{subSequenceCodeUpper}_{shotTypeCodeUpper}-{sequenceMasterLetterUpper}.uasset', UnrealObjectType.masterSequence),
                                            SequenceGeneratorFolder(Unreal.Folder.cameras),
                                            SequenceGeneratorFolder(Unreal.Folder.animation),
                                            SequenceGeneratorFolder(Unreal.Folder.subLevels, [
                                                SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}-{sequenceMasterLetterUpper}{cls.AssetNames.camsMap}.umap', UnrealObjectType.level)
                                            ]),
                                            SequenceGeneratorFolder(Unreal.Folder.subSequences, [
                                                SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}-{sequenceMasterLetterUpper}{cls.AssetNames.camsSequence}.uasset', UnrealObjectType.levelSequenceCams)
                                            ])
                                        ])
                                    ])
                                ])
                            ])
                        ])
                    ])

            cls._buffer = [_SequenceGeneratorObjectBase(_hierarchy.path, _hierarchy.type)]
            for child in _hierarchy.children:
                cls._getStructureRecursiveHelper(child, _hierarchy.path)

            return cls._buffer
            
        @classmethod
        def getStructureLegacy(cls, projectName: str, master: SequenceMaster) -> list[_SequenceGeneratorObjectBase]:
            '''Generate a default PROXi sequence structure based on the given `ProjectName` and `SequenceMaster`'''

            
            if not projectName or not master:
                unreal.log_error('SequenceFolderStructure.getStructure(): Either project name or sequence master is missing')
                unreal.log_error(f'Project name: {projectName}')
                unreal.log_error(f'Master: {master}')
                return []

            projectNameUpper = projectName.upper() # NECTAR
            sequenceCodeUpper:str|None = master.sequence['code'].upper() # BFA
            sequenceCodeLower = master.sequence['code'].lower() # bfa
            sequenceNameCamel = strings.camelCase(master.sequence["name"]) # bulletFarmAmbush
            subSequenceCodeUpper = master.subSequence['code'].upper() # BFA01
            subSequenceCodeLower = master.subSequence['code'].lower() # bfa01
            shotTypeCodeUpper = master.type.upper() # TX
            shotTypeCodeLower = master.type.lower() # tx
            shotTypeNameCamel = strings.camelCase(Unreal.SequenceTypeMapping.getShotgunValue(shotTypeCodeLower)) # toyBox
            sequenceMasterLetterUpper = master.masterLetter.upper()

            _hierarchy = SequenceGeneratorRootFolder(f'/Game/{projectNameUpper}', [
                        SequenceGeneratorFolder(Unreal.Folder.sequences, [
                            SequenceGeneratorFolder(f'{sequenceCodeUpper}_{sequenceNameCamel}', [
                                SequenceGeneratorFile(f'{sequenceCodeUpper}.uasset', UnrealObjectType.levelSequence),
                                SequenceGeneratorFile(f'{sequenceCodeUpper}{cls.AssetNames.masterMap}.umap', UnrealObjectType.world),
                                SequenceGeneratorFolder(Unreal.Folder.shared, [
                                    SequenceGeneratorFolder(Unreal.Folder.subLevels, [
                                        # SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.actorsMap}.umap', UnrealObjectType.level),
                                        # SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.actorsBlockoutMap}.umap', UnrealObjectType.level),
                                        # SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.envBlockoutMap}.umap', UnrealObjectType.level),
                                        # SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.envBuildingsMap}.umap', UnrealObjectType.level),
                                        # SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.envLandscapeMap}.umap', UnrealObjectType.level),
                                        # SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.fxEnvMap}.umap', UnrealObjectType.level),
                                        # SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.lxEnvMap}.umap', UnrealObjectType.level),
                                        # SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.ppSharedMap}.umap', UnrealObjectType.level)
                                    ])
                                ]),
                                SequenceGeneratorFolder(f'{shotTypeCodeUpper}_{shotTypeNameCamel}', [
                                    SequenceGeneratorFolder(f'{subSequenceCodeUpper}_{shotTypeCodeUpper}', [
                                        SequenceGeneratorFolder(Unreal.Folder.shared, [
                                            # SequenceGeneratorFile(f'{sequenceCodeLower}_{shotTypeCodeLower}{cls.AssetNames.fxCharMap}.umap', UnrealObjectType.level),
                                            # SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}{cls.AssetNames.fxEnvMap}.umap', UnrealObjectType.level),
                                            # SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}{cls.AssetNames.lxCineMap}.umap', UnrealObjectType.level),
                                            # SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.tvDistMap}.umap', UnrealObjectType.level),
                                            # SequenceGeneratorFile(f'{sequenceCodeLower}{cls.AssetNames.tvCamsMap}.umap', UnrealObjectType.level)
                                        ]),
                                        SequenceGeneratorFolder(f'{shotTypeCodeLower}-{sequenceMasterLetterUpper}', [
                                            SequenceGeneratorFile(f'{subSequenceCodeUpper}_{shotTypeCodeUpper}-{sequenceMasterLetterUpper}.uasset', UnrealObjectType.masterSequence),
                                            SequenceGeneratorFolder(Unreal.Folder.cameras),
                                            SequenceGeneratorFolder(Unreal.Folder.animation),
                                            SequenceGeneratorFolder(Unreal.Folder.subLevels, [
                                                SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}-{sequenceMasterLetterUpper}{cls.AssetNames.camsMap}.umap', UnrealObjectType.level)
                                            ]),
                                            SequenceGeneratorFolder(Unreal.Folder.subSequences, [
                                                SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}-{sequenceMasterLetterUpper}{cls.AssetNames.camsSequence}.uasset', UnrealObjectType.levelSequenceCams),
                                                SequenceGeneratorFile(f'{subSequenceCodeLower}_{shotTypeCodeLower}-{sequenceMasterLetterUpper}{cls.AssetNames.camsSequence}.uasset', UnrealObjectType.levelSequenceCams)

                                            ])
                                        ])
                                    ])
                                ])
                            ])
                        ])
                    ])

            cls._buffer = [_SequenceGeneratorObjectBase(_hierarchy.path, _hierarchy.type)]
            for child in _hierarchy.children:
                cls._getStructureRecursiveHelper(child, _hierarchy.path)

            return cls._buffer

        @classmethod
        def _getStructureRecursiveHelper(cls, obj: _SequenceGeneratorObjectBase, basePath: str):
            '''Self-recursing function helper for `cls.getStructure()'''
            
            obj.path = f'{basePath}/{obj.path}'
            cls._buffer.append(obj)

            # Empty folders need a placeholder asset
            if not obj.children and isinstance(obj, SequenceGeneratorFolder):
                obj.children.append(SequenceGeneratorFile(f'{Unreal.placeholderAssetName}.uasset', UnrealObjectType.material, isPlaceholder=True))

            # Recurse
            for child in obj.children:
                cls._getStructureRecursiveHelper(child, obj.path)