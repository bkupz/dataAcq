function RPM = Tachometer(Fc,A) %A is the # of magnets per shaft

RPM = (Fc*60)/A;
end