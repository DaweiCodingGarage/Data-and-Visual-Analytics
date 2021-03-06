package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object Task2 {
  def main(args: Array[String]) {
    val sc = new SparkContext(new SparkConf().setAppName("Task2"))

    // read the file
    val file = sc.textFile("hdfs://quickstart.cloudera:8020" + args(0))

    /* TODO: Needs to be implemented */
    val tokenized1=file.flatMap(_.split("\t").drop(1).take(1))
    val tokenized2=file.flatMap(_.split("\t").drop(2)).map(_.toInt)

    val edgecount=tokenized1.zip(tokenized2).reduceByKey(_ + _)


    // store output on given HDFS path.
    // YOU NEED TO CHANGE THIS
    edgecount.map(line=>(line._1+"\t"+line._2)).saveAsTextFile("hdfs://quickstart.cloudera:8020" + args(1))
  }
}
