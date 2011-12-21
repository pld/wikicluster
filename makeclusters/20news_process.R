setwd("/Users/kg/Documents/UvA/2010-2011/Classes/Semester 1/Profile Project/Code/wikicluster/trunk/makeclusters")

## load libraries
require("tm")
require("lda")

## global params
K <- 20 ## number of topics

## load the 20 news groups
ng20 <- Corpus(DirSource("20news-18828", encoding = "UTF-8", recursive = TRUE))

## load each dir
dirs <- c(
	"alt.atheism",
	"comp.graphics",
	"comp.os.ms-windows.misc",
	"comp.sys.ibm.pc.hardware",
	"comp.sys.mac.hardware",
	"comp.windows.x",
	"rec.autos",
	"rec.motorcycles",
	"rec.sport.baseball",
	"rec.sport.hockey",
	"sci.crypt",
	"sci.electronics",
	"sci.med",
	"sci.space",
	"misc.forsale",
	"talk.politics.misc",
	"talk.politics.guns",
	"talk.politics.mideast",
	"talk.religion.misc",
	"soc.religion.christian"
)
maxes <- c(25, 38, 25, 32, 25, 55, 14, 12, 15, 25, 42, 26, 34, 35, 20, 39, 26, 34, 29, 26)

sink("top_terms_lower.txt")
for (i in seq(1,K)) {
	ng20_dir <- Corpus(DirSource(paste("20news-18828/",dirs[i],sep=""), encoding = "UTF-8", recursive = TRUE))
	tdm <- DocumentTermMatrix(ng20_dir, control = list(weighting = weightTf, stopwords = TRUE))
	write.table(i, quote=FALSE)
	write.table(findFreqTerms(tdm, maxes[i]), quote=FALSE)
}
write.table(top.terms.out, quote=FALSE)
sink()

## clean data
#removeStopWords <- function(x) removeWords(x, stopwords("en"))
# punc, space, and number removed in preprocessing
#funs = list(removeNumbers, removePunctuation, removeStopWords, stripWhitespace)
#funs = list(removeStopWords, stripWhitespace)
#ng20_stopped <- tm_map(ng20, FUN=tm_reduce, tmFuns=funs)

## format for LDA
corp_lda <- lexicalize(ng20, lower=TRUE)

## parameters for LDA
num.iterations <- 25
alpha <- 0.1
eta <- 0.1

## run LDA Gibbs
result_lda <- lda.collapsed.gibbs.sampler(corp_lda$documents, K, corp_lda$vocab, num.iterations, alpha, eta, compute.log.likelihood=TRUE)

## Initialize the params
params <- sample(c(1, 20), K, replace=TRUE)

# A length D numeric vector of covariates associated with each document
annotations <- annotations

# run sLDA
result_slda <- slda.em(corp_lda$documents, num.topics, corp_lda$vocab, num.iterations, 4, alpha, eta, annotations, params, variance=0.25, lambda=1.0, logistic=FALSE, method="sLDA")

## Get the top words in the cluster
top.words <- top.topic.words(result_lda$topics, 10, by.score=TRUE)
top.words.out <- data.frame()
for (col in seq(1,K)) {
	top.words.out <- rbind(top.words.out, t(rep(col,K+1)))
	for(word in top.words[,col]) {
		top.words.out <- rbind(top.words.out, t(c(word,result_lda$topics[,word])))
	}
}
sink("top_words_lower.txt")
write.table(top.words.out, quote=FALSE)
sink()
top.documents <- top.topic.documents(result_lda$document_sums, 5)

