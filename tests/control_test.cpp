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
 feed(h,200,0); feed(h,200,30); assert(!h.enabled && !h.closed);
 feed(h,49,0,false); feed(h,100,0); assert(!h.enabled); // Short release is insufficient.
 feed(h,50,0,false); assert(!h.enabled); // Release after calibration, then hold.
 feed(h,100,0); feed(h,40,30); assert(!h.closed);
 feed(h,100,30); assert(h.closed);
 feed(h,100,0); assert(!h.closed);
 feed(h,200,30); assert(h.closed);
 feed(h,1,30,false); assert(!h.closed && !h.enabled);
 feed(h,200,30); assert(!h.closed); // Must relax after arming.
 feed(h,50,30,false);
 feed(h,100,0); feed(h,200,30); assert(h.closed);
 feed(h,3200,30); assert(!h.closed);
 feed(h,200,30); assert(!h.closed); // Timeout cannot retrigger until relaxed.
 feed(h,100,0); feed(h,200,30); assert(h.closed);
 feed(h,50,0,true,0); assert(h.fault && !h.closed && !h.enabled);
 feed(h,70000,0,false,0); feed(h,200,0); assert(h.fault && !h.enabled);
 HandControl reboot;
 feed(reboot,5200,0); feed(reboot,200,30); assert(!reboot.enabled && !reboot.closed);
 HandControl held;
 feed(held,1000,0,false); feed(held,4200,0); feed(held,200,30);
 assert(!held.enabled && !held.closed); // Release during calibration is insufficient.
 HandControl rail;
 feed(rail,49,0,true,700); assert(!rail.fault);
 feed(rail,1,0,true,307); feed(rail,49,0,true,700); assert(!rail.fault);
 feed(rail,1,0,true,700); assert(rail.fault && !rail.enabled);
 HandControl high; feed(high,5000,2047); assert(high.level==4190209UL);
 HandControl noisy; feed(noisy,5000,10); assert(noisy.threshold==325);
 std::cout << "PASS: calibration, startup/restart inhibit, rearming, debounce, release, timeout, latched fault, arithmetic\n";
}
