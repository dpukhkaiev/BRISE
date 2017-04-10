library("randtoolbox")
args <- commandArgs(TRUE)
N <- args[1]
sob <- sobol(as.integer(N),2)
#rownames(sob, do.NULL = TRUE, prefix = "row")
#rownames(sob) <- c(1:512)
#colnames(sob, do.NULL = TRUE, prefix = "col")
#colnames(sob) <- c("TR","FR")
#sob
vec <- c(6,16)
dimnames(sob) <- list(c(1:N), c("TR", "FR"))
#sob <- sob[,1] * 32
#sob <- sob[,2] * 16
sob <- sweep(sob,MARGIN=2,vec,"*")
x <- sample(1:1000000, 1)
filename <- args[2]
write.csv(sob, file=filename, sep=",",row.names=FALSE)
#sink("somefile",split=FALSE)
#apply(fract.design, , "somefile",append=TRUE)
#sob
