(ns kafkarunner.topology
  (:require [clojure.data.json :as json]
            [kafkarunner
              [spouts :refer [kafka-spout]]]
            [backtype.storm [clojure :refer [topology spout-spec bolt-spec shell-bolt-spec]] [config :refer :all]])
  (:import [backtype.storm LocalCluster]))

(defn get-modules
  []
  (json/read-str (slurp "../../configs/wiki.json") :key-fn keyword))

(defn transform-module [[n module]]
  (let [input (into {} (map (fn [m] [m :shuffle]) (:input module)))]
    [(name n) (shell-bolt-spec input
                     "python"
                     (str "/home/kevin/worker/101worker/modules/" (name n) "/program.py")
                     (:output module))]))

(defn transform-modules [modules]
  (into {} (map transform-module modules)))

(defn storm-topology
  []
  (let [modules       (get-modules)
        storm-modules (transform-modules modules)]
    (topology
      {"kafka" (spout-spec (kafka-spout "101wiki"))}
      storm-modules)))


(defn run! [& {debug "debug" workers "workers" :or {debug "true" workers "2"}}]
  (doto (LocalCluster.)
    (.submitTopology "101 storm topology"
                     {TOPOLOGY-DEBUG (Boolean/parseBoolean debug)
                      TOPOLOGY-WORKERS (Integer/parseInt workers)}
                     (storm-topology))))
