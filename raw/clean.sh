#!/bin/bash

for i in ./*.csv
do
# remove double double quotes
#    sed -i 's/\"\"/\"/g' $i

# generate the pricePerLocation summary
    ../addLocationCsv.r $i 

# Remove the new line inside the ""
#    gawk -i inplace -v RS='"' 'NR % 2 == 0 { gsub(/\n/, "") } { printf("%s%s", $0, RT) }' $i

# Remove " within "."
#    gawk -i inplace 'BEGIN { FPAT="([^,]+)|(\"[^\"]+\")"; OFS=","; N="\"" } { for (i=1;i<=NF;i++) if ($i ~ /^\".*\"$/) { gsub(/\"/,"", $i); $i=N $i N } }1' $i

# Check for " not followed by a ','
#    echo $i
#    echo -n ": "
#    grep -E '([^\ ])\"([^,])' $i | wc -l

# replace double double quotes with new line
#    sed -i 's/\"\"/\"\n\"/g' $i


done

