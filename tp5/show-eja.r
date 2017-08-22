w = read.csv("discrete-error.csv", header=F)
summary(w[,1])
res = sapply(list(w[,1]), sd)
print(res)

