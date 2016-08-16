#!/bin/bash

set -x

PROCESS_MANAGER_AGENT_URL="http://127.0.0.1:8020"

function extract_id {

    RESULT=$(echo $1 | sed 's/.*"id"://g' | sed 's/,.*//g')

    echo "$RESULT"
}

########################################################
# CREATION OF OP
########################################################

read -r -d '' OP_JSON_VALUE <<- EOM
{
    "user": "admin",
    "script": "bash -c 'sleep 10'",
    "callback_url": "http://google.fr"
}
EOM

echo $OP_JSON_VALUE

OP_REGISTRATION_OUTPUT=$(curl -u admin:pass -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d "$OP_JSON_VALUE" "$PROCESS_MANAGER_AGENT_URL/ops/")
echo $OP_REGISTRATION_OUTPUT
OP_ID=$(extract_id $OP_REGISTRATION_OUTPUT)

# Run the OP
read -r -d '' OP_ID_JSON_VALUE <<- EOM
{
    "op_id": "$OP_ID"
}
EOM

echo $OP_ID_JSON_VALUE
RUNNING_OP_OUTPUT=$(curl -u admin:pass -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d "$OP_ID_JSON_VALUE" "$PROCESS_MANAGER_AGENT_URL/ops/$OP_ID/run_op/")

exit 0
