#!/bin/bash
aws securityhub get-findings \
    --filters '{"SeverityLabel":[{"Value": "CRITICAL","Comparison":"EQUALS"}, {"Value": "HIGH","Comparison":"EQUALS"}]}' \
    --query "Findings[].[Title,Severity.Label]" \
    --output json | jq -r 'group_by(.[]) | map({title: .[0][0], severity: .[0][1], count: length}) | sort_by(.severity)' > securityhub_critical_high_findings_grouped2.txt
