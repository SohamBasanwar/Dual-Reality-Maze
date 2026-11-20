/* DUAL-REALITY MAZE — nominal CAD study, millimeters.
 * NOT RELEASED FOR PRINT. The breadboard, control modules, connectors,
 * LCD window, horn and latch fits must be physically measured.
 * Role: "explorer", "architect", "main".
 * Part: "assembly", "exploded", "base", "lid", "guard", "coupon".
 * Screws, battery bays and external radio mounts are deliberately absent.
 */
role = "explorer";
part = "assembly";
show_envelopes = true;
$fn = 48;
wall=2.8;
floor_t=3;
roof_t=2.8;
body_h=54;
main_h=48;
lid_drop=8;
fit_xy=0.5; // initial total horizontal separation; coupon before committing
uno=role=="main"?[68.85,53.34,20]:[68.6,53.4,20]; // official planar sizes; height is a planning allowance
breadboard=[83,55,12]; // ASSUMED half-size; not a measured component
joystick_hole_d=28; // assumed cap/swing opening, not module mounting size
sensor_hole_d=12; // depends on bare LDR versus a sensor module
pot_hole_d=8; // verify shaft/bushing
button_hole_d=12; // verify button; tactile 6x6 may need a printed actuator
lcd_window=[72,25]; // VERIFY actual LCD visible area before cutting
servo_body=[23,12.2,29]; // TowerPro nominal; horn and flange require measurement
W=role=="main"?160:214;
D=role=="main"?120:138;
H=role=="main"?main_h:body_h;
split=H-lid_drop;

module rr(w,d,r){translate([r,r])offset(r=r)square([w-2*r,d-2*r]);}
module outline(){
 if(role=="main")rr(W,D,13);
 else union(){translate([6,0])rr(202,106,18);translate([34,104])circle(r=34);translate([180,104])circle(r=34);}
}
module flat_shell(h){difference(){linear_extrude(h)outline();translate([0,0,floor_t])linear_extrude(h+1)offset(delta=-wall)outline();}}
module port_cuts(){
 // Large service windows are nominal. Their final centers follow the plugged-in board.
 if(role=="main"){
  translate([-1,64,9])cube([22,16,13]); // USB-C plug envelope from left
  for(x=[111,139])translate([x,-1,18])cube([10,14,10]); // two I2C harness entries
 }else{
  translate([-1,28,9])cube([24,20,20]); // USB-B and molded plug access
  translate([102,-1,19])cube([10,12,10]); // 3-wire I2C exit
  if(role=="architect")translate([171,-1,14])cube([9,12,9]); // dedicated regulated servo supply lead
 }
}
module rail_pair(x,y,w,d){
 // Edge support ledges only. Retention keys and safe PCB contact points remain to fit.
 for(yy=[y-2,y+d])translate([x-2,yy,floor_t-0.2])cube([w+4,2,3.2]);
 for(xx=[x-2,x+w])translate([xx,y-2,floor_t-0.2])cube([2,d+4,3.2]);
}
module routes(){
 // Floor-mounted wire saddles have open tops for assembly and service.
 for(x=role=="main"?[115,137]:[91,192])
  translate([x,14,2.8])difference(){cube([9,7,7]);translate([2,-1,2])cube([5,9,7]);}
}
module base(){
 difference(){
  union(){
   flat_shell(split);
   translate([0,0,split-2])linear_extrude(2)difference(){outline();offset(delta=-wall-2-fit_xy/2)outline();}
   // alignment rim, with 0.5mm initial total separation to the mating skirt
   translate([0,0,split-0.2])linear_extrude(4.2)difference(){offset(delta=-wall-fit_xy/2)outline();offset(delta=-wall-2-fit_xy/2)outline();}
   if(role=="main")rail_pair(12,60,uno[0],uno[1]);
   else{rail_pair(17,24,uno[0],uno[1]);rail_pair(99,24,breadboard[0],breadboard[1]);}
   routes();
  }
  port_cuts();
  // Finger access to release future tested retention keys; no blind closed snap hooks.
  for(x=[28,W-40])translate([x,2,split-6])cube([12,5,4]);
 }
}
module controls_cut(){
 if(role=="explorer"){
  translate([47,43,-1])cylinder(h=roof_t+3,d=joystick_hole_d);
  translate([166,22,-1])cylinder(h=roof_t+3,d=sensor_hole_d);
 }else if(role=="architect"){
  translate([45,40,-1])cylinder(h=roof_t+3,d=pot_hole_d);
  translate([169,40,-1])cylinder(h=roof_t+3,d=button_hole_d);
  translate([107,91,-1])cylinder(h=roof_t+3,d=10); // measured shaft/horn passage later
 }else{
  translate([80-lcd_window[0]/2,29-lcd_window[1]/2,-1])cube([lcd_window[0],lcd_window[1],roof_t+3]);
  for(y=[75,81,87])translate([128,y,-1])cube([19,2.5,roof_t+3]);
 }
}
module lid(){
 difference(){
  union(){
   linear_extrude(roof_t)outline();
   translate([0,0,-(lid_drop-roof_t)])linear_extrude(lid_drop-roof_t+0.2)difference(){outline();offset(delta=-wall)outline();}
   translate([0,0,-4])linear_extrude(4.2)difference(){offset(delta=-wall-2-fit_xy)outline();offset(delta=-wall-4-fit_xy)outline();}
   // Accessory mounting rails are intentionally broad nominal lands, not fitted clips.
   if(role=="architect")for(x=[88,122])translate([x,80,-17])cube([3,22,17.2]);
  }
  controls_cut();
 }
}
module guard(){
 // Nominal closed cage around the small gate. Keeper and coupling need horn measurements.
 difference(){
  translate([78,73,0])linear_extrude(29)rr(58,33,5);
  translate([81,76,-1])linear_extrude(27)rr(52,27,3);
  // Narrow viewing slots, not an unrestricted open moving mechanism.
  for(x=[84:7:126])translate([x,70,8])cube([3,40,14]);
 }
}
module envelopes(){
 if(role=="main"){
  color([.3,.3,.3,.5])translate([12,60,6])cube(uno);
  color([.6,.6,.6,.5])translate([40,11,H-20])cube([80,36,17]);
 }else{
  color([.3,.3,.3,.5])translate([17,24,6])cube(uno);
  color([.7,.7,.7,.5])translate([99,24,6])cube(breadboard);
  if(role=="explorer")color([.2,.2,.2,.6])translate([47,43,H+3])cylinder(h=12,d=24);
  if(role=="architect"){
   color([.2,.2,.2,.6])translate([45,40,H])cylinder(h=16,d=24);
   color([.4,.4,.4,.6])translate([169,40,H])cylinder(h=8,d=10);
   color([.5,.5,.5,.5])translate([95.5,84.9,H-29])cube(servo_body);
  }
 }
}
module coupon(){
 // Simple ledge fit sample. Not a final snap-fit qualification.
 for(i=[0:2])translate([i*35,0,0])difference(){cube([30,24,9]);translate([3,3,3])cube([24,18,7]);}
 for(i=[0:2])translate([i*35,32,0])union(){cube([30,24,2.8]);translate([3+(0.3+i*0.2)/2,3+(0.3+i*0.2)/2,2.6])difference(){cube([24-(0.3+i*0.2),18-(0.3+i*0.2),4]);translate([2,2,-1])cube([20-(0.3+i*0.2),14-(0.3+i*0.2),6]);}}
}
if(part=="base")base();
else if(part=="lid")translate([0,0,4])lid();
else if(part=="guard")guard();
else if(part=="coupon")coupon();
else{
 color([.75,.75,.75])base();
 color([.92,.92,.92])translate([0,0,H-roof_t+(part=="exploded"?35:0)])lid();
 if(role=="architect")color([.65,.65,.65])translate([0,0,H+(part=="exploded"?48:0)])guard();
 if(show_envelopes)%envelopes();
}
