DATA <- read.csv("global_power_plant_database_v_1_3/global_power_plant_database.csv",header = TRUE, sep= ',', quote='\"', dec= '.' )

N <- dim(DATA)[1]
coord <- DATA[1:N,c(1,6,7,8)]
c <-coord$primary_fuel == "Oil" | coord$primary_fuel == "Gas" | coord$primary_fuel == "Coal"
coord_fossil <- coord[c,1:4]
write.csv(coord_fossil, "Coordinates_FossilFuelPowerPlants.csv",row.names= TRUE)