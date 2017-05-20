#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

# Tool function to remove spaces on strings

trim <- function (x) gsub("^\\s+|\\s+$", "", x)



# Define function to add clean "location" column
# The format will be XXX,Stuttgart. It is used
# to group and calculate average price per area

beautyLocation <- function(addr) {
addr <- as.character(addr)
a <- trim( tail( unlist(strsplit(addr, ",")),2))[1]
b <- trim( tail( unlist(strsplit(addr, ",")),2))[2]
return( paste(a,b,sep=",") )
}



# Read the input file
tryCatch({
    d <- read.csv(file=args[1], head = TRUE)
},
warning = function(w) {
    print()
},
error = function( err ) {
    print("An error occurred while reading the input file, terminating.")
    message( err )
    print(" \n ")
    quit()
})

if ('location' %in% names(d))
    quit()

if (nrow(d) < 4)
    quit()

# Add the 'location' field by cleaning the address

d$location <- lapply(d$address, beautyLocation )
d$location <- as.character( d$location )



# Create the mean price per each location

cc <- aggregate(d$price/d$meters, list(d$location), mean)

# Remove row with value Inf

cc <- cc[apply(cc[c(2)],1,function(z) !any(z==Inf)),]

# Change column names

colnames(cc) <- c("location", "avgPrice")

# Write the data to file
ifile <- as.character( sub(".*/", "", args[1]) )
ofile <- as.character( paste( strsplit(ifile, "[.]")[[1]], ".csv", sep="_priceByLocation")[[1]] )
write.csv(cc, file = ofile)








