library(MASS) 
library(marginaleffects)

df <- read.csv("for_regressions_sentiment.csv")

df[df==""]<-NA

completeFun <- function(data, desiredCols) {
  completeVec <- complete.cases(data[, desiredCols])
  return(data[completeVec, ])
}

clean_df <- completeFun(df, "overarching_sentiment")


filtered_df <- clean_df[(clean_df$country == "gb") | (clean_df$country == "in") | (clean_df$country == "us"),]
model_adfontes <- polr(ordered(overarching_sentiment, levels = c("opportunity", "balanced", "cost")) ~ country + adfontes_bias, data = filtered_df, Hess=TRUE, method = "logistic")
summary(model_adfontes)

model_mbfc <- polr(ordered(overarching_sentiment, levels = c("opportunity", "balanced", "cost")) ~ country + bias, data = filtered_df, Hess=TRUE, method = "logistic")
summary(model_mbfc)

ame = avg_slopes(model_mbfc)
print(ame, nrows=50)

ame_af = avg_slopes(model_adfontes)
print(ame_af, nrows=50)