# Create the SparkContext object
from pyspark import SparkConf, SparkContext
conf = SparkConf()
sc = SparkContext(conf=conf)

# Read file lines and parallelize them
# over the cluster in a Spark RDD
lines = open("myfile.txt ")
lines_rdd = sc.parallelize(lines)

# Remove punctuation, make lines lowercase
def clean_line(s):
    s2 = s.strip().lower()
    s3 = s2.replace(".","").replace(",","")
    return s3

lines_clean = lines_rdd.map(clean_line)

# Break each line into words
words_rdd = lines_clean.flatmap(lambda l: l.split())

# Count words
def merge_counts(count1, count2):
    return count1 + count2

words_w_1 = words_rdd.map(lambda w: (w, 1))
counts = words_w_1.reduceByKey(merge_counts) 

# Collect counts and display
for word, count in counts.collect():
    print "%s: %i " % (word, count)
