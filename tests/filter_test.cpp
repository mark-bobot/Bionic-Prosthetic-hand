#include <cassert>
#include <cmath>
#include <iostream>
#include "../firmware/ProstheticHand/EMGFilters.h"
#include "../firmware/ProstheticHand/HandControl.h"
int main(){
 EMGFilters f; f.init(SAMPLE_FREQ_1000HZ,NOTCH_FREQ_50HZ,true,true,true);
 HandControl h;
 for(int i=0;i<5200;++i) h.sample(f.update(307),307,true);
 assert(h.calibrated&&!h.closed&&!h.fault);
 for(int i=0;i<50;++i)h.sample(f.update(307),307,false); // Qualified switch release.
 for(int i=0;i<100;++i) h.sample(f.update(307),307,true);
 for(int i=0;i<500;++i){int raw=307+int(50*sin(2*3.141592653589793*80*i/1000));h.sample(f.update(raw),raw,true);}
 assert(h.closed&&!h.fault);
 for(int i=0;i<500;++i)h.sample(f.update(307),307,true);
 assert(!h.closed&&!h.fault);
 std::cout<<"PASS: actual OYMotion filter + controller, synthetic rest/contraction/rest\n";
}
