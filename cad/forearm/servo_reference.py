"""FT5425BL A/0 drawing dimensions; reference geometry, not a supplier fit certificate."""
import cadquery as cq
BODY_W=20.0
BODY_L=40.6
BODY_H=30.0
SHAFT_OFFSET=11.5
SHAFT_DIAMETER=5.9
SHAFT_TOTAL_HEIGHT=34.9
EAR_LENGTH=54.4
EAR_BOTTOM=20.55
EAR_TOP=23.05
MOUNT_PITCH_LONG=49.5
MOUNT_PITCH_CROSS=10.0
MOUNT_HOLE_DIAMETER=4.5
SERVO_STATIONS=((-25,-128,-1),(0,-118,1),(25,-128,-1))

def geometry(x,y,direction,z=-11):
 def box(w,l,h,xx,yy,zz):return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((xx,yy,zz))
 body=box(BODY_W,BODY_L,BODY_H,x,y,z)
 ears=box(BODY_W,EAR_LENGTH,EAR_TOP-EAR_BOTTOM,x,y,z+EAR_BOTTOM)
 for dx in [-MOUNT_PITCH_CROSS/2,MOUNT_PITCH_CROSS/2]:
  for dy in [-MOUNT_PITCH_LONG/2,MOUNT_PITCH_LONG/2]:
   cut=cq.Workplane('XY').circle(MOUNT_HOLE_DIAMETER/2).extrude(4).translate((x+dx,y+dy,z+EAR_BOTTOM-.5))
   ears=ears.cut(cut)
 shaft=cq.Workplane('XY').circle(SHAFT_DIAMETER/2).extrude(SHAFT_TOTAL_HEIGHT-BODY_H).translate((x,y+direction*SHAFT_OFFSET,z+BODY_H))
 return body.union(ears).union(shaft)
