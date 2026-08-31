c Water box example
c ***CELLS***
1 1 0.066 -1 imp:n,p 1 $ Water-filled box 

c ***SURFACES***
1 RPP -10 10 -10 10 -10 10

c ***SOURCE***
sdef erg=14.0 pos=0 0 0 dir=d1 vec=0 0 1
si1 -1 .93 1
sp1 0 0.0 1.0
c ***MATERIALS***
c Water
m1	1001.80c 2 
	8016.80c 1 
c ***TALLIES***
c ***DATA***
mode n p
prdmp 1e8 1e8 -1 $ dump every hour
Cut:n 1j 0.1 $ 100 keV Neutron Energy Cutoff
phys:n 1j 14 $analog neutron transport
phys:p
nps 1e9
