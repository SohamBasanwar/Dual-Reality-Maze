/* Dual-Reality Maze / ergonomic revision 2 / millimeters / 2026-10-23
 * PARAMETRIC DESIGN STUDY. Reference components, not measured user hardware.
 * No final fit, retention, thermal or hand-comfort qualification.
 * role: explorer | architect | main; part: assembly | exploded | base | lid | guard | crystal
 * The whole family uses full-size breadboard allowances. No screw or battery bays.
 */
role="explorer";
part="assembly";
show_components=true;
$fn=48;
W=240; D=role=="main"?180:183;
H=role=="main"?66:54;
split=H-14;
wall=3; floor_t=3; roof_t=3;
bb=[166,55,10]; // adjustable ENVELOPE; Adafruit 239 reference is 163x53x10
uno=role=="main"?[68.85,53.34,20]:[68.6,53.4,20]; // height reserved, PCB dimensions published
bb_xy=role=="main"?[37,18]:[37,18];
uno_xy=role=="main"?[28,105]:[85,78];
module rr(w,d,r){translate([r,r])offset(r=r)square([w-2*r,d-2*r]);}
module outline(){
 if(role=="main")offset(r=7)offset(delta=-7)polygon([[40,0],[200,0],[240,40],[240,140],[200,180],[40,180],[0,140],[0,40]]);
 else offset(r=-6)offset(r=6)union(){
  rr(240,138,30);
  for(side=[0,1])hull(){
   translate([side?195:45,103])scale([1.2,1])circle(r=31);
   translate([side?202:38,155])scale([1.12,1])circle(r=28);
  }
 }
}
module centered_scale(s){translate([W/2,D/2])scale([s,s])translate([-W/2,-D/2])children();}
module skin(z,h,s1,s2,inset=0){
 translate([W/2,D/2,z])linear_extrude(h,scale=s2/s1)
  translate([-W*s1/2,-D*s1/2])scale([s1,s1])offset(delta=-inset)outline();
}
module ring_rail(x,y,w,d){
 translate([x-2,y-2,2.8])linear_extrude(4.2)
 difference(){square([w+4,d+4]);translate([2,2])square([w,d]);}
}
module base(){difference(){union(){
 difference(){
  union(){skin(0,8,.96,1);skin(8,split-8,1,1);}
  union(){skin(3,5,.975,1,wall);skin(8,split-7.9,1,1,wall);}
 }
 ring_rail(bb_xy[0]-.5,bb_xy[1]-.5,bb[0]+1,bb[1]+1);
 ring_rail(uno_xy[0]-.5,uno_xy[1]-.5,uno[0]+1,uno[1]+1);
 // Cable saddle lands. Reusable straps loop through these, not over live contacts.
 for(x=[20,216])translate([x,35,2.8])difference(){cube([8,12,7]);translate([-1,3,2])cube([10,6,3]);}
 // Main power module space is reserved; final cradle follows selected module.
 if(role=="main")ring_rail(130,112,80,42);
 }
 // Rear grommet/cable exits; use measured pigtails rather than guessed USB socket positions.
 for(x=role=="main"?[80,120,160]:[110,130])translate([x,-2,20])cube([10,14,10]);
}}
module control_holes(){
 if(role=="main"){
  translate([84,32,-1])cube([72,26,18]);
  // Crystal button's guide is provisional. Fit actuator to a captured momentary switch.
  translate([120,99,-1])cylinder(h=18,d=18);
  for(y=[105:6:123])translate([188,y,-1])cube([18,2.5,18]);
 }else if(role=="explorer"){
  translate([43,94,-1])cylinder(h=18,d=28);
  translate([197,94,-1])cylinder(h=18,d=12);
 }else{
  translate([43,94,-1])cylinder(h=18,d=8);
  translate([197,84,-1])cylinder(h=18,d=16);
  translate([176,118,-1])cylinder(h=18,d=10);
 }
}
module lid(){difference(){union(){
 difference(){skin(0,14,1,.96);skin(-.1,11.1,1,.969,wall);}
 // Locating skirt; 0.5 mm per-side nominal gap. Locking keys remain a separate fit step.
 translate([0,0,-4])linear_extrude(5)difference(){offset(delta=-3.5)outline();offset(delta=-5.5)outline();}
 }
 control_holes();
 // Shallow broad channels improve tactile location; no sharp palm-side teeth.
 if(role!="main")for(side=[0,1],j=[0:3])
  translate([side?192:25,137+j*7,13.4])rotate([0,0,side?-12:12])cube([20,2,2]);
}}
module crystal(){
 // Separate aesthetic cap study; guide, travel stop and retention flange must match the switch.
 union(){cylinder(h=3,d=22,$fn=6);translate([0,0,3])cylinder(h=7,r1=11,r2=5,$fn=6);}
}
module guard(){difference(){
 linear_extrude(27)rr(58,34,6);
 translate([3,3,-.1])linear_extrude(24)rr(52,28,4);
 for(x=[10:8:48])translate([x,-1,8])cube([3,36,12]);
}}
module components(){
 color([.25,.25,.25])translate([uno_xy[0],uno_xy[1],7])cube(uno);
 color([.8,.8,.8])translate([bb_xy[0],bb_xy[1],7])cube(bb);
 if(role=="main"){
  color([.3,.3,.3])translate([79.7,27,H-22])cube([80.6,36,19]);
  color([.45,.45,.45])translate([130,112,7])cube([80,42,22]);
 }else if(role=="explorer"){
  color([.25,.25,.25])translate([26,81,H-24])cube([34,26,20]);
  color([.25,.25,.25])translate([43,94,H+1])cylinder(h=9,d=23);
 }else{
  color([.25,.25,.25])translate([43,94,H])cylinder(h=12,d=28);
  color([.25,.25,.25])translate([197,84,H])cylinder(h=4,d=14);
  // Right of Uno: separate body envelope and wire space; final flange and shaft offset need verification.
  color([.4,.4,.4])translate([164.5,111.9,H-29])cube([23,12.2,29]);
 }
}
module applied_art(){
 // Surface artwork visualization only. Use supplied SVG decals; excluded from individual CAD solids.
 color([.12,.12,.12])translate(role=="main"?[99,127,H+.1]:[92,14,H+.1])
 linear_extrude(.12)scale(role=="main"?.6:.8)import(str("../assets/",role,"-crest-black.svg"));
 if(role=="main")color([.12,.12,.12])translate([0,0,H+.1])linear_extrude(.12)
 difference(){translate([79,27])rr(82,36,5);translate([82,30])rr(76,30,3);}
 else color([.12,.12,.12])translate([43,94,H+.1])linear_extrude(.12)
 difference(){circle(d=38);circle(d=35);}
}
if(part=="base")base();
else if(part=="lid")translate([0,0,4])lid();
else if(part=="guard")guard();
else if(part=="crystal")crystal();
else{
 color([.58,.58,.58])base();
 color([.86,.86,.86])translate([0,0,split+(part=="exploded"?50:0)])lid();
 if(role=="architect")color([.65,.65,.65])translate([147,101,H+(part=="exploded"?50:0)])guard();
 if(role=="main")color([.3,.3,.3])translate([120,99,H+(part=="exploded"?50:0)])crystal();
 if(show_components)components();
 translate([0,0,part=="exploded"?50:0])applied_art();
}
