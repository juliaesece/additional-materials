df <- read.csv("for_regressions_with_country.csv")

df[df==""]<-NA

df$mentions_own_country <- as.integer(as.logical(df$mentions_own_country))
df$about_own_country <- as.integer(as.logical(df$about_own_country))
df$mentions_gw <- as.integer(as.logical(df$mentions_gw))

filtered_df <- df[(df$country == "gb") | (df$country == "in") | (df$country == "us"),]

print("DISTRIBUTION OF NEWS SOURCES")
print(table(df$country,df$bias))
print(table(df$country,df$adfontes_bias))

print("ABOUT OWN COUNTRY MODELS")

print("Logistic regression for About Own Country, all countries, MBFC bias")
model_MBFC_filtered <- glm(about_own_country ~ country + bias + event, family=binomial, data=df)
print(summary(model_MBFC_filtered))

print("Logistic regression for About Own Country, all countries, Ad Fontes bias")
model_AF_filtered <- glm(about_own_country ~ country + adfontes_bias + event, family=binomial, data=df)
print(summary(model_AF_filtered))

print("CONTROL COUNTRIES")

print("Logistic regression for About Own Country, control countries, MBFC bias")
model_MBFC_filtered <- glm(about_own_country ~ country + bias + event, family=binomial, data=filtered_df)
print(summary(model_MBFC_filtered))

print("Logistic regression for About Own Country, control countries, Ad Fontes bias")
model_AF_filtered <- glm(about_own_country ~ country + adfontes_bias + event, family=binomial, data=filtered_df)
print(summary(model_AF_filtered))


# Calculate probabilities
intercept = exp(-0.82987) / (1 + exp(-0.82987)) # intercept: UK
pro_science = exp(-0.82987 - 2.30880) / (1 + exp(-0.82987 - 2.30880))

print("MENTIONS CLIMATE CHANGE MODELS")

print("Logistic regression for Mentions Climate Change, all countries, MBFC bias")

model_MDFC <- glm(mentions_gw ~ country + bias + event + about_own_country, family=binomial, data=df)
print(summary(model_MDFC))

print("Logistic regression for Mentions Climate Change, all countries, Ad Fontes bias")

model_AF <- glm(mentions_gw ~ country + adfontes_bias + event + about_own_country, family=binomial, data=df)
print(summary(model_AF))


print("Logistic regression for Mentions Climate Change, control countries, MBFC bias")

model_MDFC <- glm(mentions_gw ~ country + bias + event + about_own_country, family=binomial, data=filtered_df)
print(summary(model_MDFC))

print("Logistic regression for Mentions Climate Change, all countries, Ad Fontes bias")

model_AF <- glm(mentions_gw ~ country + adfontes_bias + event + about_own_country, family=binomial, data=filtered_df)
print(summary(model_AF))

intercept = exp(-0.1292) / (1 + exp(-0.1292)) # intercept with adfontes
heatwave = exp(-0.1292 + 3.0404) / (1 + exp(-0.1292 + 3.0404))
about_own = exp(-0.1292 + -0.6610) / (1 + exp(-0.1292 + -0.6610))
intercept - about_own

intercept = exp(-1.6608) / (1 + exp(-1.6608)) # intercept with mbfc
proscience = exp(-1.6608 + 1.9295) / (1 + exp(-1.6608 + 1.9295))
proscience-intercept