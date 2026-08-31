c Build 2025 example
c ***CELLS***
101 301 -5.08 -201 imp:n,p 1 $ Detector 
121 2 -4.78 -31 imp:n,p 1 $ PE+Pb shielding 
21 13 -0.92 -41 42 imp:n,p 1 $ Wheel 

c ***SURFACES***
201 RCC 56 -5 -1 0 20 0 4.5
31 RPP 19 29 -7.5 7.5 -11 9
41 RCC -2 77 8 0 25 0 29
42 RCC -2 77 8 0 25 0 27.7

c ***SOURCE***
sdef erg=14.0 pos=0 0 0 dir=d1 vec=0 0 1
si1 -1 .93 1
sp1 0 0.0 1.0
c ***MATERIALS***
c Detector
m301	35079 -0.2946 $ Br79
	35081 -0.3069 $ Br81
	57139 -0.3485 $ La139
	58140 -0.05 $ Ce140
c PE+Pb
m2	6000 -0.04286 $ C
	1001 -0.00714 $ H
	82000 -0.95 $ Pb
c Wheel
m13	1001 -0.118371 $ H
	6000 -0.881629 $ C
c ***TALLIES***
F8:n,p (101)
E8 0 1e-5 932i 8.4295
FT8 GEB -0.026198 0.059551 -0.037176 PHL 1 6 1 0
c ***DATA***
mode n p
prdmp 1e8 1e8 -1 $ dump every hour
Cut:n 1j 0.1 $ 100 keV Neutron Energy Cutoff
phys:n 1j 14 $analog neutron transport
phys:p
nps 1e9
