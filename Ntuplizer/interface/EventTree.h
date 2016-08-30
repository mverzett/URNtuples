/*
Singleton class that provides the instance of the TTree where to write the events.
Singleton skeleton taken from http://stackoverflow.com/questions/1008019/c-singleton-design-pattern 

Author: Mauro Verzetti (UR)
 */
#ifndef EventTree_h
#define EventTree_h


#include "TTree.h"
#include "TFile.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include <string>
#include <set>
#include <iostream>

class EventTree{
 public:
  static EventTree& getTree(){
    static EventTree instance;
    return instance; //instance.tree();
  }
  //TTree* tree(){return tree_;}

  //Templated version of Branch, mapping to the appropriate
  //one of ROOT::TTree, but with duplicate branch check
  template<typename ... Args>
  TBranch* branch(std::string name, Args ... args){
    //duplicate branch check
    if(branch_names_.find(name) != branch_names_.end()){
      throw edm::Exception(edm::errors::Configuration) 
	<< "branch name: " << name << " has been already defined!";
    }
    branch_names_.insert(name);
    return tree_->Branch(name.c_str(), args ...);
  }

  void fill(){tree_->Fill();}

  ~EventTree(){}
  //actually not needed, the TFileService takes care of
  //everything

 private:
  EventTree()
  {
    edm::Service<TFileService> fs;
    fs->file().cd();
    tree_ = new TTree("Events", "test");
    tree_->SetAutoSave(3000000000);
  }

  EventTree(EventTree const&);             
  void operator=(EventTree const&);

  TTree *tree_;
  std::set<std::string> branch_names_;
};

#endif
