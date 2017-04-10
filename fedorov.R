library(AlgDesign)
trials <- commandArgs(TRUE)
trials
levels.design <- c(16,6)
f.design <-gen.factorial(levels.design)
fract.design <- optFederov(data=f.design,nTrials=as.integer(trials))
sink("somefile",split=FALSE)
#apply(fract.design, , "somefile",append=TRUE)
cat(fract.design$rows)
