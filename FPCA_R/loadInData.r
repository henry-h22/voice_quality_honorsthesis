library(tidyverse)
data("acoustics", package = "voicequality")
data("egg", package = "voicequality")

gujarati <- acoustics %>% 
  filter(language == "Gujarati") %>% 
  left_join(egg) %>% 
  filter(timepoint == 5)

hmong <- acoustics %>% 
  filter(language == "Hmong") %>% 
  left_join(egg) %>% 
  filter(timepoint == 5)

mandarin <- acoustics %>% 
  filter(language == "Mandarin") %>% 
  left_join(egg) %>% 
  filter(timepoint == 5)

luchun <- acoustics %>% 
  filter(language == "Luchun") %>% 
  left_join(egg) %>% 
  filter(timepoint == 5)

yi <- acoustics %>% 
  filter(language == "Yi") %>% 
  left_join(egg) %>% 
  filter(timepoint == 5)

bo <- acoustics %>% 
  filter(language == "Bo") %>% 
  left_join(egg) %>% 
  filter(timepoint == 5)

miao <- acoustics %>% 
  filter(language == "Miao") %>% 
  left_join(egg) %>% 
  filter(timepoint == 5)

zapotec <- acoustics %>% 
  filter(language == "Zapotec") %>% 
  left_join(egg) %>% 
  filter(timepoint == 5)

all_data <- rbind(gujarati, hmong, mandarin, luchun, yi, bo, miao, zapotec) %>% 
  filter(!is.na(CQ)) %>% 
  filter(!is.na(strF0))

print(nrow(all_data))

all_data <- all_data %>% 
  # filter(SQ2_SQ1 > 0) %>% 
  # filter(SQ2_SQ1 < 1) %>% 
  # filter(SQ4_SQ3 > 0) %>% 
  # filter(SQ4_SQ3 < 1) %>% 
  mutate(LPhon = paste(language, phonation, sep = "-") %>% as.factor()) %>% 
  mutate(SQ = SQ2_SQ1 / SQ4_SQ3) %>% 
  filter(SQ > 0) %>% 
  filter(SQ < 1) %>% 
  filter(CQ_H > 0)

print(nrow(all_data))
