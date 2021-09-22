close all
clear all

data = dlmread("singleQuad.csv");

hold all
for line = data'
  id = line(1);
  x = line(2);
  y = line(3);
  z = line(4);
  
  scatter3(x,y,z,'filled')
end

legend("0","1","2","3")

