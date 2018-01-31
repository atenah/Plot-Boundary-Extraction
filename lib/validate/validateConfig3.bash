#!/bin/bash
#
# lib/validate/validateConfig3.bash
#
# Validate Config3.xml.
#
# Input: lib/Config3.xml, lib/validate/Config3.dtd, and
#        lib/validate/Config3.xsd.
#
# Output: If errors are present then they are output.  If no errors then a suc-
#         cess message is output.

builtin declare -r selfDir="${0%/*}"                # delete shortest end match
command "${selfDir}/validate.bash" "${selfDir}/../Config3.xml"
