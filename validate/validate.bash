#!/bin/bash
#
# validate/validate.bash
#
# Validate input xml file.
#
# Input: Input xml file, .dtd file in validate/, and .xsd file in validate/.
#
# Output: If errors are present then they are output.  If no errors are present
#         then a success message is output.
#
# Used in: validate/validateConfig3.bash


# Initialize ${inputXml}.
if [ -z ${1} ]                  # first command-line parameter is null
then
  builtin read -e -p 'Input: '  # if no vars specified places input in ${REPLY}
  builtin declare -r inputXml="${REPLY}"
else
  builtin declare -r inputXml="${1}"
fi


# Initialize ${inputDtd} and ${inputXsd}.
if [ -z ${2} ]                          # second command-line parameter is null
then
  builtin declare -r inputXmlFileName="${inputXml##*/}"      # delete longest
                                                             #  beginning match
  builtin declare -r inputDtdFileName="${inputXmlFileName/%.xml/.dtd}"
  builtin declare -r inputXsdFileName="${inputXmlFileName/%.xml/.xsd}"
else
  builtin declare -r inputDtdFileName="${2}.dtd"
  builtin declare -r inputXsdFileName="${2}.xsd"
fi

builtin declare -r selfDir="${0%/*}"                # delete shortest end match
builtin declare -r inputDtd="${selfDir}/${inputDtdFileName}"
builtin declare -r inputXsd="${selfDir}/${inputXsdFileName}"


# Validate input xml file.
builtin declare -r \
  xmllint="command /usr/bin/xmllint --noblanks --noent --noout"

if [ -f ${inputDtd} ]
then
  ${xmllint} --dtdvalid "${inputDtd}" "${inputXml}"
else
  builtin echo "${inputDtd} is not present." 1> "/dev/stderr"
fi

if [ -f ${inputXsd} ]
then
  ${xmllint} --schema "${inputXsd}" "${inputXml}"
else
  builtin echo "${inputXsd} is not present." 1> "/dev/stderr"
fi
