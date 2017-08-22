w = read.csv("dist.txt", header=F)
ann = aggregate(w[w[,1]=='diagonal',3], list(w[w[,1]=='diagonal',2]), median)
bnn = aggregate(w[w[,1]=='paralelo',3], list(w[w[,1]=='paralelo',2]), median)
print(ann)
print(bnn)

