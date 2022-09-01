# -*- coding: utf-8 -*-
'''Modify the unreal.py stubs to include type hinting

To export a Python stub file from the Unreal Python plugin, follow these directions:
    https://sondreutheim.com/post/getting_started_with_python_in_ue4#4-autocomplete-in-vs-code
'''

from __future__ import annotations

import os
import re


TARGET_STUBS_FILENAME = 'unreal_orig_5.py'
EXTRA_IMPORTS = ['from __future__ import annotations']
DEFAULT = 'object'
BUILTINS = [
    'bool',
    'int',
    'float',
    'str',
    'None',
    'object',
    'tuple',
    # 'type'
]
CORRECTIONS = {
    'enum': 'Enum', # Unreal type
    'Bool': 'bool',
    'pair': 'tuple',
    'int32': 'int',
    'int64': 'int',
    'uint8': 'int',
    'integer': 'int',
    'string': 'str',
    'struct': DEFAULT,
    'type': DEFAULT
}
ITERABLES = {
    'Array': 'list',
    'FixedArray': 'list',
    'Map': 'dict',
    'Set': 'set'
}


class Patterns:
    className = re.compile(r'(\s*)?class (\w+)(?:\((.*?)\))?:?(\s*)?')
    returnTypeHint = re.compile(r'\s*?.\.([a-zA-Z0-9_]+)\(.*\) -> ([a-zA-Z0-9_]+)(?:\((.*?)\))?:?(\s*)?\s*?')
    returnActual = re.compile(r'\s+?(pass|return None)\s*?')


def main(verbose: bool = False):

    thisDir = os.path.dirname(__file__)
    pythonBaseDir = os.path.dirname(thisDir)
    autocompleteDir = os.path.join(pythonBaseDir, '.autocomplete')
    unrealStubsFile = os.path.join(autocompleteDir, TARGET_STUBS_FILENAME)
    processedFile = os.path.join(autocompleteDir, 'unreal.py')

    unrealTypes: list[str] = []
    hintedTypes: list[str] = []
    buffer: list[str] = []
    # lastTypeHint: str = ''

    print(f'Parsing file {unrealStubsFile}...')
    with open(unrealStubsFile, 'r') as f:
        for line in f.readlines():
            if 'import ' in line:
                line = line.encode("ascii", "ignore").decode()

            buffer.append(line)

            # This is a class declaration
            classMatch = Patterns.className.match(line)
            if classMatch:
                # lastTypeHint = ''
                className = classMatch.group(2)
                if not className.startswith('_'):
                    unrealTypes.append(className)

                # Class inheritance needs some nudging
                if className in ITERABLES:
                    indent = classMatch.group(1)
                    whitespace = classMatch.group(4) or ''
                    inheritance = classMatch.group(3)
                    correction = [ITERABLES[className]]
                    if inheritance:
                        correction.insert(0, inheritance)

                    buffer[-1] = f'{indent}class {className}({", ".join(correction)}):{whitespace}'
                continue

            # This is a type-signature for a method
            typeMatch = Patterns.returnTypeHint.match(line)
            if typeMatch:
                typeName = typeMatch.group(2)
                typeName = CORRECTIONS.get(typeName, typeName)
                # lastTypeHint = typeName if not typeName.startswith('_') else ''
                hintedTypes.append(typeName)
                continue

            # This is a return statement
            # if lastTypeHint and lastTypeHint != 'None':
            #     returnMatch = Patterns.returnActual.match(line)
            #     if returnMatch:
            #         oldStatement = returnMatch.group(1)
            #         newStatement = f'return {lastTypeHint}()'
            #         buffer[-1] = line.replace(oldStatement, newStatement)

    print('Done!')

    unrealTypesSet = set(unrealTypes)
    hintedTypesSet = set(hintedTypes)
    unaccountedForSet = hintedTypesSet-unrealTypesSet
    diffUnrealTypes = len(unrealTypes)-len(unrealTypesSet)
    diffHintedTypes = len(hintedTypes)-len(hintedTypesSet)

    print(f'\nFound {len(unrealTypesSet)} Unreal types ({diffUnrealTypes} filtered out)')
    if verbose:
        for typ in sorted(unrealTypesSet, key=lambda x: x.lower()):
            print(f'    {typ}')

        print('')

    print(f'Found {len(hintedTypesSet)} hinted types ({diffHintedTypes} filtered out)')
    if verbose:
        for typ in sorted(hintedTypesSet, key=lambda x: x.lower()):
            print(f'    {typ}')

        print('')

    print(f'{len(unaccountedForSet)} types unaccounted for')
    if verbose:
        for typ in sorted(unaccountedForSet, key=lambda x: x.lower()):
            print(f'    {typ}')

    print('\nProcessing method signatures...')
    replacements = 0
    returnTypeObjectBuffer = ''
    for i, line in enumerate(buffer):

        # This is a class declaration
        classMatch = Patterns.className.match(line)
        if classMatch:
            returnTypeObjectBuffer = ''
            continue

        # This is a type-signature for a method
        typeMatch = Patterns.returnTypeHint.match(line)
        if typeMatch:
            targetLineNum = i-2
            methodName = typeMatch.group(1)
            returnTypeRaw = typeMatch.group(2)
            returnTypeRaw = CORRECTIONS.get(returnTypeRaw, returnTypeRaw)
            returnTypeSub = typeMatch.group(3)

            if returnTypeRaw != DEFAULT and (returnTypeRaw in BUILTINS or returnTypeRaw in unrealTypesSet):
                returnTypeActual = returnTypeRaw
                returnTypeObjectBuffer = returnTypeRaw
                if returnTypeSub:

                    ## It's actually better to keep this 'incorrect', which produces an incomplete type hint, which in turn is less annoying for
                    ## Unreal methods that return sub-types specific to the input Array[MovieSceneScriptingChannel] vs. Array[MovieSceneScriptingFloatChannel], etc
                    # returnTypeActual = ITERABLES.get(returnTypeActual, returnTypeActual) # Translates Array->list, etc

                    returnTypesSub: list[str] = []
                    for typ in returnTypeSub.split(','):
                        typ = typ.strip()
                        typ = CORRECTIONS.get(typ, typ)
                        if typ in BUILTINS or typ in unrealTypesSet:
                            returnTypesSub.append(typ)
                        else:
                            returnTypesSub.append(DEFAULT)

                    returnTypeActual = f'{returnTypeActual}[{", ".join(returnTypesSub)}]'
            else:
                returnTypeActual = DEFAULT
                returnTypeObjectBuffer = DEFAULT

            if targetLineNum < 0:
                print(f'ERROR: Line {i} -> Target line {targetLineNum} is invalid')
                continue

            targetLine = buffer[targetLineNum]
            if not methodName in targetLine:
                print(f'ERROR: Line {i} -> Target line {targetLineNum} does not contain expected method name {methodName}')
                continue
            elif not targetLine.strip().endswith(':'):
                print(f'ERROR: Line {i} -> Target line {targetLineNum} does not end with a colon, perhaps it\'s already type hinted?')
                continue

            buffer[targetLineNum] = targetLine.replace(':', f' -> {returnTypeActual}:')
            replacements += 1

            continue

        # Return statement
        returnMatch = Patterns.returnActual.match(line)
        if returnMatch:
            if returnTypeObjectBuffer and returnTypeObjectBuffer not in ['None', 'type']:
                oldStatement = returnMatch.group(1)
                newStatement = f'return {returnTypeObjectBuffer}()'
                buffer[i] = line.replace(oldStatement, newStatement)
                replacements += 1

            returnTypeObjectBuffer = ''

    print('Done!')

    if not replacements:
        print('No replacements were made! This is bad news...')
        return

    print(f'Inserted {replacements} type hints')
    print(f'Writing content to {processedFile}...')
    with open(processedFile, 'w') as f:
        for imp in EXTRA_IMPORTS:
            f.write(f'{imp}\n')

        for line in buffer:
            f.write(line)

    print('Done!')




if __name__ == '__main__':
    main()