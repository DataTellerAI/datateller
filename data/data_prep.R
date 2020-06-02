
# Package -----------------------------------------------------------------
library(tidyverse)
library(readxl)
library(stringi)
library(stringdist)
library(openxlsx)
library(backports)
library(RJSONIO)
library(jsonlite)
library(reshape2)

# Colombia ----------------------------------------------------------------

load("/Users/campopinillos/OneDrive - Universidad Externado de Colombia/01 UNIVERSIDAD/Tesis - Campo/BDTesisFinal.RData")

nombresCol <- filter(df, !is.na(GENERO), !is.na(NOMBRES)) %>%
  select(Nombres = NOMBRES, Genero = GENERO, Probabilidad = PROB_GENERO, Edad = EDAD_SINIESTRO) %>% 
  mutate(Nombres = stri_trans_totitle(Nombres)) %>% 
  mutate(Genero = as.character(Genero)) %>% 
  mutate(Genero = stri_trans_totitle(Genero)) %>%  
  mutate(Probabilidad = ifelse(Probabilidad=='Hombre' | Probabilidad=='Mujer', '1',Probabilidad)) %>% 
  mutate(Probabilidad = as.numeric(Probabilidad)) %>% 
  mutate(Probabilidad = ifelse(Probabilidad >= 0.7, 1, Probabilidad)) %>% 
  mutate(Probabilidad = ifelse(is.na(Probabilidad), 1, Probabilidad))

nombresCol <- nombresCol %>% 
  group_by(Nombres, Genero, Probabilidad) %>% 
  summarise(Frecuencia = n(), EdadMedia=round(mean(Edad)))

nombresCol <- nombresCol %>% 
  mutate(Dup1 = duplicated(paste(Nombres))) %>% 
  mutate(Dup2 = duplicated(paste(Nombres), fromLast = T))
  
# View(filter(nombresCol,Dup1==T| Dup2==T))

nombresCol <- nombresCol %>% 
  mutate(Probabilidad = ifelse(Dup1==T|Dup2==T, 1,Probabilidad)) %>% 
  group_by(Nombres,Genero,Probabilidad) %>% 
  summarise(Frecuencia = sum(Frecuencia), EdadMedia=mean(EdadMedia)) %>% 
  mutate(Pais = 'Colombia',
         Dup1 = duplicated(paste(Nombres)),
         Dup2 = duplicated(paste(Nombres), fromLast = T))

# View(filter(nombresCol, Dup1==T| Dup2==T))

nombresCol <- select(nombresCol, names(nombresCol)[1:6])
rm(df)

# Argentina ---------------------------------------------------------------

nombresArg <- read_xlsx("/Users/campopinillos/Documents/Proyecto Final/nombres.xlsx", sheet = 1)

nombresArg <- nombresArg %>% 
  mutate(Genero = ifelse(Genero %in%c('M','MASCULINO','m'), 'Hombre', Genero)) %>% 
  mutate(Genero = ifelse(Genero %in%c('F','FEMENINO'), 'Mujer', Genero)) %>% 
  mutate(Genero = ifelse(Genero %in%c('A'), 'Ambiguo', Genero)) %>% 
  mutate(Nombre = stri_trans_totitle(Nombre),
         Pais = stri_trans_totitle(Pais),
         Frecuencia = NA, EdadMedia = NA) 

names(nombresArg)[names(nombresArg)=='Nombre'] <- 'Nombres'
nombresArg <- filter(nombresArg,!(Nombres=='Jose' & Genero=='Mujer'))
nombresArg <- filter(nombresArg,!(Nombres=='Kamila' & Genero=='Hombre'))
nombresArg <- filter(nombresArg,!(Nombres=='Karol' & Genero=='Hombre'))
nombresArg <- filter(nombresArg,!(Nombres=='Iñaki' & Genero=='Mujer'))
nombresArg <- filter(nombresArg,!(Nombres=='Marlin' & Genero=='Mujer'))

nombresArg <- nombresArg %>% 
  group_by(Nombres,Genero, EdadMedia, Pais) %>%
  summarise(Frecuencia=n()) %>% 
  mutate(Dup1 = duplicated(paste(Nombres))) %>% 
  mutate(Dup2 = duplicated(paste(Nombres), fromLast = T))

nombresArg <- filter(nombresArg,!(Genero=='Ambiguo' & Dup1==T))
nombresArg <- filter(nombresArg,!(Genero=='Ambiguo' & Dup2==T))

nombresArg <- nombresArg %>% 
  mutate(Dup1 = duplicated(paste(Nombres)),
         Dup2 = duplicated(paste(Nombres), fromLast = T),
         Probabilidad = ifelse(Genero %in%c('Hombre','Mujer'),1,NA),
         Probabilidad = ifelse(Genero %in%c('Ambiguo'),0.5,Probabilidad))

nombresArg <- filter(nombresArg,!(Dup1==T | Dup2==T))

# table(nombresArg$Genero)
# View(filter(nombresArg, Dup1==T| Dup2==T))

nombresArg <- select(nombresArg, names(nombresCol))

# nombresArg <- filter(nombresArg, Genero!='Ambiguo')
# View(filter(nombresArg,Genero=='Ambiguo'))

# Mexico ------------------------------------------------------------------

nombresMexH <- read_csv("/Users/campopinillos/OneDrive - Universidad Externado de Colombia/01 UNIVERSIDAD/Tesis - Campo/Back-ups Datos/hombres.csv")

nombresMexH$Genero = 'Hombre'

nombresMexM <- read_csv("/Users/campopinillos/OneDrive - Universidad Externado de Colombia/01 UNIVERSIDAD/Tesis - Campo/Back-ups Datos/mujeres.csv")

nombresMexM$Genero = 'Mujer'

nombresMex <- rbind(nombresMexH, nombresMexM)
rm(nombresMexH,nombresMexM)

names(nombresMex)[names(nombresMex)=='nombre'] <- 'Nombres'
names(nombresMex)[names(nombresMex)=='frec'] <- 'Frecuencia'
names(nombresMex)[names(nombresMex)=='edad_media'] <- 'EdadMedia'

nombresMex <- nombresMex %>% 
  mutate(Probabilidad = 1, Pais = 'México',
         Nombres = stri_trans_totitle(Nombres))
         
nombresMex <- nombresMex %>% 
  group_by(Nombres, Genero, Probabilidad, Pais) %>% 
  summarise(Frecuencia = sum(Frecuencia),
            EdadMedia = mean(EdadMedia)) 

nombresMex <- nombresMex %>% 
  mutate(Dup1 = duplicated(paste(Nombres), fromLast = F)) %>% 
  mutate(Dup2 = duplicated(paste(Nombres), fromLast = T))

nombresMex1 <- filter(nombresMex, Dup1==T| Dup2==T)
nombresMex <- filter(nombresMex, !(Dup1==T| Dup2==T))

nombresMex1 <- nombresMex1 %>% 
  select(Nombres, Genero, Frecuencia, EdadMedia)

nombresMexP <- dcast(nombresMex1, Nombres ~ Genero, value.var=c("Frecuencia"))
nombresMexQ <- dcast(nombresMex1, Nombres ~ Genero, value.var=c("EdadMedia"))

nombresMexP <- merge(nombresMexP,nombresMexQ, by = 'Nombres' )
nombresMexP <- nombresMexP %>% 
  mutate(Genero = ifelse(Hombre.x > Mujer.x,'Hombre', 'Mujer')) %>% 
  mutate(Frecuencia = ifelse(Genero=='Hombre', Hombre.x, Mujer.x))%>% 
  mutate(EdadMedia = ifelse(Genero=='Hombre', Hombre.y, Mujer.y))

nombresMexP <- nombresMexP %>% 
  select(Nombres, Genero, Frecuencia, EdadMedia) %>% 
  mutate(Probabilidad = 1, Pais = 'México')

nombresMex <- select(nombresMex, names(nombresCol))

nombresMex <- rbind(nombresMex, nombresMexP)

rm(nombresMexQ, nombresMex1, nombresMexP)


nombresMex <- nombresMex %>% 
  mutate(Dup1 = duplicated(paste(Nombres), fromLast = F)) %>% 
  mutate(Dup2 = duplicated(paste(Nombres), fromLast = T))


# View(filter(nombresMex, Dup1==T| Dup2==T))

nombresMex <- select(nombresMex, names(nombresCol))

# USA Base ---------------------------------------------------------------

load("/Users/campopinillos/Documents/Proyecto Final/sysdata.rda")

nombresUsa <- basic_names %>% 
  group_by(name) %>% 
  summarise(Hombres = sum(male), Mujeres = sum(female))

nombresUsa <- nombresUsa %>% 
  ungroup() %>%
  mutate(name = stri_trans_totitle(name)) %>% 
  mutate(Genero = ifelse(Hombres > Mujeres,'Hombre', 'Mujer')) %>% 
  mutate(Frecuencia = ifelse(Genero=='Hombre', Hombres, Mujeres),
         Pais = 'USA', Probabilidad = 1, EdadMedia = NA)

names(nombresUsa)[names(nombresUsa)=='name'] <- 'Nombres'


nombresUsa <- nombresUsa %>%
  select(names(nombresCol))
  
rm(basic_names)
# Base Complete -----------------------------------------------------------

nombres <- rbind(nombresCol,nombresArg,nombresMex,nombresUsa)

nombres <- nombres %>%
  ungroup() %>% 
  mutate(Nombres = str_replace_all(Nombres, "[[:punct:]]", "")) %>% 
  mutate(Nombres = str_replace_all(Nombres, "[^[:alnum:]]", " ")) %>% 
  mutate(Nombres = str_replace_all(Nombres, '[[:digit:]]+', '')) %>% 
  mutate(Nombres = str_to_title(tolower(Nombres))) %>% 
  mutate(Nombres = str_squish(Nombres)) %>% 
  mutate(Nombres = trimws(Nombres, which = c("both"), whitespace = "[ \t\r\n]"))

nombres <- nombres %>% 
  mutate(Dup1 = duplicated(paste(Nombres), fromLast = F)) %>% 
  mutate(Dup2 = duplicated(paste(Nombres), fromLast = T))

nombresComunes <- filter(nombres, Dup1==T| Dup2==T)
nombres <- filter(nombres, !(Dup1==T| Dup2==T))
nombres <- nombres[!names(nombres)%in%c('Dup1','Dup2')]
nombresComunes1 <- nombresComunes %>% 
  select(Nombres, Genero, Frecuencia, EdadMedia) %>% 
  group_by(Nombres, Genero) %>% 
  summarise(Frecuencia = sum(Frecuencia),
            EdadMedia = round(mean(EdadMedia, na.rm = T)))

nombresComunes <- nombresComunes %>% 
  select(Nombres, Genero, Pais) %>% 
  mutate(Dup = duplicated(Nombres))

nombresComunes <- filter(nombresComunes, Dup==F)
nombresComunes <- nombresComunes[!names(nombresComunes)%in%'Dup']
nombresComunes <- merge(nombresComunes1,
                        nombresComunes, 
                        by=c('Nombres','Genero'),
                        all.x = T, all.y = F)

nombresComunes$Probabilidad = 1

nombres <- rbind(nombres, nombresComunes)

rm(nombresComunes, nombresComunes1)

nombres <- nombres %>% 
  mutate(Dup1 = duplicated(paste(Nombres), fromLast = F)) %>% 
  mutate(Dup2 = duplicated(paste(Nombres), fromLast = T))

nombresComunes <- filter(nombres, Dup1==T| Dup2==T)
nombres <- filter(nombres, !(Dup1==T| Dup2==T))
nombres <- nombres[!names(nombres)%in%c('Dup1','Dup2')]

nombresComunes1 <- nombresComunes %>% 
  select(Nombres, Genero, Frecuencia, EdadMedia)

nombresComunes1_1 <- dcast(nombresComunes1, Nombres ~ Genero, value.var=c("Frecuencia"))
nombresComunes1_2 <- dcast(nombresComunes1, Nombres ~ Genero, value.var=c("EdadMedia"))

nombresComunes1_1 <- merge(nombresComunes1_1,nombresComunes1_2, by = 'Nombres' )

nombresComunes1_1 <- nombresComunes1_1 %>% 
  select(Nombres, Hombre.x,Mujer.x, Hombre.y, Mujer.y) %>% 
  mutate(Hombre.x = ifelse(is.na(Hombre.x), 0, Hombre.x)) %>% 
  mutate(Mujer.x = ifelse(is.na(Mujer.x), 0, Mujer.x))
                    
nombresComunes1_1 <- nombresComunes1_1 %>% 
  mutate(Genero = ifelse(Hombre.x > Mujer.x,'Hombre', 'Mujer')) %>% 
  mutate(Frecuencia = ifelse(Genero=='Hombre', Hombre.x, Mujer.x))%>% 
  mutate(EdadMedia = ifelse(Genero=='Hombre', Hombre.y, Mujer.y))

nombresComunes1_1 <- nombresComunes1_1 %>% 
  select(Nombres, Genero, Frecuencia, EdadMedia)

nombresComunes <- filter(nombresComunes, !is.na(Pais)) %>% 
  select(Nombres, Pais)

nombresComunes <- merge(nombresComunes1_1, nombresComunes, by ='Nombres')
nombresComunes$Probabilidad = 1

nombres <- rbind(nombres, nombresComunes)

rm(nombresComunes,nombresComunes1, nombresComunes1_1, nombresComunes1_2)

nombres <- nombres %>% 
  mutate(Dup1 = duplicated(paste(Nombres), fromLast = F)) %>% 
  mutate(Dup2 = duplicated(paste(Nombres), fromLast = T))

View(filter(nombres, Dup1==T| Dup2==T))


table(nombres$Genero)
table(nombres$Probabilidad)
table(nombres$Pais)




save(nombres, file = '/Users/campopinillos/Documents/Proyecto Final/nombres.RData')

# Data for ML Model -----------------------------------------------------------------

load("/Users/campopinillos/Documents/Proyecto Final/nombres.Rdata")

nombres <- nombres %>%
  ungroup() %>% 
  mutate(CantNombres = sapply(strsplit(Nombres, " "), length)) %>% 
  mutate(Letras = str_length(Nombres))

nombres <- filter(nombres, CantNombres<=6, Letras>2)

unwanted_array = list('Š'='S', 'š'='s', 'Ž'='Z', 'ž'='z', 'À'='A', 'Á'='A', 'Â'='A', 'Ã'='A', 'Ä'='A', 'Å'='A', 'Æ'='A', 'Ç'='C', 'È'='E', 'É'='E',
                      'Ê'='E', 'Ë'='E', 'Ì'='I', 'Í'='I', 'Î'='I', 'Ï'='I', 'Ñ'='N', 'Ò'='O', 'Ó'='O', 'Ô'='O', 'Õ'='O', 'Ö'='O', 'Ø'='O', 'Ù'='U',
                      'Ú'='U', 'Û'='U', 'Ü'='U', 'Ý'='Y', 'Þ'='B', 'ß'='S', 'à'='a', 'á'='a', 'â'='a', 'ã'='a', 'ä'='a', 'å'='a', 'æ'='a', 'ç'='c',
                      'è'='e', 'é'='e', 'ê'='e', 'ë'='e', 'ì'='i', 'í'='i', 'î'='i', 'ï'='i', 'ð'='o', 'ñ'='n', 'ò'='o', 'ó'='o', 'ô'='o', 'õ'='o',
                      'ö'='o', 'ø'='o', 'ù'='u', 'ú'='u', 'û'='u', 'ý'='y', 'ý'='y', 'þ'='b', 'ÿ'='y' )

nombres <- nombres %>% 
  mutate(Nombres2 = chartr(paste(names(unwanted_array), collapse=''),
                           paste(unwanted_array, collapse=''),
                           Nombres)) %>%
  mutate(Nombres2 = iconv(Nombres2, to="ASCII//TRANSLIT"),
         Soundex = phonetic(Nombres2)) 

# nombres <- separate(nombres,col='NOMBRES',into = c('NOM1','NOM2','NOM3','NOM4','NOM5','NOM6'), sep = ' ', remove = F, fill = 'right')

save(nombres, file = '/Users/campopinillos/Documents/Proyecto Final/nombres.RData')
write.xlsx(nombres, file = "/Users/campopinillos/Documents/Proyecto Final/nombresFull.xlsx")


# Data for Mongo ----------------------------------------------------------

nombres2 <- select(nombres, Nombres, Nombres2, Genero, Probabilidad, Frecuencia, EdadMedia, Pais)
nombres2 <- filter(nombres2, Probabilidad >=1)
table(is.na(nombres2$Nombres))
table(is.na(nombres2$Nombres2))
table(is.na(nombres2$Genero))
table(is.na(nombres2$Probabilidad))
table(is.na(nombres2$Frecuencia))
table(is.na(nombres2$Pais))

id <- c(1:nrow(nombres2))
nombres2 <- cbind(id, nombres2)

nombres_json=toJSON(nombres2, pretty = TRUE, .withNames=T)
writeLines(nombres_json, "/Users/campopinillos/Documents/Proyecto Final/nombres.JSON")



