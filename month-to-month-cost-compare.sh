#!/bin/bash

# Filenames
FILE1="costs_prev_month.txt"
FILE2="costs_month_before_prev.txt"
OUTPUT="cost_comparison.txt"

# Clear the output file
> $OUTPUT

# Helper function to determine the sign
get_sign() {
    local num=$1
    if (( $(echo "$num < 0" | bc -l) )); then
        echo "-"
    else
        echo "+"
    fi
}

# Compare services between the two files
while read -r line1; do
    service1=$(echo "$line1" | cut -d'$' -f1 | sed 's/ *$//g')
    cost1=$(printf "%.2f" $(echo "$line1" | cut -d'$' -f2))

    while read -r line2; do
        service2=$(echo "$line2" | cut -d'$' -f1 | sed 's/ *$//g')
        cost2=$(echo "$line2" | cut -d'$' -f2)

        if [[ "$service1" == "$service2" ]]; then
            difference=$(printf "%.2f" $(echo "$cost1 - $cost2" | bc))

            if (( $(echo "$cost2 == 0" | bc -l) )); then
                percent_change="100.00"
            else
                percent_change=$(echo "scale=2; ($difference / $cost2) * 100" | bc)
            fi

            # Get the sign for the difference and percentage change
            sign_dif=$(get_sign "$difference")
            sign_pc=$(get_sign "$percent_change")

            # Remove negative sign if present, for display purposes
            difference=$(echo $difference | tr -d '-')
            percent_change=$(echo $percent_change | tr -d '-')

            printf "%s $%.2f (%s$%.2f, %s%.2f%%)\n" "$service1" "$cost1" "$sign_dif" "$difference" "$sign_pc" "$percent_change" >> $OUTPUT
            break
        fi

    done < "$FILE2"

done < "$FILE1"

echo "Comparison saved to $OUTPUT"
