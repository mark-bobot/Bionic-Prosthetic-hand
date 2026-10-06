"""Depth-buffered orthographic preview of exported CAD, not a product photograph."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import cadquery as cq
from matplotlib import font_manager

def render(path, output, title='Right bionic Phoenix — prototype 0.2.1'):
    shape=cq.importers.importStep(str(path))
    meshes=[]
    for solid in shape.solids().vals():
        vertices,triangles=solid.tessellate(.35)
        v=np.array([p.toTuple() for p in vertices]); f=np.asarray(triangles)
        b=solid.BoundingBox()
        color=np.array([172,188,193] if b.ymax>0 and b.zmax>0 else [105,133,147],float)
        meshes.append((v[f],color))
    az,el=np.radians([-35,28])
    toward=np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])
    right=np.array([-np.sin(az),np.cos(az),0]);up=np.cross(toward,right)
    basis=np.stack([right,up,toward],axis=1)
    cloud=np.concatenate([m[0].reshape(-1,3) for m in meshes])@basis
    lower=cloud[:,:2].min(axis=0);upper=cloud[:,:2].max(axis=0)
    width,height=1600,1150;scale=min((width-120)/(upper[0]-lower[0]),(height-200)/(upper[1]-lower[1]))
    center=(lower+upper)/2
    pixels=np.full((height,width,3),250,np.uint8);depth=np.full((height,width),-np.inf)
    light=np.array([.1,-.3,1]);light=light/np.linalg.norm(light)
    for triangles,color in meshes:
        normal=np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0])
        normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12)
        shades=.55+.45*np.abs(normal@light)
        projected=triangles@basis
        projected[:,:,0]=(projected[:,:,0]-center[0])*scale+width/2
        projected[:,:,1]=-(projected[:,:,1]-center[1])*scale+(height+80)/2
        for t,shade in zip(projected,shades):
            x0=max(0,int(np.floor(t[:,0].min())));x1=min(width-1,int(np.ceil(t[:,0].max())))
            y0=max(0,int(np.floor(t[:,1].min())));y1=min(height-1,int(np.ceil(t[:,1].max())))
            if x1<x0 or y1<y0:continue
            a,b,c=t;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(den)<1e-10:continue
            yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
            u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
            v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den
            w=1-u-v;z=u*a[2]+v*b[2]+w*c[2]
            region=depth[y0:y1+1,x0:x1+1]
            mask=(u>=-1e-8)&(v>=-1e-8)&(w>=-1e-8)&(z>region)
            region[mask]=z[mask];pixels[y0:y1+1,x0:x1+1][mask]=(color*shade).astype(np.uint8)
    image=Image.fromarray(pixels);draw=ImageDraw.Draw(image)
    font_path=font_manager.findfont('DejaVu Sans')
    font=ImageFont.truetype(font_path,30);small=ImageFont.truetype(font_path,20)
    draw.text((width/2,35),title,font=font,fill='#26363d',anchor='mt')
    draw.text((width/2,80),'CAD preview • assumed socket dimensions • physical fit and load tests pending',font=small,fill='#53636b',anchor='mt')
    image.save(output)

if __name__=='__main__':
    root=Path(__file__).resolve().parent/'exports'
    render(root/'complete_right_bionic.step',root/'complete_preview.png')
