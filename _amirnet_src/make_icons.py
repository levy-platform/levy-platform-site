"""Draws the app icons (no PIL): indigo tile, white 'A', green check badge. Run: python3 -I _amirnet_src/make_icons.py"""
import zlib, struct, math, os
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "amirnet", "icons")
IND=(79,70,229); WHITE=(255,255,255); GREEN=(34,165,90)
def seg_d(px,py,ax,ay,bx,by):
    vx,vy=bx-ax,by-ay; t=max(0,min(1,((px-ax)*vx+(py-ay)*vy)/(vx*vx+vy*vy))); dx,dy=px-(ax+t*vx),py-(ay+t*vy); return math.hypot(dx,dy)
def render(size, maskable):
    ss=3; N=size*ss; s=(0.62 if maskable else 0.78)*N; o=(N-s)/2; r=0.22*N
    lw=s*.14/2; cw=s*.05/2
    A=[(o+s*.22,o+s*.84,o+s*.5,o+s*.16),(o+s*.5,o+s*.16,o+s*.78,o+s*.84),(o+s*.34,o+s*.58,o+s*.66,o+s*.58)]
    cx,cy,cr=o+s*.86,o+s*.2,s*.15
    C=[(o+s*.79,o+s*.2,o+s*.84,o+s*.25),(o+s*.84,o+s*.25,o+s*.93,o+s*.15)]
    rows=[]
    for y in range(size):
        row=bytearray([0])
        for x in range(size):
            acc=[0,0,0,0]
            for sy in range(ss):
                for sx in range(ss):
                    px,py=x*ss+sx+.5,y*ss+sy+.5
                    inside=True
                    if not maskable:
                        qx=min(max(px,r),N-r); qy=min(max(py,r),N-r)
                        inside=math.hypot(px-qx,py-qy)<=r
                    if not inside: continue
                    col=IND
                    if any(seg_d(px,py,*a)<=lw for a in A): col=WHITE
                    if math.hypot(px-cx,py-cy)<=cr:
                        col=GREEN
                        if any(seg_d(px,py,*c)<=cw for c in C): col=WHITE
                    acc[0]+=col[0];acc[1]+=col[1];acc[2]+=col[2];acc[3]+=255
            n=ss*ss; a=acc[3]//n
            if a: row+=bytes([acc[0]//(acc[3]//255), acc[1]//(acc[3]//255), acc[2]//(acc[3]//255), a])
            else: row+=bytes([0,0,0,0])
        rows.append(bytes(row))
    raw=b"".join(rows)
    def chunk(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    return b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",size,size,8,6,0,0,0))+chunk(b"IDAT",zlib.compress(raw,9))+chunk(b"IEND",b"")
for name,size,mask in [("icon-192.png",192,False),("icon-512.png",512,False),("maskable-512.png",512,True),("apple-touch-icon.png",180,True)]:
    open(os.path.join(OUT,name),"wb").write(render(size,mask)); print(name)
