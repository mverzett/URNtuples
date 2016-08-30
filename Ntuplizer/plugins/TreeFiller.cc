/*
class: TreeFiller

This EDAnalyzer does nothing but filling the tree, marking the end of the event.
It should therefore be always used only once per cfg and in the EndPath, to 
ensure that the Ntuple filling has been completed. 

Author: Mauro Verzetti (UR)
*/

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "URNtuples/Ntuplizer/interface/Obj2BranchBase.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "TTree.h"

class TreeFiller: public Obj2BranchBase{
public:
  TreeFiller(edm::ParameterSet cfg): Obj2BranchBase(cfg){}
  ~TreeFiller(){}

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&){tree_.fill();}
};

//define CMSSW plug-ins
DEFINE_FWK_MODULE(TreeFiller);



