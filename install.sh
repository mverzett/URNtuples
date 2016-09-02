#!/bin/env bash

vers='CMSSW_8_0_19' 
if [ "$CMSSW_VERSION" -eq "$vers" ]
		echo "URNtuple installation is CMSSW-version dependent!"
		echo "This recipe was made for $vers, either update the recipe (and push to a new branch), use the appropriate branch for the release, or use $vers!"
		exit 42
fi

pushd $CMSSW_BASE/src
git cms-merge-topic cms-met:metTool80X
git cms-merge-topic -u cms-met:CMSSW_8_0_X-METFilterUpdate
popd
