#!/bin/bash 

# Setup the environment for the framework
export URN=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P)
echo "Setting variable \$URN=$URN"
export URN_BASE=$(dirname $URN)

echo "Setting up CMSSW runtime environment"
eval `scramv1 runtime -sh`

#source site-dependent configuration
source $URN/Configuration/site/site_configuration.sh
alias crab3='/cvmfs/cms.cern.ch/crab3/crab-env-bootstrap.sh'
export CRAB3_LOCATION=/cvmfs/cms.cern.ch/crab3/crab.sh
export CRAB2_LOCATION=/cvmfs/cms.cern.ch/crab/crab.sh

# Don't require a scram build to get updated scripts
export PATH=$URN/Utilities/scripts:$PATH

#re-run cmsenv, crab tends to screw up many things
eval `scramv1 runtime -sh`
