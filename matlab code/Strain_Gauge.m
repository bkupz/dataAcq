function IN = Strain_Gauge(Vi,GF,CC)
VP=12.1;
Gain=100;
IN =(4*((Vi-CC)/Gain))/((GF*VP)-(2*((Vi-CC)/Gain))); 
end