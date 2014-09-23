#! /usr/bin/Rscript

data <- read.table("results", header=TRUE, comment.char="")
counts <- table(data$Mementos)
pdf("hist.pdf")
barplot(counts, log="y", ylim=c(.75, nrow(data)), ylab="Sites", xlab="Memento Count", main="Memento Count per Site")
dev.off()