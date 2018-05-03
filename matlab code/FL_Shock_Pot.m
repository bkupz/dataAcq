function IN = FL_Shock_Pot(Vi,BATT)

IN = (0.0848*(Vi*(5/BATT))^2)+(1.2141*(Vi*(5/BATT)))+11.671;
end