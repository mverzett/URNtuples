#!/bin/env bash
set -o nounset
set -o errexit

vers='CMSSW_8_0_19' 
if [ "$CMSSW_VERSION" -eq "$vers" ]; then
		echo "URNtuple installation is CMSSW-version dependent!"
		echo "This recipe was made for $vers, either update the recipe (and push to a new branch), use the appropriate branch for the release, or use $vers!"
		exit 42
fi

pushd $CMSSW_BASE/src
echo "Applying patch to smeared jets to avoid pt sorting, necessary for the NTuples"
git cms-addpkg PhysicsTools/PatUtils
git apply --check URNtuples/SmearedJetProducerT.patch
git am --signoff < URNtuples/SmearedJetProducerT.patch
echo "installing other stuff"
git cms-merge-topic cms-met:metTool80X
git cms-merge-topic -u cms-met:CMSSW_8_0_X-METFilterUpdate
popd
