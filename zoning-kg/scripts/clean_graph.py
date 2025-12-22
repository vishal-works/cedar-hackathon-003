#!/usr/bin/env python3
"""
Graph cleanup script (non-destructive).

Actions:
- Normalize edge type names to canonical upper-case forms.
- Tag rare/noisy edge types (<=2 occurrences) with r.noisy=true.
- Remove base Entity label from typed nodes.
- Tag untyped entities (NeedsType=true).
- Tag orphan nodes (orphan_candidate=true).
- Tag duplicate-name entities (duplicate_candidate=true, duplicate_group=name).

All steps avoid deletions/merges to prevent data loss.
"""

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def run(tx, query, params=None):
    return list(tx.run(query, params or {}))


def main():
    with driver.session() as session:
        print("=== Normalize edge type names ===")
        session.execute_write(
            run,
            """
            UNWIND [
              ['CONTAINS',      ['Contains']],
              ['APPLIES_IN',    ['AppliesIn','APPLIESIN']],
              ['ALLOWS_USE',    ['AllowsUse','ALLOWSUSE']],
              ['GOVERNED_BY',   ['GovernedBy']],
              ['SOURCED_FROM',  ['SourcedFrom']],
              ['HAS_CONSTRAINT',['HasConstraint','HASCONSTRAINT']],
              ['HAS_CONDITION', ['HasCondition']]
            ] AS mapping
            WITH mapping[0] AS canonical, mapping[1] AS variants
            UNWIND variants AS v
            MATCH ()-[r:RELATES_TO {name:v}]->()
            SET r.name = canonical
            """,
        )

        print("=== Tag rare/noisy edge types (<=2 occurrences) ===")
        session.execute_write(
            run,
            """
            MATCH ()-[r:RELATES_TO]->()
            WITH r.name AS edge, count(*) AS cnt
            WHERE cnt <= 2
            MATCH ()-[r:RELATES_TO {name:edge}]->()
            SET r.noisy = true
            """,
        )

        print("=== Remove Entity label from typed nodes ===")
        session.execute_write(
            run,
            """
            MATCH (n:Entity)
            WHERE n:Zone OR n:Rule OR n:UseType OR n:Constraint
               OR n:Jurisdiction OR n:Override OR n:Condition OR n:DocumentSource
            REMOVE n:Entity
            """,
        )

        print("=== Tag untyped entities (NeedsType) ===")
        session.execute_write(
            run,
            """
            MATCH (n:Entity)
            WHERE NOT (n:Zone OR n:Rule OR n:UseType OR n:Constraint
                       OR n:Jurisdiction OR n:Override OR n:Condition OR n:DocumentSource)
            SET n.NeedsType = true
            """,
        )

        print("=== Tag orphan nodes (orphan_candidate) ===")
        session.execute_write(
            run,
            """
            MATCH (n)
            WHERE NOT (n)-[:RELATES_TO]-() AND NOT (n)<-[:RELATES_TO]-()
            SET n.orphan_candidate = true
            """,
        )

        print("=== Tag duplicate-name entities (duplicate_candidate) ===")
        session.execute_write(
            run,
            """
            MATCH (n)
            WHERE n.name IS NOT NULL
            WITH n.name AS name, collect(n) AS nodes, count(*) AS cnt
            WHERE cnt > 1
            UNWIND nodes AS node
            SET node.duplicate_candidate = true,
                node.duplicate_group = name
            """,
        )

        print("Cleanup complete (non-destructive).")


if __name__ == "__main__":
    main()
