#include <cassert>
#include <iostream>
#include "../firmware/ProstheticHand/HandControl.h"
void feed(HandControl& h, int n, int v, bool armed=true, int raw=307) {
  for(int i=0;i<n;++i)h.sample(v,raw,armed);
}
int main(){
 HandControl h;
 feed(h,4999,0); assert(!h.calibrated && !h.closed);
 feed(h,1,0); assert(h.calibrated && h.threshold==100);
 feed(h,100,0); feed(h,40,30); assert(!h.closed);
 feed(h,100,30); assert(h.closed);
 feed(h,100,0); assert(!h.closed);
 feed(h,200,30); assert(h.closed);
 feed(h,1,30,false); assert(!h.closed);
 feed(h,200,30); assert(!h.closed); // Must relax after arming.
 feed(h,100,0); feed(h,200,30); assert(h.closed);
 feed(h,3200,30); assert(!h.closed);
 feed(h,200,30); assert(!h.closed); // Timeout cannot retrigger until relaxed.
 feed(h,100,0); feed(h,200,30); assert(h.closed);
 feed(h,50,0,true,0); assert(h.fault && !h.closed);
 HandControl high; feed(high,5000,2047); assert(high.level==4190209UL);
 HandControl noisy; feed(noisy,5000,10); assert(noisy.threshold==325);
 std::cout << "PASS: calibration, debounce, release, arming, timeout, fault, arithmetic\n";
}
