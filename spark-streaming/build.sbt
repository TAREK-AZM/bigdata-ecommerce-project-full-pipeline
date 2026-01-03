name := "EcommerceStreamProcessor"

version := "1.0"

scalaVersion := "2.12.18"

val sparkVersion = "3.5.0"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-sql" % sparkVersion,
  "org.apache.spark" %% "spark-streaming" % sparkVersion,
  "org.apache.spark" %% "spark-sql-kafka-0-10" % sparkVersion,
  "org.apache.hbase" % "hbase-client" % "2.5.5",
  "org.apache.hbase" % "hbase-common" % "2.5.5",
  "org.apache.hbase" % "hbase-mapreduce" % "2.5.5",
  "com.typesafe" % "config" % "1.4.2"
)

assemblyMergeStrategy in assembly := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case x => MergeStrategy.first
}
