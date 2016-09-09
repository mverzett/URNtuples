// -*- C++ -*-
//
// Package:    URNtuples/ObjectFilter
// Class:      ObjectFilter
// 
/**\class ObjectFilter ObjectFilter.cc URNtuples/ObjectFilter/plugins/ObjectFilter.cc

 Description: String cut filter on a single object (like LHE results or trigger)

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  mauro verzetti
//         Created:  Fri, 09 Sep 2016 09:23:18 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "CommonTools/UtilAlgos/interface/StringCutObjectSelector.h"
//
// class declaration
//

template<typename OBJ>
class ObjectFilter : public edm::stream::EDFilter<> {
public:
	explicit ObjectFilter(const edm::ParameterSet&);
	~ObjectFilter();

	static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
	virtual void beginStream(edm::StreamID) override;
	virtual bool filter(edm::Event&, const edm::EventSetup&) override;
	virtual void endStream() override;

	//virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
	//virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
	//virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
	//virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

	// ----------member data ---------------------------
	edm::EDGetTokenT< OBJ > src_;
	StringCutObjectSelector<OBJ, true> cut_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
template<typename OBJ>
ObjectFilter<OBJ>::ObjectFilter(const edm::ParameterSet& cfg):
	src_(consumes< OBJ >(cfg.getParameter<edm::InputTag>("src"))),
	cut_(cfg.getParameter<std::string>("cut"))
{
   //now do what ever initialization is needed

}


template<typename OBJ>
ObjectFilter<OBJ>::~ObjectFilter()
{
 
   // do anything here that needs to be done at destruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
template<typename OBJ>
bool
ObjectFilter<OBJ>::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   Handle<OBJ> handle;
   iEvent.getByToken(src_, handle);
	 
   return cut_(*(handle.product()));
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
template<typename OBJ>
void
ObjectFilter<OBJ>::beginStream(edm::StreamID)
{
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
template<typename OBJ>
void
ObjectFilter<OBJ>::endStream() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
ObjectFilter::beginRun(edm::Run const&, edm::EventSetup const&)
{ 
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
ObjectFilter::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
ObjectFilter::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
ObjectFilter::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
template<typename OBJ>
void
ObjectFilter<OBJ>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}



//define this as a plug-in
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
typedef ObjectFilter<LHEEventProduct> LHEEventProductFilter;
DEFINE_FWK_MODULE(LHEEventProductFilter);
