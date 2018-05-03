function IN = FR_Shock_Pot(Vi,BATT)

IN = (0.0645*(Vi*(5/BATT))^2)+(1.2583*(Vi*(5/BATT)))+11.403;
end
