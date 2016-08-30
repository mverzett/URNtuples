#ifndef typeConversion_H
#define typeConversion_H

#include "TMath.h"

namespace ura{
  template<typename T> inline T as(double x){ return static_cast<T>(x);} //for long ints should be reinterpret cast both sides (parser too) 
  template<>           inline double as<Double_t>(double x) { return x; } //do nothing
  template<>           inline float as<Float_t>(double x) { return x; } //do nothing
  template<>           inline int as<Int_t>(double x) { return TMath::Nint(x); } //avoid rounding errors
}

#endif
