#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

new <- read.csv(file='/home/zeta/autoHouse/new', head = TRUE)
old <- read.csv(file='/home/zeta/autoHouse/old', head = TRUE)

old <- unique(old)
new <- unique(new)

old$included_old <- TRUE
new$included_new <- TRUE

res <- merge(old, new, all=TRUE)

numNew = nrow(subset(res, is.na(res$included_old)))
numRem = nrow(subset(res, is.na(res$included_new)))

cat("\n\nReport houseSearcher - ")
Sys.time()

cat("\n\n", numNew, " new listing.\n", numRem, " listings were removed\n\n")
cat("Number of new apartament by area:\n\n")

summary( subset(res, is.na(res$included_old) )$area )



cat("\nSummary dei prezzi per nuovi appartamenti:\n\n")
summary(subset(res, is.na(res$included_old) )$price)
cat("\n\n")
#merge(aggregate(price ~ area, apts, mean), aggregate(id ~ area, apts, count))
cat("New apartaments\n")
subset(res, is.na(res$included_old))[,c(3,4,7,8)]
cat("\n\n")



#print("PRICES: Summary for this week")
#summary(apts$price)
#print("")
#print("Distribution of apartaments per area")
#summary(apts$area)
