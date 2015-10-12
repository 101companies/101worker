# Headline

A module assigning and validating 101wiki and 101repo URLs

# Description

This module goes certain metadata keys, that can be found in .101meta files. It then checks whether a wiki page exists
for this kind of metadata and creates a entry in its dump.
It will then go over all contributions defined in the wiki and check if there is a repository link that belongs to this
contribution.

# Requirements

This program relies on the output produced by pull101repo(PullRepo.json), rules101meta (rules.json) and wiki2json (Wiki101Full.json)
 modules.