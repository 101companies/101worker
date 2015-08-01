(ns kafkarunner.spouts
  "Spouts.

More info on the Clojure DSL here:

https://github.com/nathanmarz/storm/wiki/Clojure-DSL"
  (:require [backtype.storm [clojure :refer [defspout spout emit-spout!]]]
            [clojure.data.json :as json]))

(def config {"zookeeper.connect" "localhost:2181"
             "group.id" "clj-kafka.consumer"
             "auto.offset.reset" "smallest"
             "auto.commit.enable" "true"})

(defn kafka-spout
  [topic]
  (let [hosts (storm.kafka.ZkHosts. "localhost:2181")
        spoutConfig (storm.kafka.SpoutConfig. hosts topic (str "/" topic) (str topic "-listener"))]
        (set! (.scheme spoutConfig) (backtype.storm.spout.SchemeAsMultiScheme. (storm.kafka.StringScheme.)))
        (storm.kafka.KafkaSpout. spoutConfig)))
