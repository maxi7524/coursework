# Analiza regresji dla danych Abalone w R

# ---------------------------
# 1. Ładowanie bibliotek
# ---------------------------
if (!require("tidyverse")) install.packages("tidyverse")
if (!require("car")) install.packages("car")
if (!require("broom")) install.packages("broom")
if (!require("ggcorrplot")) install.packages("ggcorrplot")
if (!require("huxtable")) install.packages("huxtable")
if (!require("performance")) install.packages("performance")

library(tidyverse)
library(car)
library(broom)
library(ggcorrplot)
library(huxtable)
library(performance)

set.seed(1333)

# Ustawienie ziarna dla reprodukowalności
set.seed(1333)

# ---------------------------
# 2. Funkcje pomocnicze
# ---------------------------

# Funkcja do obliczania VIF
calculate_vifs <- function(df) {
  # Tworzymy tymczasowy model z fikcyjną zmienną zależną
  temp_df <- df %>% select(where(is.numeric))
  temp_model <- lm(I(rep(1, nrow(temp_df))) ~ ., data = temp_df)
  
  # Obliczamy VIF dla każdej zmiennej
  vif_values <- car::vif(temp_model)
  
  # Zwracamy jako uporządkowaną ramkę danych
  tibble(
    Zmienna = names(vif_values),
    VIF = vif_values
  ) %>% arrange(desc(VIF))
}

# Funkcja do testowania istotności nowych zmiennych
test_feature_importance <- function(base_df, y, test_features) {
  results <- tibble()
  
  # Model bazowy
  base_model <- lm(y ~ ., data = base_df)
  
  for (feature in names(test_features)) {
    # Nowy model z dodatkową zmienną
    new_df <- bind_cols(base_df, test_features[feature])
    names(new_df)[ncol(new_df)] <- feature  # Upewniamy się, że nazwa kolumny jest poprawna
    new_model <- lm(y ~ ., data = new_df)
    
    # Porównanie modeli
    anova_test <- anova(base_model, new_model)
    
    # Zapis wyników
    results <- bind_rows(results, tibble(
      Zmienna = feature,
      RSS_diff = anova_test$RSS[2] - anova_test$RSS[1],
      df_diff = anova_test$Df[2] - anova_test$Df[1],
      F_stat = anova_test$F[2],
      p_value = anova_test$`Pr(>F)`[2]
    ))
  }
  
  # Dodanie informacji o odrzuceniu H0
  results %>% mutate(
    Odrzucenie_H0 = p_value < 0.05
  )
}

# ---------------------------
# 3. Wczytanie i przygotowanie danych
# ---------------------------

# Wczytanie danych
abalone <- read_csv("abalone.csv", col_names = c("Plec", "Dlugosc", "Srednica", "Wysokosc", 
                                               "Cala_waga", "Waga_po_obraniu", "Waga_trzewi", 
                                               "Waga_powloki", "Pierscienie"), skip = 1)

# Kodowanie zmiennej kategorycznej
abalone <- abalone %>%
  mutate(
    Plec_M = as.numeric(Plec == "M"),
    Plec_F = as.numeric(Plec == "F"),
    Plec_I = as.numeric(Plec == "I")
  ) %>%
  select(-Plec) %>%
  select(Plec_I, Plec_M, Plec_F, everything())

# ---------------------------
# 4. Analiza danych
# ---------------------------

# Podział na zmienne objaśniające i docelową
X <- abalone %>% select(-Pierscienie)
y <- abalone$Pierscienie

# Parametry do redukcji
sex_columns <- c("Plec_I", "Plec_M", "Plec_F")
reduce_features <- c("Srednica", "Cala_waga")

# ---------------------------
# 5. Modelowanie dla samic (F)
# ---------------------------

# Filtracja danych dla samic
X_F <- X %>% filter(Plec_F == 1) %>% select(-all_of(sex_columns), -all_of(reduce_features))
y_F <- y[X$Plec_F == 1]

# Tworzenie nowych zmiennych (zgodnie z Twoją nową wersją)
X_new <- X_F %>%
  mutate(
    # stosunki wymiarów
    `Dlugosc/Wysokosc` = abalone$Dlugosc[X$Plec_F == 1] / abalone$Srednica[X$Plec_F == 1],
    
    # masa / objętość
    `Masa/objetosc` = abalone$Cala_waga[X$Plec_F == 1] * abalone$Dlugosc[X$Plec_F == 1] * 
                      abalone$Srednica[X$Plec_F == 1] * abalone$Wysokosc[X$Plec_F == 1],
    
    # stosunki mas
    `Waga_powloki/Waga_po_obraniu` = abalone$Waga_powloki[X$Plec_F == 1] / abalone$Waga_po_obraniu[X$Plec_F == 1],
    `Waga_powloki/Waga_trzewi` = abalone$Waga_powloki[X$Plec_F == 1] / abalone$Waga_trzewi[X$Plec_F == 1],
    `Waga_powloki/Cala_waga` = abalone$Waga_powloki[X$Plec_F == 1] / abalone$Cala_waga[X$Plec_F == 1],
    `Waga_po_obraniu/Cala_waga` = abalone$Waga_po_obraniu[X$Plec_F == 1] / abalone$Cala_waga[X$Plec_F == 1],
    `Waga_trzewi/Cala_waga` = abalone$Waga_trzewi[X$Plec_F == 1] / abalone$Cala_waga[X$Plec_F == 1]
  )

# Testowanie nowych zmiennych
new_features <- setdiff(names(X_new), names(X_F))
results <- test_feature_importance(X_F, y_F, X_new[new_features])

# Wyświetlenie wyników
print(results)

# Usunięcie nieistotnych zmiennych
drop_features <- results %>% filter(p_value >= 0.05) %>% pull(Zmienna)
X_new_features <- X_new %>% select(-all_of(drop_features))

# Ponowna analiza VIF
cat("\nVIF po usunięciu nieistotnych zmiennych:\n")
print(calculate_vifs(X_new_features))

# Finalny wybór zmiennych
X_final <- X_new_features %>% select(-Waga_po_obraniu, -Waga_trzewi, -Waga_powloki)

# ---------------------------
# 6. Budowa i ocena modeli
# ---------------------------

# Model ze wszystkimi zmiennymi
model_full <- lm(y_F ~ ., data = X_new)
summary(model_full)

# Model ze zredukowanymi zmiennymi
model_reduced <- lm(y_F ~ ., data = X_final)
summary(model_reduced)

# Porównanie modeli
anova(model_full, model_reduced)

# ---------------------------
# 7. Diagnostyka modelu
# ---------------------------

# Reszty modelu
residuals <- residuals(model_reduced)

# Wykres QQ
qqnorm(residuals)
qqline(residuals, col = "red")
title("Wykres QQ reszt modelu")

# Testy normalności
shapiro.test(residuals)

# Inne wykresy diagnostyczne
par(mfrow = c(2, 2))
plot(model_reduced)
par(mfrow = c(1, 1))