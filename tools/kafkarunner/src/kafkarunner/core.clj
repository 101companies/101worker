(ns kafkarunner.core
  (:gen-class)
  (:require [kafkarunner.topology :as topology]))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (topology/run!))
