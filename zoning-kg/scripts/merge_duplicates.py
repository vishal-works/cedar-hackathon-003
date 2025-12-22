#!/usr/bin/env python3
"""
Merge duplicate nodes (duplicate_candidate=true) without APOC.
Assumptions:
- Relationship types are limited to RELATES_TO and MENTIONS.
- Edge semantics stored in r.name; properties are preserved.

Strategy per duplicate_group:
- Choose first node as keeper.
- For each other node:
  - Re-link incoming/outgoing relationships to keeper (preserve type & props).
  - Merge properties into keeper (last-write wins for same keys; properties are added).
  - Union labels.
  - Detach delete the duplicate.

This is destructive (removes duplicate nodes) but preserves relationships and properties.
"""

import os
from dotenv import dotenv_values
from neo4j import GraphDatabase

env = dotenv_values('.env')
uri = env.get('NEO4J_URI')
user = env.get('NEO4J_USER')
pwd  = env.get('NEO4J_PASSWORD')
if not (uri and user and pwd):
    raise SystemExit('Missing Neo4j connection env vars')

driver = GraphDatabase.driver(uri, auth=(user, pwd))

merge_query = """
// Get groups with duplicate_candidate flag
MATCH (n)
WHERE n.duplicate_candidate = true AND n.duplicate_group IS NOT NULL
WITH n.duplicate_group AS grp, collect(n) AS nodes
WHERE size(nodes) > 1
// Process each group separately
CALL {
  WITH nodes
  WITH nodes[0] AS keeper, nodes[1..] AS others
  UNWIND others AS o
  // incoming relationships
  OPTIONAL MATCH (s)-[r]->(o)
  WITH keeper, o, s, r
  FOREACH (_ IN CASE WHEN type(r)='RELATES_TO' THEN [1] ELSE [] END |
    MERGE (s)-[nr:RELATES_TO]->(keeper)
    SET nr += properties(r)
  )
  FOREACH (_ IN CASE WHEN type(r)='MENTIONS' THEN [1] ELSE [] END |
    MERGE (s)-[nr:MENTIONS]->(keeper)
    SET nr += properties(r)
  )
  // outgoing relationships
  WITH keeper, o
  OPTIONAL MATCH (o)-[r]->(t)
  WITH keeper, o, r, t
  FOREACH (_ IN CASE WHEN type(r)='RELATES_TO' THEN [1] ELSE [] END |
    MERGE (keeper)-[nr:RELATES_TO]->(t)
    SET nr += properties(r)
  )
  FOREACH (_ IN CASE WHEN type(r)='MENTIONS' THEN [1] ELSE [] END |
    MERGE (keeper)-[nr:MENTIONS]->(t)
    SET nr += properties(r)
  )
  // merge properties and labels into keeper
  WITH keeper, o
  SET keeper += o
  WITH keeper, o, labels(o) AS labs
  UNWIND labs AS lab
  SET keeper:`${lab}`
  // remove duplicate node
  DETACH DELETE o
  RETURN count(*) AS merged
}
RETURN count(*) AS groups_processed;
"""

with driver.session() as session:
    res = session.run(merge_query)
    groups_processed = res.single()[0]
    print(f"Groups processed: {groups_processed}")

print("Duplicate merge complete.")
