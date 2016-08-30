#ifndef ObjExpression_H
#define ObjExpression_H
#define SEPARATOR "."

/*
class: ObjExpression<EDObject>
Simple abstract class wrapping around the StringObjectFunction<> class. 
Provides some additional virtual methods for derived classes to use.

Public inheritance might have been an option, but with weird tamplated
classes like StringObjectFunction it's always a risk.

Author: Mauro Verzetti (UR)
 */

#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

template <typename EDObject>
class ObjExpression{
public:
  ObjExpression(std::string &expr):
    functor_(expr, true) {} //lazy parsing
  virtual ~ObjExpression() {}
  virtual void fill(const EDObject &obj) =0;
  virtual void reserve(size_t i) {}
  virtual void clear() {}
  virtual void debug() {}

protected:
  StringObjectFunction<EDObject> functor_;
};

#include "FWCore/Utilities/interface/InputTag.h"

/*
class: BranchInfo

Struct that provides unified method to extract the relevant information 
from an edm::PSet and make it usable for ObjExpression derived classes.

Implemented here to avoid excessive proliferation of header files, also
because the struct was designed and intended to specifically work with
ObjExpression daughters.

Author: Mauro Verzetti
*/ 

struct BranchInfo{
  enum typeID {
    DOUBLE,
    SHORT, 
    USHORT,
    INT, 
    UINT,
    FLOAT, 
    LONG, 
    ULONG,
    BOOL    };
  BranchInfo(std::string& prefix, const edm::ParameterSet &tag):
    name(prefix+SEPARATOR+tag.getParameter<std::string>("name")),
    expr(tag.getParameter<std::string>("expr")),
    str_type(tag.getParameter<std::string>("type"))
  {
    if(expr.empty()) expr = tag.getParameter<std::string>("name");
    if(str_type.empty()) str_type = "/F";
    if(str_type == "/D") type = DOUBLE;
    else if(str_type == "/S") type = SHORT ;
    else if(str_type == "/s") type = USHORT;
    else if(str_type == "/I") type = INT   ;
    else if(str_type == "/i") type = UINT  ;
    else if(str_type == "/F") type = FLOAT ;
    else if(str_type == "/L") type = LONG  ;
    else if(str_type == "/l") type = ULONG ;
    else if(str_type == "/O") type = BOOL  ;
    else type = FLOAT;
  }
  std::string name, expr, str_type;
  typeID type;
};

#endif
