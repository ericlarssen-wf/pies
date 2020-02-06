  
#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

${DIR?}/cleanup.sh

kubectl create -f ${DIR?}/service-account.yaml -n workiva
kubectl create -f ${DIR?}/job.yaml -n workiva