(defproject kafkarunner "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.6.0"]
                 [clj-time "0.8.0"]
                 [http-kit "2.1.18"]
                 [org.apache.storm/storm-core "0.11.0-SNAPSHOT"]
                 [org.apache.storm/multilang-python "0.11.0-SNAPSHOT"]
                 [org.apache.kafka/kafka_2.9.2 "0.8.2.0"]
                 [org.apache.curator/curator-framework "2.5.0"]
                 [org.apache.curator/curator-recipes "2.5.0"]
                 [org.clojure/data.json "0.2.6"]]
  :main ^:skip-aot kafkarunner.core
  :resource-paths ["lib/storm-kafka-0.11.0-SNAPSHOT.jar"]
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
