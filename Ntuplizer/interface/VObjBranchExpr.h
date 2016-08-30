#ifndef VObjBranchExpr_H
#define VObjBranchExpr_H

#include "URNtuples/Ntuplizer/interface/ObjExpression.h"
#include "URNtuples/Utilities/interface/typeConversion.h"
#include "URNtuples/Ntuplizer/interface/EventTree.h"
#include "TTree.h"
#include <vector>
#include <iostream>
#include <memory>

/*
class: VObjBranchExpr<EDObject, VType>

This class provides the implementation of a vectorial TTree branch filled with a 
StringObjectFunction. 
The first template argument defines the EDObject on which the functor operates,
while the second template provides the output collection type.

WARNING: As every return value computed by StringObjectFunction () operator is
by default a double, rounding errors for big numbers WILL happen. This makes
this option not suitable for long ints and similar where every bit counts.
The final return value is just a type cast from double, in order to save space.

To evercome this effect the internal implementation of StringObjectFunction's
grammar should be changed, returning instead of the static_cast of the variable
the reinterpret_cast, but this gets beyond the scope of this framework and would 
break backward compatibility and the physical meaning of the number.

Author: Mauro Verzetti (UR)
 */

template <typename EDObject, typename VType>
class VObjBranchExpr: public ObjExpression<EDObject> {
public:
  VObjBranchExpr(std::string branch_name, EventTree& tree, std::string &expr):
    ObjExpression<EDObject>(expr),
    branch_vals_(),
    name_(branch_name)
  {
    //std::cout<<name_ <<": set branch to vals addr: " << &branch_vals_ << std::endl;
    branch_ = tree.branch(branch_name, &branch_vals_);
    //std::cout<<name_ <<": set branch to vals addr: " << &branch_vals_ << std::endl;
  }

  ~VObjBranchExpr(){ /*delete branch_vals_;*/ }
  virtual void fill(const EDObject &obj) {branch_vals_.push_back( ura::as<VType>(this->functor_(obj)));}
  virtual void reserve(size_t i) {branch_vals_.reserve(i);}
  virtual void clear() {branch_vals_.clear();}
  virtual void debug() {std::cout<<name_ <<" vals addr: "<< &branch_vals_<< " branch addr: "<< (std::vector<VType>*) branch_->GetAddress() << std::endl;}

private:
  std::vector<VType> branch_vals_;
  TBranch *branch_;
  std::string name_;
};

/*
function: VObjBranchExprFactory<EDObject>

This factory specializes the second template argument of VObjBranchExpr, 
providing the proper vector type according to the information encoded in
BranchInfo (defined in: URNtuples/Ntuplizer/interface/ObjExpression.h).

Author: Mauro Verzetti (UR)
 */

template <typename EDObject>
ObjExpression<EDObject>* VObjBranchExprFactory(BranchInfo &info, EventTree& tree)
{
  switch(info.type){
  case BranchInfo::typeID::USHORT : return new VObjBranchExpr<EDObject, unsigned short>(info.name, tree, info.expr);
  case BranchInfo::typeID::DOUBLE : return new VObjBranchExpr<EDObject, double>(info.name, tree, info.expr);	       
  case BranchInfo::typeID::SHORT  : return new VObjBranchExpr<EDObject, short >(info.name, tree, info.expr);	       
  case BranchInfo::typeID::INT    : return new VObjBranchExpr<EDObject, int>(info.name, tree, info.expr);	       
  case BranchInfo::typeID::UINT   : return new VObjBranchExpr<EDObject, unsigned int>(info.name, tree, info.expr);  
  case BranchInfo::typeID::FLOAT  : return new VObjBranchExpr<EDObject, float>(info.name, tree, info.expr);	       
  case BranchInfo::typeID::LONG   : return new VObjBranchExpr<EDObject, long>(info.name, tree, info.expr);	       
  case BranchInfo::typeID::BOOL   : return new VObjBranchExpr<EDObject, bool>(info.name, tree, info.expr); 	       
  case BranchInfo::typeID::ULONG  : return new VObjBranchExpr<EDObject, unsigned long>(info.name, tree, info.expr); 
  default: return NULL;
  }
  //return ret;
}

#endif 
